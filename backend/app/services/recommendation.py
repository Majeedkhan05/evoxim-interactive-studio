"""
Deterministic recommendation engine for Evoxim services.

Uses rule-based logic to match prospects to the right service offering.
Structured so an LLM layer can be added later without changing the interface.
"""

from __future__ import annotations

from app.models.schemas import (
    Confidence,
    DiscoverySession,
    ExperienceType,
    FitLevel,
    RecommendationResponse,
)
from app.services.knowledge import MECHANICS, OBJECTIVES, SERVICES


# ---------------------------------------------------------------------------
# Objective-to-mechanic mapping
# ---------------------------------------------------------------------------

OBJECTIVE_MECHANIC_MAP: dict[str, list[str]] = {
    "clearer_meetings": ["micro_game", "flashes"],
    "active_listening": ["micro_game", "small_game"],
    "communication": ["small_game", "big_game"],
    "participation": ["micro_game", "small_game", "flashes"],
    "collective_creativity": ["big_game", "macro_game"],
    "collaboration": ["small_game", "big_game"],
    "psychological_safety": ["micro_game", "small_game"],
    "navigating_tensions": ["small_game", "big_game"],
}

# ---------------------------------------------------------------------------
# Objective-to-benefit mapping
# ---------------------------------------------------------------------------

OBJECTIVE_BENEFIT_MAP: dict[str, list[str]] = {
    "clearer_meetings": ["efficiency", "communication"],
    "active_listening": ["listening", "cohesion"],
    "communication": ["communication", "confidence"],
    "participation": ["energy", "confidence"],
    "collective_creativity": ["creativity", "energy"],
    "collaboration": ["cohesion", "efficiency"],
    "psychological_safety": ["well_being", "confidence"],
    "navigating_tensions": ["leadership", "communication"],
}


def _is_long_term(session: DiscoverySession) -> bool:
    """Check whether the prospect is looking for long-term / habit-building."""
    long_keywords = {"long", "long-term", "habit", "habits", "autonomy", "durable", "autonomie"}
    text = f"{session.duration_preference} {session.situation_description} {session.team_context}".lower()
    return any(kw in text for kw in long_keywords)


def _is_large_group(session: DiscoverySession) -> bool:
    return session.team_size > 30


def _determine_service(session: DiscoverySession) -> str:
    """Apply deterministic rules to select the best service."""
    exp = session.experience_type

    if exp == ExperienceType.team_program:
        if _is_long_term(session):
            return "integration_autonomy"
        return "exploration_discovery"

    if exp == ExperienceType.one_time_event:
        if _is_large_group(session):
            return "event_integration"
        return "event_exploration"

    # ExperienceType.unsure — infer from signals
    if _is_long_term(session):
        return "integration_autonomy"
    if _is_large_group(session):
        return "event_integration"
    if session.team_size <= 15:
        return "event_exploration"
    return "exploration_discovery"


def _determine_fit(session: DiscoverySession, service_key: str) -> FitLevel:
    """Assess how well the recommended service fits the prospect."""
    score = 0

    # Explicit experience type match
    if session.experience_type == ExperienceType.team_program and service_key in (
        "exploration_discovery",
        "integration_autonomy",
    ):
        score += 2
    elif session.experience_type == ExperienceType.one_time_event and service_key in (
        "event_exploration",
        "event_integration",
    ):
        score += 2
    elif session.experience_type == ExperienceType.unsure:
        score += 1

    # Objectives alignment
    if session.objectives:
        score += 1

    # Team size sanity
    if service_key in ("exploration_discovery", "integration_autonomy") and 4 <= session.team_size <= 25:
        score += 1
    elif service_key == "event_exploration" and session.team_size <= 30:
        score += 1
    elif service_key == "event_integration" and session.team_size > 20:
        score += 1

    if score >= 4:
        return FitLevel.strong
    if score >= 2:
        return FitLevel.moderate
    return FitLevel.exploratory


def _determine_confidence(session: DiscoverySession) -> Confidence:
    """Confidence based on how much information was provided."""
    info_count = 0
    if session.experience_type != ExperienceType.unsure:
        info_count += 1
    if session.objectives:
        info_count += 1
    if session.situation_description.strip():
        info_count += 1
    if session.duration_preference.strip():
        info_count += 1
    if session.team_context.strip():
        info_count += 1

    if info_count >= 4:
        return Confidence.high
    if info_count >= 2:
        return Confidence.medium
    return Confidence.low


def _collect_mechanics(objectives: list[str]) -> list[str]:
    """Collect unique mechanics suggested by the objectives."""
    seen: set[str] = set()
    result: list[str] = []
    for obj in objectives:
        for mech in OBJECTIVE_MECHANIC_MAP.get(obj, []):
            if mech not in seen:
                seen.add(mech)
                result.append(mech)
    if not result:
        result = ["micro_game", "small_game"]
    return result


