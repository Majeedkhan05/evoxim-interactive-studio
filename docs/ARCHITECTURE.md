# Evoxim AI Experience Platform -- Architecture

> Evoxim -- Collective Communication is a Montreal-based facilitation company
> (founder: Maxime Dufour) that transforms how teams communicate through their
> "Creative Formula" methodology. This platform digitizes the prospect discovery
> and proposal workflow so facilitators can focus on what they do best: running
> workshops.

---

## 1. System Overview

```
                         Internet
                            |
              +-------------+--------------+
              |                            |
     /index.html (cinematic)      /platform (Next.js)
              |                            |
              |            +---------------+---------------+
              |            |               |               |
              |       /discover       /admin           /api/*
              |     (prospect UX)   (dashboard)    (Next.js Route
              |                                     Handlers)
              |                                        |
              |                              +---------+---------+
              |                              |                   |
              |                      Recommendation         FastAPI
              |                        Engine              /backend
              |                     (deterministic)            |
              |                                           SQLite (dev)
              |                                       PostgreSQL + pgvector
              |                                          (production)
              +--------------------------------------------+
```

### Repositories / Directories

| Path | Role | Stack |
|------|------|-------|
| `/index.html` | Cinematic prototype -- brand showcase, preserved as-is | Vanilla HTML/CSS/JS |
| `/platform` | Production application -- discovery flow, admin, API | Next.js 15, TypeScript, Tailwind CSS 4 |
| `/backend` | Python API server -- recommendation engine, data layer | FastAPI, Pydantic, SQLite |
| `/docs` | This documentation | Markdown |

---

## 2. Frontend: Next.js 15

### Stack

| Dependency | Version | Purpose |
|------------|---------|---------|
| Next.js | 16.3.2 | App Router, Server Components, Route Handlers |
| React | 19.2.8 | UI rendering |
| TypeScript | 5.x | Type safety |
| Tailwind CSS | 4.x | Utility-first styling |
| Framer Motion | 13.x | Cinematic animations in the discovery flow |
| jsPDF | 4.x | Client-side PDF proposal generation |
| Lucide React | 1.x | Icon system |
| clsx | 2.x | Conditional class names |

### Directory Structure (planned)

```
platform/src/
  app/
    layout.tsx               # Root layout, font loading, i18n provider
    page.tsx                 # Landing / entry point
    [lang]/
      discover/
        page.tsx             # 6-step discovery flow
      summary/
        page.tsx             # Personalized recommendation summary
      contact/
        page.tsx             # Lead capture form
    admin/
      layout.tsx             # Admin shell (sidebar, auth gate)
      page.tsx               # Dashboard overview
      leads/
        page.tsx             # Lead list with filters
        [id]/page.tsx        # Single lead detail
      proposals/
        page.tsx             # Proposal list
        [id]/page.tsx        # Proposal editor + PDF preview
  components/
    discovery/               # Step components for the interactive flow
    admin/                   # Dashboard widgets, tables, charts
    ui/                      # Shared primitives (Button, Card, Modal)
    proposal/                # PDF template components
  lib/
    types.ts                 # Shared TypeScript types (exists)
    api.ts                   # Fetch wrappers for backend endpoints
    recommendation.ts        # Client-side deterministic engine (mirror)
    i18n/
      en.ts                  # English dictionary
      fr.ts                  # French dictionary
      index.ts               # Dictionary resolver
    pdf/
      generate-proposal.ts   # jsPDF proposal builder
```

### Internationalization (i18n)

The platform supports English and French via static dictionaries -- not runtime
translation. Each dictionary is a deeply nested object of the same shape. The
active language is determined by URL segment (`/en/discover`, `/fr/discover`)
and stored in a React context. All user-facing strings reference the dictionary;
no hardcoded English appears in components.

This approach was chosen because:
- Evoxim operates in Montreal (bilingual market)
- Workshop facilitators review every string for brand voice
- Runtime translation (e.g., Google Translate API) would compromise tone quality
- Static dictionaries are zero-latency and auditable

---

## 3. Backend: FastAPI

### Stack

| Dependency | Version | Purpose |
|------------|---------|---------|
| FastAPI | 0.115.6 | API framework |
| Uvicorn | 0.34.0 | ASGI server |
| Pydantic | 2.10.4 | Request/response validation |
| python-dotenv | 1.0.1 | Environment configuration |
| Jinja2 | 3.1.5 | Server-side template rendering (future proposals) |
| python-multipart | 0.0.20 | Form data parsing |

