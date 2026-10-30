"""
Proposal generator for Evoxim.

Takes lead data + recommendation and produces a structured proposal document
as JSON that the frontend can render and optionally convert to PDF.
"""

from __future__ import annotations

import os
from datetime import datetime, timedelta

from app.models.schemas import RecommendationResponse
from app.services.knowledge import (
    MECHANICS,
    OBJECTIVES,
    SERVICES,
    get_benefits_by_keys,
)

COMPANY_EMAIL = os.getenv("COMPANY_EMAIL", "info@evoxim.com")
COMPANY_PHONE = os.getenv("COMPANY_PHONE", "+1-514-000-0000")
COMPANY_WEBSITE = os.getenv("COMPANY_WEBSITE", "https://evoxim.com")


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _section_client_info(lead: dict, lang: str) -> dict:
    title = "Information client" if lang == "fr" else "Client Information"
    return {
        "title": title,
        "type": "client_info",
        "data": {
            "name": lead["name"],
            "company": lead["company"],
            "email": lead["email"],
            "phone": lead.get("phone", ""),
            "team_size": lead.get("team_size"),
        },
    }


def _section_stated_needs(lead: dict, recommendation: RecommendationResponse, lang: str) -> dict:
    if lang == "fr":
        title = "Besoins exprimes"
        intro = "Lors de votre decouverte, vous avez identifie les objectifs suivants:"
    else:
        title = "Stated Needs"
        intro = "During your discovery, you identified the following objectives:"

    return {
        "title": title,
        "type": "stated_needs",
        "data": {
            "introduction": intro,
            "objectives": recommendation.objectives,
            "context": lead.get("context", ""),
        },
    }


def _section_recommended_approach(recommendation: RecommendationResponse, lang: str) -> dict:
    svc_key = recommendation.recommended_service
    svc = SERVICES.get(svc_key, {}).get(lang, {})

    if lang == "fr":
        title = "Approche recommandee"
    else:
        title = "Recommended Approach"

    return {
        "title": title,
        "type": "recommended_approach",
        "data": {
            "service_name": svc.get("name", svc_key),
            "tagline": svc.get("tagline", ""),
            "description": svc.get("description", ""),
            "duration": svc.get("duration", ""),
            "format": svc.get("format", ""),
            "fit_level": recommendation.fit_level.value,
            "confidence": recommendation.confidence.value,
        },
    }


def _section_why_it_fits(recommendation: RecommendationResponse, lang: str) -> dict:
    title = "Pourquoi cette approche" if lang == "fr" else "Why This Approach"
    return {
        "title": title,
        "type": "why_it_fits",
        "data": {
            "reasoning": recommendation.reasoning,
            "client_summary": recommendation.client_summary,
        },
    }


def _section_experience_structure(recommendation: RecommendationResponse, lang: str) -> dict:
    svc_key = recommendation.recommended_service
    svc = SERVICES.get(svc_key, {}).get(lang, {})

    if lang == "fr":
        title = "Structure de l'experience"
    else:
        title = "Experience Structure"

    outcomes = svc.get("outcomes", [])

    return {
        "title": title,
        "type": "experience_structure",
        "data": {
            "duration": svc.get("duration", ""),
            "ideal_for": svc.get("ideal_for", ""),
            "outcomes": outcomes,
        },
    }


def _section_mechanics(recommendation: RecommendationResponse, lang: str) -> dict:
    title = "Mecaniques de jeu" if lang == "fr" else "Game Mechanics"
    mechanics_data = []
    for name in recommendation.suggested_mechanics:
        for key, mech in MECHANICS.items():
            if mech[lang]["name"] == name:
                mechanics_data.append({
                    "name": mech[lang]["name"],
                    "description": mech[lang]["description"],
                    "duration": mech[lang]["duration"],
                })
                break

    return {
        "title": title,
        "type": "mechanics",
        "data": {"mechanics": mechanics_data},
    }


def _section_objectives(recommendation: RecommendationResponse, lang: str) -> dict:
    title = "Objectifs vises" if lang == "fr" else "Target Objectives"
    objectives_data = []
    for obj_name in recommendation.objectives:
        for key, obj in OBJECTIVES.items():
            if obj[lang]["name"] == obj_name:
                objectives_data.append({
                    "name": obj[lang]["name"],
                    "description": obj[lang]["description"],
                })
                break

    return {
        "title": title,
        "type": "objectives",
        "data": {"objectives": objectives_data},
    }


def _section_next_steps(lang: str) -> dict:
    if lang == "fr":
        return {
            "title": "Prochaines etapes",
            "type": "next_steps",
            "data": {
                "steps": [
                    "Planifier un appel decouverte de 30 minutes pour approfondir vos besoins",
                    "Personnaliser le programme selon votre contexte d'equipe",
                    "Confirmer les dates et la logistique",
                    "Lancer l'experience avec votre equipe",
                ],
                "cta": "Planifier un appel",
                "validity": "Cette proposition est valide pour 30 jours.",
            },
        }
    return {
        "title": "Next Steps",
        "type": "next_steps",
        "data": {
            "steps": [
                "Schedule a 30-minute discovery call to deepen our understanding of your needs",
                "Customize the program to your team's specific context",
                "Confirm dates and logistics",
                "Launch the experience with your team",
            ],
            "cta": "Schedule a Call",
            "validity": "This proposal is valid for 30 days.",
        },
    }


def _section_contact(lang: str) -> dict:
    if lang == "fr":
        title = "Coordonnees"
        org_desc = "Communication Collective"
    else:
        title = "Contact Information"
        org_desc = "Collective Communication"

    return {
        "title": title,
        "type": "contact",
        "data": {
            "company": "Evoxim",
            "description": org_desc,
            "founder": "Maxime Dufour",
            "location": "Montreal, QC",
            "email": COMPANY_EMAIL,
            "phone": COMPANY_PHONE,
            "website": COMPANY_WEBSITE,
        },
    }


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def generate_proposal(
    lead: dict,
    recommendation: RecommendationResponse,
    lang: str = "en",
) -> dict:
    """
    Generate a complete structured proposal.

    Returns a JSON-serializable dict with metadata and ordered sections
    that the frontend can render as a document or convert to PDF.
    """
    now = datetime.utcnow()
    svc = SERVICES.get(recommendation.recommended_service, {}).get(lang, {})

    proposal = {
        "metadata": {
            "generated_at": now.isoformat(),
            "valid_until": (now + timedelta(days=30)).isoformat(),
            "language": lang,
            "version": 1,
            "service_key": recommendation.recommended_service,
            "service_name": svc.get("name", recommendation.recommended_service),
        },
        "header": {
            "title": "Proposition" if lang == "fr" else "Proposal",
            "subtitle": svc.get("tagline", ""),
            "company": "Evoxim",
            "client": lead["company"],
            "date": now.strftime("%Y-%m-%d"),
        },
        "sections": [
            _section_client_info(lead, lang),
            _section_stated_needs(lead, recommendation, lang),
            _section_recommended_approach(recommendation, lang),
            _section_why_it_fits(recommendation, lang),
            _section_experience_structure(recommendation, lang),
            _section_mechanics(recommendation, lang),
            _section_objectives(recommendation, lang),
            _section_next_steps(lang),
            _section_contact(lang),
        ],
    }

    return proposal
