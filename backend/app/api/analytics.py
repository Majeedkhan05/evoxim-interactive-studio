"""Analytics routes."""

from __future__ import annotations

import json
from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, Query

from app.database import LEAD_STATUSES, get_db
from app.models.schemas import AnalyticsEvent, AnalyticsResponse

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.get("", response_model=AnalyticsResponse)
def get_analytics(recent_limit: int = Query(default=20, ge=1, le=100)) -> AnalyticsResponse:
    """Return dashboard metrics."""
    with get_db() as conn:
        # Total leads
        total = conn.execute("SELECT COUNT(*) as c FROM leads").fetchone()["c"]

        # Leads by status
        status_rows = conn.execute(
            "SELECT status, COUNT(*) as c FROM leads GROUP BY status"
        ).fetchall()
        leads_by_status = {r["status"]: r["c"] for r in status_rows}
        # Fill in missing statuses
        for s in LEAD_STATUSES:
            leads_by_status.setdefault(s, 0)

        # Recommendations count
        rec_rows = conn.execute(
            "SELECT recommended_service, COUNT(*) as c FROM leads "
            "WHERE recommended_service IS NOT NULL GROUP BY recommended_service"
        ).fetchall()
        recommendations_count = {r["recommended_service"]: r["c"] for r in rec_rows}

        # Proposal stats
        proposals_generated = conn.execute("SELECT COUNT(*) as c FROM proposals").fetchone()["c"]
        proposals_approved = conn.execute(
            "SELECT COUNT(*) as c FROM proposals WHERE status = 'APPROVED'"
        ).fetchone()["c"]
        proposals_sent = conn.execute(
            "SELECT COUNT(*) as c FROM proposals WHERE status = 'SENT'"
        ).fetchone()["c"]

        # Conversion rate (WON / total leads)
        won = leads_by_status.get("WON", 0)
        conversion_rate = round(won / total, 4) if total > 0 else 0.0

        # Recent events
        event_rows = conn.execute(
            "SELECT * FROM analytics_events ORDER BY created_at DESC LIMIT ?",
            (recent_limit,),
        ).fetchall()
        recent_events = []
        for e in event_rows:
            ed = dict(e)
            ed["metadata"] = json.loads(ed["metadata"]) if ed["metadata"] else {}
            recent_events.append(ed)

    return AnalyticsResponse(
        total_leads=total,
        leads_by_status=leads_by_status,
        recommendations_count=recommendations_count,
        proposals_generated=proposals_generated,
        proposals_approved=proposals_approved,
        proposals_sent=proposals_sent,
        conversion_rate=conversion_rate,
        recent_events=recent_events,
    )


@router.post("/event", status_code=201)
def track_event(payload: AnalyticsEvent) -> dict:
    """Track a custom analytics event."""
    event_id = str(uuid4())
    now = datetime.utcnow().isoformat()

    with get_db() as conn:
        conn.execute(
            "INSERT INTO analytics_events (id, event_type, metadata, created_at) VALUES (?, ?, ?, ?)",
            (event_id, payload.event_type, json.dumps(payload.metadata), now),
        )

    return {"id": event_id, "event_type": payload.event_type, "created_at": now}