### Directory Structure

```
backend/
  app/
    __init__.py
    database.py              # SQLite connection, schema DDL, migrations
    api/
      __init__.py            # Route definitions (to be implemented)
    models/
      __init__.py            # Pydantic models (to be implemented)
    services/
      __init__.py            # Business logic (to be implemented)
    knowledge/
      __init__.py            # Evoxim service catalog, rules (to be implemented)
  requirements.txt
  .env.example
```

### Configuration

Environment variables (see `.env.example`):

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite:///./evoxim.db` | Database connection string |
| `LLM_API_KEY` | -- | API key for LLM provider (P2, not used in MVP) |
| `LLM_MODEL` | `claude-sonnet-4-20250514` | Model identifier |
| `LLM_PROVIDER` | `anthropic` | LLM provider name |
| `HOST` | `0.0.0.0` | Server bind address |
| `PORT` | `8000` | Server port |
| `DEBUG` | `true` | Debug mode |
| `CORS_ORIGINS` | `http://localhost:3000,...` | Allowed CORS origins |
| `DEFAULT_LANGUAGE` | `en` | Fallback language |
| `COMPANY_EMAIL` | `info@evoxim.com` | Footer / proposal contact |

---

## 4. Database

### Development: SQLite

SQLite with WAL mode and foreign keys enabled. Single-file database at
`backend/evoxim.db`. Suitable for local development and early beta testing
(single-server deployment).

### Production: PostgreSQL + pgvector

For production deployment:
- PostgreSQL for reliability, concurrent access, and backup tooling
- pgvector extension for future semantic search over workshop descriptions
  and recommendation embeddings (P2 RAG feature)

### Schema

```sql
-- Core lead tracking
CREATE TABLE leads (
    id              TEXT PRIMARY KEY,
    name            TEXT NOT NULL,
    company         TEXT NOT NULL,
    email           TEXT NOT NULL,
    phone           TEXT,
    team_size       INTEGER,
    language        TEXT DEFAULT 'en',
    status          TEXT DEFAULT 'NEW',
    recommended_service TEXT,
    objectives      TEXT,          -- JSON array of ObjectiveId
    context         TEXT,
    discovery_answers TEXT,        -- JSON blob of full DiscoveryData
    ai_summary      TEXT,
    ai_brief        TEXT,
    created_at      TEXT NOT NULL,
    updated_at      TEXT NOT NULL
);

-- Proposals generated for leads
CREATE TABLE proposals (
    id          TEXT PRIMARY KEY,
    lead_id     TEXT NOT NULL REFERENCES leads(id) ON DELETE CASCADE,
    version     INTEGER DEFAULT 1,
    content     TEXT,             -- JSON blob of ProposalContent
    status      TEXT DEFAULT 'DRAFT',
    language    TEXT DEFAULT 'en',
    created_at  TEXT NOT NULL,
    approved_at TEXT,
    sent_at     TEXT
);

-- Admin feedback on recommendations (training data for AI)
CREATE TABLE feedback (
    id                      TEXT PRIMARY KEY,
    lead_id                 TEXT NOT NULL REFERENCES leads(id) ON DELETE CASCADE,
    original_recommendation TEXT,
    override_recommendation TEXT,
    reason                  TEXT,
    created_at              TEXT NOT NULL
);

-- Analytics event log
CREATE TABLE analytics_events (
    id          TEXT PRIMARY KEY,
    event_type  TEXT NOT NULL,
    metadata    TEXT,             -- JSON blob
    created_at  TEXT NOT NULL
);
```

### Indexes

| Index | Table | Column(s) | Purpose |
|-------|-------|-----------|---------|
| `idx_leads_status` | leads | status | Filter leads by pipeline stage |
| `idx_leads_email` | leads | email | Duplicate detection |
| `idx_proposals_lead_id` | proposals | lead_id | Fetch proposals for a lead |
| `idx_feedback_lead_id` | feedback | lead_id | Fetch feedback for a lead |
| `idx_analytics_event_type` | analytics_events | event_type | Filter by event type |
| `idx_analytics_created_at` | analytics_events | created_at | Time-range queries |

### Lead Status Machine

