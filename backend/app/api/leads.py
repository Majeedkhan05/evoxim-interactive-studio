"""Lead management routes."""

from __future__ import annotations

import json
from datetime import datetime
from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Query

from app.database import LEAD_STATUSES, get_db
from app.models.schemas import (
    DiscoverySession,
    LeadCreate,
    LeadDetail,
    LeadResponse,
    LeadStatus,
    LeadStatusUpdate,
    lead_row_to_detail,
    lead_row_to_response,
)
from app.services.recommendation import generate_recommendation

router = APIRouter(prefix="/api/leads", tags=["leads"])


@router.post("", response_model=LeadDetail, status_code=201)
def create_lead(payload: LeadCreate) -> LeadDetail:
    """Create a new lead from discovery data."""
    lead_id = str(uuid4())
    now = datetime.utcnow().isoformat()

    # Generate recommendation from discovery data
    recommendation = generate_recommendation(payload.discovery)

    discovery_dict = payload.discovery.model_dump(mode="json")

    with get_db() as conn:
        conn.execute(
            """
            INSERT INTO leads
                (id, name, company, email, phone, team_size, language, status,
                 recommended_service, objectives, context, discovery_answers,
                 ai_summary, ai_brief, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                lead_id,
                payload.name,
                payload.company,
                payload.email,
                payload.phone,
                payload.discovery.team_size,
                payload.discovery.language.value,
                LeadStatus.NEW.value,
                recommendation.recommended_service,
                json.dumps(payload.discovery.objectives),
                payload.discovery.situation_description,
                json.dumps(discovery_dict),
                recommendation.client_summary,
                None,
                now,
                now,
            ),
        )

        # Track analytics event
        conn.execute(
            "INSERT INTO analytics_events (id, event_type, metadata, created_at) VALUES (?, ?, ?, ?)",
            (
                str(uuid4()),
                "lead_created",
                json.dumps({"lead_id": lead_id, "service": recommendation.recommended_service}),
                now,
            ),
        )

        row = conn.execute("SELECT * FROM leads WHERE id = ?", (lead_id,)).fetchone()

    return lead_row_to_detail(dict(row))


@router.get("", response_model=list[LeadResponse])
def list_leads(
    status: Optional[LeadStatus] = None,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[LeadResponse]:
    """List leads with optional status filter (admin)."""
    with get_db() as conn:
        if status:
            rows = conn.execute(
                "SELECT * FROM leads WHERE status = ? ORDER BY created_at DESC LIMIT ? OFFSET ?",
                (status.value, limit, offset),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM leads ORDER BY created_at DESC LIMIT ? OFFSET ?",
                (limit, offset),
            ).fetchall()

    return [lead_row_to_response(dict(r)) for r in rows]


@router.get("/{lead_id}", response_model=LeadDetail)
def get_lead(lead_id: str) -> LeadDetail:
    """Get full lead detail."""
    with get_db() as conn:
        row = conn.execute("SELECT * FROM leads WHERE id = ?", (lead_id,)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead_row_to_detail(dict(row))


@router.patch("/{lead_id}/status", response_model=LeadResponse)
def update_lead_status(lead_id: str, payload: LeadStatusUpdate) -> LeadResponse:
    """Update lead status."""
    now = datetime.utcnow().isoformat()

    if payload.status.value not in LEAD_STATUSES:
        raise HTTPException(status_code=400, detail=f"Invalid status: {payload.status}")

    with get_db() as conn:
        row = conn.execute("SELECT * FROM leads WHERE id = ?", (lead_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Lead not found")

        conn.execute(
            "UPDATE leads SET status = ?, updated_at = ? WHERE id = ?",
            (payload.status.value, now, lead_id),
        )

        conn.execute(
            "INSERT INTO analytics_events (id, event_type, metadata, created_at) VALUES (?, ?, ?, ?)",
            (
                str(uuid4()),
                "lead_status_changed",
                json.dumps({
                    "lead_id": lead_id,
                    "old_status": row["status"],
                    "new_status": payload.status.value,
                }),
                now,
            ),
        )

        updated = conn.execute("SELECT * FROM leads WHERE id = ?", (lead_id,)).fetchone()

    return lead_row_to_response(dict(updated))


@router.post("/{lead_id}/brief")
def generate_brief(lead_id: str) -> dict:
    """
    Generate an AI brief for a lead.

    MVP: generates a deterministic summary from discovery data.
    Future: call LLM for richer analysis.
    """
    with get_db() as conn:
        row = conn.execute("SELECT * FROM leads WHERE id = ?", (lead_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Lead not found")

        lead = dict(row)
        lang = lead.get("language", "en")
        discovery = json.loads(lead["discovery_answers"]) if lead["discovery_answers"] else {}

        # Build deterministic brief
        objectives = json.loads(lead["objectives"]) if lead["objectives"] else []
        service = lead.get("recommended_service", "exploration_discovery")

        if lang == "fr":
            brief_lines = [
                f"Resume pour {lead['name']} ({lead['company']})",
                f"Taille d'equipe: {lead.get('team_size', 'N/A')} personnes",
                f"Service recommande: {service}",
                f"Objectifs: {', '.join(objectives) if objectives else 'Non specifies'}",
            ]
            if lead.get("context"):
                brief_lines.append(f"Contexte: {lead['context']}")
            brief_lines.append("Pret pour un appel decouverte pour approfondir les besoins.")
        else:
            brief_lines = [
                f"Brief for {lead['name']} ({lead['company']})",
                f"Team size: {lead.get('team_size', 'N/A')} people",
                f"Recommended service: {service}",
                f"Objectives: {', '.join(objectives) if objectives else 'Not specified'}",
            ]
            if lead.get("context"):
                brief_lines.append(f"Context: {lead['context']}")
            brief_lines.append("Ready for a discovery call to deepen understanding of needs.")

        brief_text = "\n".join(brief_lines)

        now = datetime.utcnow().isoformat()
        conn.execute(
            "UPDATE leads SET ai_brief = ?, updated_at = ? WHERE id = ?",
            (brief_text, now, lead_id),
        )

    return {"lead_id": lead_id, "brief": brief_text}
