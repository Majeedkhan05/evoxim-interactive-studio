from __future__ import annotations

import json
from datetime import datetime
from enum import Enum
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class ExperienceType(str, Enum):
    team_program = "team_program"
    one_time_event = "one_time_event"
    unsure = "unsure"


class Language(str, Enum):
    en = "en"
    fr = "fr"


class LeadStatus(str, Enum):
    NEW = "NEW"
    QUALIFIED = "QUALIFIED"
    PROPOSAL_DRAFT = "PROPOSAL_DRAFT"
    PROPOSAL_SENT = "PROPOSAL_SENT"
    MEETING_REQUESTED = "MEETING_REQUESTED"
    WON = "WON"
    LOST = "LOST"


class ProposalStatus(str, Enum):
    DRAFT = "DRAFT"
    APPROVED = "APPROVED"
    SENT = "SENT"


class FitLevel(str, Enum):
    strong = "strong"
    moderate = "moderate"
    exploratory = "exploratory"


class Confidence(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"


# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------

class DiscoverySession(BaseModel):
    team_size: int = Field(..., ge=1, description="Number of people in the team")
    organization: str = Field(..., min_length=1, description="Company or organization name")
    team_context: str = Field(default="", description="Brief context about the team")
    objectives: list[str] = Field(default_factory=list, description="Selected objectives")
    situation_description: str = Field(default="", description="Free-text situation description")
    experience_type: ExperienceType = Field(default=ExperienceType.unsure)
    language: Language = Field(default=Language.en)
    duration_preference: str = Field(default="", description="short, long-term, or empty")


# ---------------------------------------------------------------------------
# Leads
# ---------------------------------------------------------------------------

class LeadCreate(BaseModel):
    name: str = Field(..., min_length=1)
    company: str = Field(..., min_length=1)
    email: str = Field(..., min_length=1)
    phone: Optional[str] = None
    discovery: DiscoverySession


class LeadResponse(BaseModel):
    id: UUID
    name: str
    company: str
    email: str
    phone: Optional[str]
    team_size: Optional[int]
    language: str
    status: LeadStatus
    recommended_service: Optional[str]
    created_at: datetime
    updated_at: datetime


class LeadDetail(LeadResponse):
    objectives: Optional[list[str]]
    context: Optional[str]
    discovery_answers: Optional[dict[str, Any]]
    ai_summary: Optional[str]
    ai_brief: Optional[str]


class LeadStatusUpdate(BaseModel):
    status: LeadStatus


# ---------------------------------------------------------------------------
# Recommendation
# ---------------------------------------------------------------------------

class RecommendationResponse(BaseModel):
    recommended_service: str
    fit_level: FitLevel
    reasoning: list[str]
    objectives: list[str]
    suggested_mechanics: list[str]
    facilitation_notes: list[str]
    client_summary: str
    confidence: Confidence


# ---------------------------------------------------------------------------
# Proposals
# ---------------------------------------------------------------------------

class ProposalCreate(BaseModel):
    language: Language = Language.en


class ProposalResponse(BaseModel):
    id: UUID
    lead_id: UUID
    version: int
    content: dict[str, Any]
    status: ProposalStatus
    language: str
    created_at: datetime
    approved_at: Optional[datetime]
    sent_at: Optional[datetime]


# ---------------------------------------------------------------------------
# Feedback
# ---------------------------------------------------------------------------

class FeedbackCreate(BaseModel):
    original_recommendation: str
    override_recommendation: str
    reason: str = ""


class FeedbackResponse(BaseModel):
    id: UUID
    lead_id: UUID
    original_recommendation: str
    override_recommendation: str
    reason: str
    created_at: datetime


# ---------------------------------------------------------------------------
# Analytics
# ---------------------------------------------------------------------------

class AnalyticsEvent(BaseModel):
    event_type: str = Field(..., min_length=1)
    metadata: dict[str, Any] = Field(default_factory=dict)


class AnalyticsResponse(BaseModel):
    total_leads: int
    leads_by_status: dict[str, int]
    recommendations_count: dict[str, int]
    proposals_generated: int
    proposals_approved: int
    proposals_sent: int
    conversion_rate: float
    recent_events: list[dict[str, Any]]


# ---------------------------------------------------------------------------
# Helpers for DB row parsing
# ---------------------------------------------------------------------------

def _parse_json(value: str | None) -> Any:
    if value is None:
        return None
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return value


def lead_row_to_response(row: dict) -> LeadResponse:
    return LeadResponse(
        id=row["id"],
        name=row["name"],
        company=row["company"],
        email=row["email"],
        phone=row["phone"],
        team_size=row["team_size"],
        language=row["language"],
        status=row["status"],
        recommended_service=row["recommended_service"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
    )


def lead_row_to_detail(row: dict) -> LeadDetail:
    return LeadDetail(
        id=row["id"],
        name=row["name"],
        company=row["company"],
        email=row["email"],
        phone=row["phone"],
        team_size=row["team_size"],
        language=row["language"],
        status=row["status"],
        recommended_service=row["recommended_service"],
        objectives=_parse_json(row["objectives"]),
        context=row["context"],
        discovery_answers=_parse_json(row["discovery_answers"]),
        ai_summary=row["ai_summary"],
        ai_brief=row["ai_brief"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
    )


def proposal_row_to_response(row: dict) -> ProposalResponse:
    return ProposalResponse(
        id=row["id"],
        lead_id=row["lead_id"],
        version=row["version"],
        content=_parse_json(row["content"]) or {},
        status=row["status"],
        language=row["language"],
        created_at=row["created_at"],
        approved_at=row["approved_at"],
        sent_at=row["sent_at"],
    )