```
NEW --> QUALIFIED --> PROPOSAL_DRAFT --> PROPOSAL_SENT --> MEETING_REQUESTED --> WON
  \                                                                        \--> LOST
   \----------------------------------------------------------------------> LOST
```

---

## 5. AI / Recommendation Engine

### Phase 1 (MVP): Deterministic Engine

A rule-based engine that maps discovery inputs to Evoxim services. No LLM
calls, no network latency, no hallucination risk.

**Input:** `DiscoveryData` (team size, objectives, experience type, context)

**Output:** `Recommendation` (service ID, fit level, reasoning, mechanics, confidence)

**Service Catalog:**

| Service ID | Name | Best For |
|------------|------|----------|
| `exploration_discovery` | Exploration & Discovery Program | Teams wanting to explore communication fundamentals over multiple sessions |
| `integration_autonomy` | Integration & Autonomy Program | Teams ready for deeper, sustained communication transformation |
| `event_exploration` | Exploration Event | One-time events focused on discovery and engagement |
| `event_integration` | Integration Event | One-time events for deeper team integration |

**Decision Logic:**

1. `experienceType == 'one_time_event'` --> Event services
2. `experienceType == 'team_program'` --> Program services
3. `teamSize < 20` + introductory objectives --> Exploration
4. `teamSize >= 20` + advanced objectives --> Integration
5. `experienceType == 'unsure'` --> Engine picks based on objectives and context

**Confidence Calibration:**

| Level | Criteria |
|-------|----------|
| `high` | All required fields populated, clear objective match, unambiguous experience type |
| `medium` | Most fields populated, objectives span categories, or `experienceType == 'unsure'` |
| `low` | Sparse inputs, conflicting signals, very large or very small team size |

**Mechanics Selection:**

| Mechanic ID | Name | Description |
|-------------|------|-------------|
| `micro_game` | Micro Game | Quick 2-5 minute energizers |
| `small_game` | Small Game | 10-20 minute structured activities |
| `big_game` | Big Game | 30-60 minute immersive experiences |
| `macro_game` | Macro Game | Full-session collaborative challenges |
| `flashes` | Flashes | Spontaneous micro-interventions |

### Phase 2 (P2): RAG with LLM

- Embed Evoxim's workshop descriptions, case studies, and facilitator notes
- Use pgvector for semantic retrieval
- Pass retrieved context + discovery data to Claude as structured prompt
- Validate LLM output against the same Pydantic schema
- Human-in-the-loop: admin reviews before any recommendation goes to client

---

## 6. PDF Generation

### MVP: Client-Side (jsPDF)

PDF proposals are generated entirely in the browser using jsPDF. This keeps the
MVP simple (no server-side rendering dependencies) and lets the admin preview
in real time before downloading.

**Template Structure:**
1. Cover page with Evoxim branding
2. Client context summary (from discovery data)
3. Recommended approach (service, reasoning)
4. Experience structure (duration, frequency, format)
5. Selected mechanics with descriptions
6. Objectives alignment
7. Next steps
8. Evoxim contact information

### Future: Server-Side Generation

Architecture is prepared for server-side PDF generation via Jinja2 templates
rendered to HTML, then converted to PDF. This enables:
- Consistent rendering across browsers
- Batch generation
- Email attachment workflows
- Version-controlled templates

---

## 7. Authentication

### MVP: Cookie-Based Admin Session

Simple cookie-based authentication for the admin dashboard. A single admin
password is set via environment variable. No user registration, no roles.
Sufficient for a single-facilitator operation during beta.

### Production: Supabase Auth

- Email/password and magic link authentication
- Role-based access (admin, facilitator, viewer)
- Row-level security on PostgreSQL
- JWT tokens with refresh rotation

---

## 8. Data Flow

