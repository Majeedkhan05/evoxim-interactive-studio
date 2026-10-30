"""Proposal routes."""

from __future__ import annotations

import json
from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, HTTPException

from app.database import get_db
from app.models.schemas import (
    ProposalCreate,
    ProposalResponse,
    ProposalStatus,
    proposal_row_to_response,
)
from app.services.proposal import generate_proposal
from app.services.recommendation import generate_recommendation
from app.models.schemas import DiscoverySession

router = APIRouter(tags=["proposals"])


@router.post("/api/leads/{lead_id}/proposal", response_model=ProposalResponse, status_code=201)
def create_proposal(lead_id: str, payload: ProposalCreate) -> ProposalResponse:
    """Generate a proposal for a lead."""
    with get_db() as conn:
        lead_row = conn.execute("SELECT * FROM leads WHERE id = ?", (lead_id,)).fetchone()
        if not lead_row:
            raise HTTPException(status_code=404, detail="Lead not found")

        lead = dict(lead_row)
        lang = payload.language.value

        # Reconstruct recommendation from discovery answers
        discovery_data = json.loads(lead["discovery_answers"]) if lead["discovery_answers"] else {}
        if discovery_data:
            session = DiscoverySession(**discovery_data)
            recommendation = generate_recommendation(session)
        else:
            # Minimal fallback
            session = DiscoverySession(
                team_size=lead.get("team_size") or 10,
                organization=lead["company"],
                language=payload.language,
            )
            recommendation = generate_recommendation(session)

        # Generate proposal content
        proposal_content = generate_proposal(lead, recommendation, lang)

        # Determine version number
        existing = conn.execute(
            "SELECT MAX(version) as max_v FROM proposals WHERE lead_id = ?",
            (lead_id,),
        ).fetchone()
        version = (existing["max_v"] or 0) + 1

        proposal_id = str(uuid4())
        now = datetime.utcnow().isoformat()

        conn.execute(
            """
            INSERT INTO proposals (id, lead_id, version, content, status, language, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                proposal_id,
                lead_id,
                version,
                json.dumps(proposal_content),
                ProposalStatus.DRAFT.value,
                lang,
                now,
            ),
        )

        # Update lead status
        conn.execute(
            "UPDATE leads SET status = 'PROPOSAL_DRAFT', updated_at = ? WHERE id = ?",
            (now, lead_id),
        )

        # Track event
        conn.execute(
            "INSERT INTO analytics_events (id, event_type, metadata, created_at) VALUES (?, ?, ?, ?)",
            (
                str(uuid4()),
                "proposal_generated",
                json.dumps({"lead_id": lead_id, "proposal_id": proposal_id, "version": version}),
                now,
            ),
        )

        row = conn.execute("SELECT * FROM proposals WHERE id = ?", (proposal_id,)).fetchone()

    return proposal_row_to_response(dict(row))


@router.get("/api/proposals/{proposal_id}", response_model=ProposalResponse)
def get_proposal(proposal_id: str) -> ProposalResponse:
    """Get a proposal by ID."""
    with get_db() as conn:
        row = conn.execute("SELECT * FROM proposals WHERE id = ?", (proposal_id,)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Proposal not found")
    return proposal_row_to_response(dict(row))


@router.post("/api/proposals/{proposal_id}/approve", response_model=ProposalResponse)
def approve_proposal(proposal_id: str) -> ProposalResponse:
    """Mark a proposal as approved."""
    now = datetime.utcnow().isoformat()

    with get_db() as conn:
        row = conn.execute("SELECT * FROM proposals WHERE id = ?", (proposal_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Proposal not found")

        conn.execute(
            "UPDATE proposals SET status = ?, approved_at = ? WHERE id = ?",
            (ProposalStatus.APPROVED.value, now, proposal_id),
        )

        # Track event
        conn.execute(
            "INSERT INTO analytics_events (id, event_type, metadata, created_at) VALUES (?, ?, ?, ?)",
            (
                str(uuid4()),
                "proposal_approved",
                json.dumps({"proposal_id": proposal_id, "lead_id": row["lead_id"]}),
                now,
            ),
        )

        updated = conn.execute("SELECT * FROM proposals WHERE id = ?", (proposal_id,)).fetchone()

    return proposal_row_to_response(dict(updated))