def _build_reasoning(
    session: DiscoverySession, service_key: str, lang: str = "en"
) -> list[str]:
    """Build a list of human-readable reasoning statements."""
    svc = SERVICES[service_key][lang]
    reasons: list[str] = []

    if lang == "fr":
        reasons.append(f"Avec une equipe de {session.team_size} personnes, {svc['name']} est bien adapte.")
        if session.experience_type != ExperienceType.unsure:
            type_label = "programme d'equipe" if session.experience_type == ExperienceType.team_program else "evenement ponctuel"
            reasons.append(f"Vous cherchez un {type_label}, ce qui correspond a cette offre.")
        if session.objectives:
            obj_names = [OBJECTIVES.get(o, {}).get("fr", {}).get("name", o) for o in session.objectives]
            reasons.append(f"Vos objectifs ({', '.join(obj_names)}) s'alignent bien avec cette approche.")
        if _is_long_term(session):
            reasons.append("Votre interet pour le developpement a long terme correspond au format de ce programme.")
        reasons.append(f"Format: {svc['duration']}.")
    else:
        reasons.append(f"With a team of {session.team_size}, {svc['name']} is a strong fit.")
        if session.experience_type != ExperienceType.unsure:
            type_label = "team program" if session.experience_type == ExperienceType.team_program else "one-time event"
            reasons.append(f"You're looking for a {type_label}, which aligns with this offering.")
        if session.objectives:
            obj_names = [OBJECTIVES.get(o, {}).get("en", {}).get("name", o) for o in session.objectives]
            reasons.append(f"Your objectives ({', '.join(obj_names)}) align well with this approach.")
        if _is_long_term(session):
            reasons.append("Your interest in long-term development matches this program's format.")
        reasons.append(f"Format: {svc['duration']}.")

    return reasons


def _build_facilitation_notes(
    session: DiscoverySession, service_key: str, lang: str = "en"
) -> list[str]:
    """Generate facilitation notes for the admin."""
    notes: list[str] = []

    if lang == "fr":
        if session.team_size > 20:
            notes.append("Grand groupe — prevoir des sous-groupes et une facilitation de soutien.")
        if "navigating_tensions" in session.objectives:
            notes.append("Le client mentionne des tensions — aborder avec sensibilite, etablir la securite d'abord.")
        if "psychological_safety" in session.objectives:
            notes.append("La securite psychologique est une priorite — commencer par des activites a faible risque.")
        if session.situation_description:
            notes.append(f"Contexte du client: {session.situation_description[:200]}")
        if not notes:
            notes.append("Approche standard de facilitation recommandee.")
    else:
        if session.team_size > 20:
            notes.append("Large group — plan for breakout sub-groups and support facilitation.")
        if "navigating_tensions" in session.objectives:
            notes.append("Client mentions tensions — approach with sensitivity, build safety first.")
        if "psychological_safety" in session.objectives:
            notes.append("Psychological safety is a priority — start with low-risk activities.")
        if session.situation_description:
            notes.append(f"Client context: {session.situation_description[:200]}")
        if not notes:
            notes.append("Standard facilitation approach recommended.")

    return notes


def _build_client_summary(
    session: DiscoverySession, service_key: str, lang: str = "en"
) -> str:
    """Generate a plain-language summary for the prospect."""
    svc = SERVICES[service_key][lang]

    if lang == "fr":
        return (
            f"Nous recommandons {svc['name']} pour votre equipe de "
            f"{session.team_size} personnes chez {session.organization}. "
            f"{svc['description']}"
        )
    return (
        f"We recommend {svc['name']} for your team of "
        f"{session.team_size} at {session.organization}. "
        f"{svc['description']}"
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def generate_recommendation(session: DiscoverySession) -> RecommendationResponse:
    """
    Generate a service recommendation from discovery session data.

    This is the single entry point used by the API layer.  It applies
    deterministic rules now; swap the internals for LLM calls later without
    changing the return type.
    """
    lang = session.language.value
    service_key = _determine_service(session)
    fit = _determine_fit(session, service_key)
    confidence = _determine_confidence(session)

    mechanics = _collect_mechanics(session.objectives)
    mechanic_names = [
        MECHANICS[m][lang]["name"] for m in mechanics if m in MECHANICS
    ]

    objective_names = [
        OBJECTIVES.get(o, {}).get(lang, {}).get("name", o) for o in session.objectives
    ] or [OBJECTIVES[k][lang]["name"] for k in list(OBJECTIVES)[:3]]

    return RecommendationResponse(
        recommended_service=service_key,
        fit_level=fit,
        reasoning=_build_reasoning(session, service_key, lang),
        objectives=objective_names,
        suggested_mechanics=mechanic_names,
        facilitation_notes=_build_facilitation_notes(session, service_key, lang),
        client_summary=_build_client_summary(session, service_key, lang),
        confidence=confidence,
    )