```
                    PROSPECT JOURNEY
                    ================

[1] Visitor lands on discovery page
         |
[2] 6-step interactive flow collects:
    - Organization name
    - Team size
    - Team context / situation
    - Communication objectives (multi-select)
    - Situation description (free text)
    - Experience type preference
         |
[3] Recommendation Engine processes DiscoveryData
    - Deterministic rules match service
    - Confidence level calculated
    - Reasoning chain generated
    - Mechanics selected
         |
[4] Personalized summary displayed
    - Recommended service with explanation
    - "Why this fits your team"
    - Suggested workshop mechanics
    - Facilitator notes
         |
[5] Contact form captures lead info
    - Name, company, email, phone
    - Combined with DiscoveryData + Recommendation
         |
[6] Lead created in database (status: NEW)
    - Analytics event logged
         |
         v

                    ADMIN WORKFLOW
                    ==============

[7] Admin dashboard shows new lead
    - Discovery answers visible
    - AI recommendation displayed
    - Confidence indicator
         |
[8] Admin reviews and qualifies (status: QUALIFIED)
    - Can override recommendation
    - Override logged to feedback table
         |
[9] Admin generates proposal (status: PROPOSAL_DRAFT)
    - Pre-populated from recommendation
    - Editable before PDF generation
    - Client-side PDF preview
         |
[10] Admin approves and sends (status: PROPOSAL_SENT)
     - PDF downloaded or emailed (future)
         |
[11] Follow-up tracking
     - MEETING_REQUESTED / WON / LOST
     - Analytics aggregation
```

---

## 9. API Endpoints

All endpoints are prefixed with `/api` and served by Next.js Route Handlers
(forwarding to FastAPI where needed).

### Discovery

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/discovery/recommend` | Submit DiscoveryData, receive Recommendation |
| `GET` | `/api/discovery/services` | List available Evoxim services |
| `GET` | `/api/discovery/objectives` | List selectable objectives with labels |
| `GET` | `/api/discovery/mechanics` | List game mechanics with descriptions |

### Leads

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/leads` | Create a new lead (DiscoveryData + ContactData) |
| `GET` | `/api/leads` | List leads (filterable by status, date, language) |
| `GET` | `/api/leads/:id` | Get single lead with full details |
| `PATCH` | `/api/leads/:id` | Update lead status or fields |
| `DELETE` | `/api/leads/:id` | Soft-delete a lead |
| `POST` | `/api/leads/:id/brief` | Generate AI brief for a lead |

### Proposals

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/proposals` | Create proposal for a lead |
| `GET` | `/api/proposals` | List proposals (filterable by status, lead) |
| `GET` | `/api/proposals/:id` | Get single proposal with content |
| `PATCH` | `/api/proposals/:id` | Update proposal content or status |
| `POST` | `/api/proposals/:id/approve` | Mark proposal as approved |
| `POST` | `/api/proposals/:id/send` | Mark proposal as sent |

### Analytics

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/analytics/events` | Log an analytics event |
| `GET` | `/api/analytics/summary` | Aggregated metrics (leads by status, conversion rate) |
| `GET` | `/api/analytics/funnel` | Discovery-to-proposal funnel metrics |
| `GET` | `/api/analytics/timeline` | Leads over time |

### Feedback

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/feedback` | Log recommendation override |
| `GET` | `/api/feedback` | List all feedback entries |
| `GET` | `/api/feedback/accuracy` | Recommendation accuracy report |

### Health

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/health` | Server health check |
| `GET` | `/api/health/db` | Database connectivity check |

---

## 10. Deployment Architecture

### Development

```
localhost:3000  -->  Next.js dev server (platform/)
localhost:8000  -->  Uvicorn dev server (backend/)
evoxim.db       -->  SQLite file (backend/)
```

### Production (planned)

```
Vercel          -->  Next.js frontend + API routes
Railway/Render  -->  FastAPI backend
Supabase        -->  PostgreSQL + pgvector + Auth
Resend          -->  Transactional email (P2)
Vercel Blob     -->  PDF storage (P2)
```

---

## 11. Key Type Definitions

All shared types are defined in `/platform/src/lib/types.ts` and mirrored as
Pydantic models in the backend. See that file for the canonical definitions of:

- `Language` -- `'en' | 'fr'`
- `ExperienceType` -- `'team_program' | 'one_time_event' | 'unsure'`
- `FitLevel` -- `'strong' | 'moderate' | 'exploratory'`
- `Confidence` -- `'high' | 'medium' | 'low'`
- `LeadStatus` -- 7-state pipeline enum
- `ServiceId` -- 4 Evoxim service identifiers
- `ObjectiveId` -- 8 communication objectives
- `MechanicId` -- 5 Creative Formula game mechanics
- `DiscoveryData` -- Prospect discovery flow input
- `ContactData` -- Lead contact information
- `Recommendation` -- Engine output
- `Lead` -- Full lead record
- `Proposal` -- Proposal metadata
- `ProposalContent` -- Structured proposal body
