"""
Evoxim knowledge base — structured data for the Creative Formula methodology.

All content is bilingual (EN / FR).  Keys in each dict are service / mechanic /
benefit / objective identifiers used by the recommendation and proposal engines.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Services
# ---------------------------------------------------------------------------

SERVICES: dict[str, dict] = {
    "exploration_discovery": {
        "key": "exploration_discovery",
        "en": {
            "name": "Exploration & Discovery",
            "tagline": "Build a strong foundation through guided team exploration",
            "description": (
                "A 4-hour immersive program spread over one month that uses the "
                "Creative Formula to help teams explore their dynamics, discover "
                "strengths, and build foundational habits of collective communication."
            ),
            "duration": "4 hours over 1 month",
            "format": "Team program",
            "ideal_for": "Teams beginning their journey toward better collaboration",
            "outcomes": [
                "Improved team awareness and listening",
                "Foundation of psychological safety",
                "Shared language for collaboration",
                "Initial habits of collective creativity",
            ],
        },
        "fr": {
            "name": "Exploration & Decouverte",
            "tagline": "Batir une base solide par l'exploration guidee en equipe",
            "description": (
                "Un programme immersif de 4 heures reparti sur un mois qui utilise "
                "la Formule Creative pour aider les equipes a explorer leur dynamique, "
                "decouvrir leurs forces et batir des habitudes fondamentales de "
                "communication collective."
            ),
            "duration": "4 heures sur 1 mois",
            "format": "Programme d'equipe",
            "ideal_for": "Les equipes qui commencent leur parcours vers une meilleure collaboration",
            "outcomes": [
                "Amelioration de la conscience d'equipe et de l'ecoute",
                "Fondation de securite psychologique",
                "Langage partage pour la collaboration",
                "Habitudes initiales de creativite collective",
            ],
        },
    },
    "integration_autonomy": {
        "key": "integration_autonomy",
        "en": {
            "name": "Integration & Autonomy",
            "tagline": "Embed lasting habits of collective communication",
            "description": (
                "A 12-hour deep-dive program over three months designed to integrate "
                "the Creative Formula into daily team life, building autonomy in "
                "facilitation and sustainable communication habits."
            ),
            "duration": "12 hours over 3 months",
            "format": "Team program",
            "ideal_for": "Teams ready to commit to long-term transformation",
            "outcomes": [
                "Deep-rooted communication habits",
                "Internal facilitation capability",
                "Autonomous team dynamics",
                "Sustained collective creativity and engagement",
            ],
        },
        "fr": {
            "name": "Integration & Autonomie",
            "tagline": "Ancrer des habitudes durables de communication collective",
            "description": (
                "Un programme approfondi de 12 heures sur trois mois concu pour "
                "integrer la Formule Creative dans la vie quotidienne de l'equipe, "
                "developper l'autonomie en facilitation et des habitudes de "
                "communication durables."
            ),
            "duration": "12 heures sur 3 mois",
            "format": "Programme d'equipe",
            "ideal_for": "Les equipes pretes a s'engager dans une transformation a long terme",
            "outcomes": [
                "Habitudes de communication profondement ancrees",
                "Capacite de facilitation interne",
                "Dynamiques d'equipe autonomes",
                "Creativite collective et engagement durables",
            ],
        },
    },
    "event_exploration": {
        "key": "event_exploration",
        "en": {
            "name": "Event Formula — Exploration",
            "tagline": "A single powerful event to ignite team energy",
            "description": (
                "A one-time facilitated event using the Creative Formula, designed "
                "for smaller groups seeking an energizing, exploratory experience "
                "that sparks new ways of communicating and collaborating."
            ),
            "duration": "Half-day or full-day",
            "format": "One-time event",
            "ideal_for": "Small to medium groups, team off-sites, retreats",
            "outcomes": [
                "Burst of team energy and cohesion",
                "New perspectives on collaboration",
                "Memorable shared experience",
                "Immediate improvement in group dynamics",
            ],
        },
        "fr": {
            "name": "Formule Evenement — Exploration",
            "tagline": "Un evenement puissant pour allumer l'energie d'equipe",
            "description": (
                "Un evenement facilite unique utilisant la Formule Creative, concu "
                "pour les petits groupes cherchant une experience energisante et "
                "exploratoire qui suscite de nouvelles facons de communiquer."
            ),
            "duration": "Demi-journee ou journee complete",
            "format": "Evenement ponctuel",
            "ideal_for": "Petits et moyens groupes, journees hors-site, retraites",
            "outcomes": [
                "Eclat d'energie et de cohesion d'equipe",
                "Nouvelles perspectives sur la collaboration",
                "Experience partagee memorable",
                "Amelioration immediate de la dynamique de groupe",
            ],
        },
    },
    "event_integration": {
        "key": "event_integration",
        "en": {
            "name": "Event Formula — Integration",
            "tagline": "Large-scale events that create lasting impact",
            "description": (
                "A high-impact facilitated event for larger groups or corporate "
                "gatherings, integrating the Creative Formula into conferences, "
                "summits, or organization-wide events for maximum engagement."
            ),
            "duration": "Half-day to multi-day",
            "format": "One-time event",
            "ideal_for": "Large groups, conferences, corporate events, summits",
            "outcomes": [
                "Organization-wide engagement",
                "Cross-team connection and cohesion",
                "Scalable facilitation impact",
                "Shared organizational language",
            ],
        },
        "fr": {
            "name": "Formule Evenement — Integration",
            "tagline": "Des evenements a grande echelle qui creent un impact durable",
            "description": (
                "Un evenement facilite a fort impact pour les grands groupes ou "
                "rassemblements corporatifs, integrant la Formule Creative dans "
                "des conferences, sommets ou evenements a l'echelle de l'organisation."
            ),
            "duration": "Demi-journee a plusieurs jours",
            "format": "Evenement ponctuel",
            "ideal_for": "Grands groupes, conferences, evenements corporatifs, sommets",
            "outcomes": [
                "Engagement a l'echelle de l'organisation",
                "Connexion et cohesion inter-equipes",
                "Impact de facilitation extensible",
                "Langage organisationnel partage",
            ],
        },
    },
}


# ---------------------------------------------------------------------------
# Game mechanics
# ---------------------------------------------------------------------------

MECHANICS: dict[str, dict] = {
    "micro_game": {
        "key": "micro_game",
        "en": {
            "name": "Micro Game",
            "description": "Quick 2-5 minute activities that shift energy and build micro-habits of listening and participation.",
            "duration": "2-5 minutes",
            "group_size": "Any",
            "best_for": ["meetings", "warm-ups", "energy shifts"],
        },
        "fr": {
            "name": "Micro Jeu",
            "description": "Activites rapides de 2 a 5 minutes qui changent l'energie et construisent des micro-habitudes d'ecoute et de participation.",
            "duration": "2-5 minutes",
            "group_size": "Tous",
            "best_for": ["reunions", "echauffements", "changements d'energie"],
        },
    },
    "small_game": {
        "key": "small_game",
        "en": {
            "name": "Small Game",
            "description": "10-20 minute structured activities that deepen team connection and practice collective creativity.",
            "duration": "10-20 minutes",
            "group_size": "4-15 people",
            "best_for": ["team building", "skill practice", "creative warm-ups"],
        },
        "fr": {
            "name": "Petit Jeu",
            "description": "Activites structurees de 10 a 20 minutes qui approfondissent la connexion d'equipe et pratiquent la creativite collective.",
            "duration": "10-20 minutes",
            "group_size": "4-15 personnes",
            "best_for": ["consolidation d'equipe", "pratique de competences", "echauffements creatifs"],
        },
    },
    "big_game": {
        "key": "big_game",
        "en": {
            "name": "Big Game",
            "description": "30-60 minute immersive experiences that challenge teams to collaborate, create, and communicate at a deeper level.",
            "duration": "30-60 minutes",
            "group_size": "8-30 people",
            "best_for": ["workshops", "off-sites", "deep exploration"],
        },
        "fr": {
            "name": "Grand Jeu",
            "description": "Experiences immersives de 30 a 60 minutes qui mettent les equipes au defi de collaborer, creer et communiquer a un niveau plus profond.",
            "duration": "30-60 minutes",
            "group_size": "8-30 personnes",
            "best_for": ["ateliers", "hors-sites", "exploration approfondie"],
        },
    },
    "macro_game": {
        "key": "macro_game",
        "en": {
            "name": "Macro Game",
            "description": "Full-session experiences (1-3 hours) that create transformative team moments through extended creative collaboration.",
            "duration": "1-3 hours",
            "group_size": "10-50+ people",
            "best_for": ["summits", "conferences", "transformative events"],
        },
        "fr": {
            "name": "Macro Jeu",
            "description": "Experiences de session complete (1 a 3 heures) qui creent des moments d'equipe transformateurs par une collaboration creative prolongee.",
            "duration": "1-3 heures",
            "group_size": "10-50+ personnes",
            "best_for": ["sommets", "conferences", "evenements transformateurs"],
        },
    },
    "flashes": {
        "key": "flashes",
        "en": {
            "name": "Flashes",
            "description": "Spontaneous micro-moments of creative engagement that can be sprinkled throughout any meeting or event.",
            "duration": "30 seconds - 2 minutes",
            "group_size": "Any",
            "best_for": ["energy resets", "transitions", "engagement boosts"],
        },
        "fr": {
            "name": "Flashes",
            "description": "Micro-moments spontanes d'engagement creatif qui peuvent etre parsemes dans toute reunion ou evenement.",
            "duration": "30 secondes - 2 minutes",
            "group_size": "Tous",
            "best_for": ["resets d'energie", "transitions", "boosts d'engagement"],
        },
    },
}


# ---------------------------------------------------------------------------
# Benefits
# ---------------------------------------------------------------------------

BENEFITS: dict[str, dict] = {
    "cohesion": {
        "en": {"name": "Team Cohesion", "description": "Stronger bonds and shared identity within the team."},
        "fr": {"name": "Cohesion d'equipe", "description": "Liens plus forts et identite partagee au sein de l'equipe."},
    },
    "listening": {
        "en": {"name": "Active Listening", "description": "Deeper attention and presence in conversations."},
        "fr": {"name": "Ecoute Active", "description": "Attention et presence plus profondes dans les conversations."},
    },
    "communication": {
        "en": {"name": "Communication", "description": "Clearer, more effective exchange of ideas."},
        "fr": {"name": "Communication", "description": "Echange d'idees plus clair et plus efficace."},
    },
    "leadership": {
        "en": {"name": "Leadership", "description": "Shared leadership and distributed facilitation skills."},
        "fr": {"name": "Leadership", "description": "Leadership partage et competences de facilitation distribuees."},
    },
    "confidence": {
        "en": {"name": "Confidence", "description": "Greater willingness to contribute and take creative risks."},
        "fr": {"name": "Confiance", "description": "Plus grande volonte de contribuer et de prendre des risques creatifs."},
    },
    "energy": {
        "en": {"name": "Energy", "description": "Renewed enthusiasm and engagement in collective work."},
        "fr": {"name": "Energie", "description": "Enthousiasme et engagement renouveles dans le travail collectif."},
    },
    "well_being": {
        "en": {"name": "Well-being", "description": "Improved psychological safety and workplace satisfaction."},
        "fr": {"name": "Bien-etre", "description": "Amelioration de la securite psychologique et de la satisfaction au travail."},
    },
    "efficiency": {
        "en": {"name": "Efficiency", "description": "More productive meetings and collaborative sessions."},
        "fr": {"name": "Efficacite", "description": "Reunions et sessions collaboratives plus productives."},
    },
    "creativity": {
        "en": {"name": "Creativity", "description": "Unlocked collective imagination and innovative thinking."},
        "fr": {"name": "Creativite", "description": "Imagination collective liberee et pensee innovante."},
    },
}


# ---------------------------------------------------------------------------
# Objectives
# ---------------------------------------------------------------------------

OBJECTIVES: dict[str, dict] = {
    "clearer_meetings": {
        "en": {"name": "Clearer Meetings", "description": "Run meetings where everyone contributes and outcomes are clear."},
        "fr": {"name": "Reunions plus claires", "description": "Animer des reunions ou chacun contribue et les resultats sont clairs."},
    },
    "active_listening": {
        "en": {"name": "Active Listening", "description": "Develop a culture of deep listening across the team."},
        "fr": {"name": "Ecoute active", "description": "Developper une culture d'ecoute profonde dans l'equipe."},
    },
    "communication": {
        "en": {"name": "Better Communication", "description": "Improve how ideas, feedback, and needs are shared."},
        "fr": {"name": "Meilleure communication", "description": "Ameliorer la facon dont les idees, les retours et les besoins sont partages."},
    },
    "participation": {
        "en": {"name": "Greater Participation", "description": "Increase engagement and voice from every team member."},
        "fr": {"name": "Plus grande participation", "description": "Augmenter l'engagement et la voix de chaque membre de l'equipe."},
    },
    "collective_creativity": {
        "en": {"name": "Collective Creativity", "description": "Unlock the team's creative potential through structured play."},
        "fr": {"name": "Creativite collective", "description": "Liberer le potentiel creatif de l'equipe par le jeu structure."},
    },
    "collaboration": {
        "en": {"name": "Stronger Collaboration", "description": "Break silos and build habits of cross-functional teamwork."},
        "fr": {"name": "Collaboration renforcee", "description": "Briser les silos et batir des habitudes de travail interfonctionnel."},
    },
    "psychological_safety": {
        "en": {"name": "Psychological Safety", "description": "Create an environment where people feel safe to speak up and take risks."},
        "fr": {"name": "Securite psychologique", "description": "Creer un environnement ou les gens se sentent en securite pour s'exprimer et prendre des risques."},
    },
    "navigating_tensions": {
        "en": {"name": "Navigating Tensions", "description": "Develop capacity to address and work through team tensions constructively."},
        "fr": {"name": "Naviguer les tensions", "description": "Developper la capacite a aborder et traverser les tensions d'equipe de maniere constructive."},
    },
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_service(key: str, lang: str = "en") -> dict | None:
    svc = SERVICES.get(key)
    if svc is None:
        return None
    return {**svc[lang], "key": key}


def get_mechanic(key: str, lang: str = "en") -> dict | None:
    mech = MECHANICS.get(key)
    if mech is None:
        return None
    return {**mech[lang], "key": key}


def get_all_services(lang: str = "en") -> list[dict]:
    return [get_service(k, lang) for k in SERVICES]


def get_all_mechanics(lang: str = "en") -> list[dict]:
    return [get_mechanic(k, lang) for k in MECHANICS]


def get_objectives_by_keys(keys: list[str], lang: str = "en") -> list[dict]:
    result = []
    for k in keys:
        obj = OBJECTIVES.get(k)
        if obj:
            result.append({**obj[lang], "key": k})
    return result


def get_benefits_by_keys(keys: list[str], lang: str = "en") -> list[dict]:
    result = []
    for k in keys:
        ben = BENEFITS.get(k)
        if ben:
            result.append({**ben[lang], "key": k})
    return result
