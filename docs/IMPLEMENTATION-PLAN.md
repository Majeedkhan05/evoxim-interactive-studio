# Evoxim AI Experience Platform -- Implementation Plan

> Prioritized roadmap from MVP to full platform. Each phase builds on the
> previous one. Features within a phase are ordered by implementation sequence.

---

## Priority Framework

| Priority | Definition | Timebox |
|----------|-----------|---------|
| **P0** | MVP -- the minimum viable product for beta testing | 4-6 weeks |
| **P1** | Post-MVP -- features added once P0 is stable and validated | 2-4 weeks |
| **P2** | Future -- strategic capabilities requiring new infrastructure | Ongoing |

---

## P0: MVP (Current Sprint)

### 1. Prospect Discovery Experience

**Goal:** An interactive 6-step flow that replaces the current intake call with
a self-service digital experience.

**Steps:**

| Step | Screen | Collects | UI Pattern |
|------|--------|----------|------------|
| 1 | Welcome | Language preference (EN/FR) | Two large buttons, cinematic background |
| 2 | Organization | Organization name, team size | Text input + number stepper |
| 3 | Context | Team context, current situation | Textarea with character guidance |
| 4 | Objectives | Communication objectives | Multi-select cards (max 3) |
| 5 | Situation | Detailed description | Rich textarea with prompts |
| 6 | Experience Type | Program vs. event vs. unsure | Three illustrated cards |

**Implementation Details:**
- Each step is a client component with Framer Motion transitions
- Progress indicator shows step position
- Back navigation preserves answers
- State held in React context (not URL params) to prevent manipulation
- Mobile-first responsive layout
- All strings from i18n dictionary

**Files to create:**
- `platform/src/app/[lang]/discover/page.tsx`
- `platform/src/components/discovery/DiscoveryFlow.tsx`
- `platform/src/components/discovery/steps/WelcomeStep.tsx`
- `platform/src/components/discovery/steps/OrganizationStep.tsx`
- `platform/src/components/discovery/steps/ContextStep.tsx`
- `platform/src/components/discovery/steps/ObjectivesStep.tsx`
- `platform/src/components/discovery/steps/SituationStep.tsx`
- `platform/src/components/discovery/steps/ExperienceTypeStep.tsx`
- `platform/src/components/discovery/ProgressBar.tsx`
- `platform/src/lib/discovery-context.tsx`

---

### 2. Deterministic Recommendation Engine

**Goal:** Transform discovery answers into a personalized Evoxim service
recommendation without any LLM dependency.

**Algorithm:**

```
function recommend(data: DiscoveryData): Recommendation {
  1. Determine service category:
     - one_time_event --> event services
     - team_program   --> program services
     - unsure         --> infer from objectives + team size

  2. Select specific service:
     - Introductory objectives + smaller teams --> exploration variant
     - Advanced objectives + larger teams     --> integration variant

  3. Calculate fit level:
     - strong:      clear match, aligned objectives
     - moderate:    partial match, some objectives span categories
     - exploratory: unclear signals, recommend conversation

  4. Generate reasoning chain:
     - 3-5 bullet points explaining why this service fits
     - Reference specific objectives the client selected

  5. Select mechanics:
     - Map objectives to appropriate game mechanics
     - Consider team size for mechanic suitability

  6. Set confidence:
     - high:   all fields complete, unambiguous match
     - medium: some ambiguity, experienceType == 'unsure'
     - low:    sparse data, conflicting signals

  return Recommendation
}
```

**Files to create:**
- `platform/src/lib/recommendation.ts` (client-side engine)
- `backend/app/services/recommendation.py` (server-side mirror)
- `backend/app/knowledge/services.py` (Evoxim service catalog)
- `backend/app/knowledge/objectives.py` (objective-to-service mapping)
- `backend/app/knowledge/mechanics.py` (mechanic definitions and rules)

---

### 3. Personalized Experience Summary

**Goal:** Display the recommendation in a compelling, personalized way that
makes the prospect feel understood.

**Sections:**
1. "Based on what you shared..." -- brief acknowledgment of their situation
2. "We recommend..." -- service name with visual card
3. "Why this fits your team" -- reasoning bullets
4. "What the experience looks like" -- mechanics preview
5. "Ready to explore?" -- CTA to contact form

**Implementation:**
- Server Component that receives recommendation via searchParams or POST
- Animated reveal of each section (Framer Motion stagger)
- Shareable URL (recommendation encoded, not discovery data)
- Print-friendly CSS

**Files to create:**
- `platform/src/app/[lang]/summary/page.tsx`
- `platform/src/components/summary/RecommendationCard.tsx`
- `platform/src/components/summary/ReasoningList.tsx`
- `platform/src/components/summary/MechanicsPreview.tsx`
- `platform/src/components/summary/SummaryCTA.tsx`

---

### 4. Lead Creation and Storage

**Goal:** Capture prospect contact information and persist the complete
discovery-to-recommendation journey.

**Flow:**
1. Summary page has "Get Your Personalized Proposal" CTA
2. Contact form collects name, company, email, optional phone
3. On submit: create lead via `POST /api/leads`
4. Backend stores DiscoveryData + Recommendation + ContactData
5. Thank-you screen with expectation setting

**Validation:**
- Email format validation (client + server)
- Required fields: name, company, email
- Duplicate email check (warn, don't block -- same person may explore twice)

**Files to create:**
- `platform/src/app/[lang]/contact/page.tsx`
- `platform/src/components/contact/ContactForm.tsx`
- `platform/src/app/api/leads/route.ts`
- `backend/app/api/leads.py`
- `backend/app/models/lead.py`

---

### 5. Admin Dashboard

**Goal:** Give Maxime a single place to see all leads, review recommendations,
and manage the pipeline.

**Views:**

#### 5a. Overview Dashboard
- Total leads count (by status)
- Recent leads (last 7 days)
- Recommendation distribution (pie/bar chart)
- Conversion funnel snapshot

#### 5b. Leads List
- Sortable table: name, company, status, service, date, language
- Status filter pills
- Search by name/company/email
- Click to open lead detail

#### 5c. Lead Detail
- Full discovery answers
- Recommendation with confidence indicator
- Status update controls
- Override recommendation (with reason -- logged to feedback table)
- Generate proposal button
- Activity timeline

#### 5d. Proposals List
- Table: lead name, version, status, language, date
- Filter by status (DRAFT / APPROVED / SENT)

**Files to create:**
- `platform/src/app/admin/layout.tsx`
- `platform/src/app/admin/page.tsx`
- `platform/src/app/admin/leads/page.tsx`
- `platform/src/app/admin/leads/[id]/page.tsx`
- `platform/src/app/admin/proposals/page.tsx`
- `platform/src/app/admin/proposals/[id]/page.tsx`
- `platform/src/components/admin/DashboardStats.tsx`
- `platform/src/components/admin/LeadsTable.tsx`
- `platform/src/components/admin/LeadDetail.tsx`
- `platform/src/components/admin/StatusBadge.tsx`
- `platform/src/components/admin/ProposalEditor.tsx`

---

### 6. Proposal Generation (Client-Side PDF)

**Goal:** Generate professional PDF proposals pre-filled from discovery data
and recommendations, editable by admin before download.

**Workflow:**
1. Admin clicks "Generate Proposal" on lead detail
2. ProposalContent is assembled from Lead + Recommendation
3. Admin can edit any field in a form view
4. Live PDF preview renders alongside the form
5. "Download PDF" generates via jsPDF
6. Proposal record saved to database

**PDF Template Sections:**
1. Cover page -- Evoxim logo, client name, date
2. "Understanding Your Team" -- rewritten discovery context
3. "Our Recommendation" -- service description, fit explanation
4. "Experience Structure" -- duration, frequency, format
5. "Workshop Mechanics" -- selected mechanics with descriptions
6. "Aligned Objectives" -- objective checklist
7. "Next Steps" -- numbered action items
8. "About Evoxim" -- company info, contact

**Files to create:**
- `platform/src/lib/pdf/generate-proposal.ts`
- `platform/src/lib/pdf/template-sections.ts`
- `platform/src/components/proposal/ProposalPreview.tsx`
- `platform/src/components/proposal/ProposalForm.tsx`

---

### 7. EN/FR Bilingual Support

**Goal:** Every user-facing string available in English and Quebec French.

**Implementation:**
- Static dictionary objects (not JSON files -- enables TypeScript checking)
- URL-based language: `/en/discover`, `/fr/discover`
- Admin dashboard: language toggle in header (not URL-based)
- Proposals generated in the lead's language
- PDF content in the lead's language

**Dictionary Structure:**
```typescript
const en = {
  discovery: {
    welcome: { title: "...", subtitle: "...", cta: "..." },
    organization: { title: "...", label_name: "...", ... },
    // ... per step
  },
  summary: { ... },
  contact: { ... },
  admin: { ... },
  proposal: { ... },
  common: { back: "Back", next: "Next", submit: "Submit", ... },
};
```

**Files to create:**
- `platform/src/lib/i18n/en.ts`
- `platform/src/lib/i18n/fr.ts`
- `platform/src/lib/i18n/index.ts`
- `platform/src/lib/i18n/use-dictionary.ts`

---

### 8. AI-Generated Client Brief (Template-Based for MVP)

**Goal:** Generate a human-readable brief summarizing the prospect's situation
and recommended approach, suitable for sharing with facilitators.

**MVP approach:** Template-based string interpolation (no LLM).

```
Brief for {company}
===================
{name} from {company} has a team of {teamSize} people.

They are looking for help with: {objectives_as_sentence}.

Their situation: {situationDescription}

We recommend: {service_name} ({fit_level} fit)

Key reasoning:
{reasoning_bullets}

Suggested mechanics: {mechanics_list}

Facilitator notes:
{facilitation_notes}
```

**Files to create:**
- `platform/src/lib/brief-generator.ts`
- `backend/app/services/brief.py`

---

## P1: Post-MVP Enhancements

### 9. Follow-Up Reminders

**Goal:** Notify admin when a lead needs follow-up action.

**Implementation:**
- Time-based rules: "No status change in 3 days" triggers reminder
- Dashboard notification badge
- Optional browser push notifications
- Configurable reminder intervals per status

---

### 10. Proposal History and Versioning

**Goal:** Track all proposal versions for a lead.

**Implementation:**
- Each edit creates a new version (proposals.version increments)
- Version comparison view (diff highlight)
- Restore previous version
- Audit log of who changed what

---

### 11. Analytics Dashboard

**Goal:** Visualize platform performance and Evoxim's sales funnel.

**Metrics:**
- Discovery completions vs. abandonments (by step)
- Recommendation distribution (which services are recommended most)
- Lead-to-proposal conversion rate
- Average time in each pipeline stage
- Language split (EN vs. FR usage)
- Device/viewport breakdown
- Recommendation override rate (admin feedback)

**Implementation:**
- Recharts or Chart.js for visualizations
- Date range selector
- Export to CSV

---

### 12. Event Mode (QR Code Collective Pulse)

**Goal:** During live events, attendees scan a QR code and participate in a
real-time collective pulse check, displayed on the facilitator's screen.

**Implementation:**
- Admin creates an "event session" with a unique code
- QR code links to `/event/{code}`
- Attendees answer 2-3 pulse questions (mood, energy, expectation)
- Real-time aggregation displayed on a presenter view
- WebSocket or Server-Sent Events for live updates
- Results archived for post-event analysis

---

## P2: Future Platform Capabilities

### 13. Adaptive AI Discovery Questions (LLM)

**Goal:** Replace the fixed 6-step flow with dynamic follow-up questions
generated by an LLM based on previous answers.

**Requirements:**
- LLM generates the next question based on answers so far
- Maximum 8 questions (hard cap to prevent fatigue)
- Fall back to deterministic flow if LLM unavailable
- All questions validated against an approved question bank
- No off-brand or intrusive questions

---

### 14. RAG-Based Recommendations

**Goal:** Use retrieval-augmented generation to produce richer, more nuanced
recommendations grounded in Evoxim's full knowledge base.

**Requirements:**
- Embed workshop descriptions, case studies, testimonials
- pgvector for semantic similarity search
- Claude as the generation model
- Structured output validation (same Pydantic schema)
- Human-in-the-loop approval before client delivery
- Fallback to deterministic engine if RAG fails

---

### 15. Client Portal

**Goal:** Prospects and clients can log in to see their proposals, session
history, and upcoming workshops.

**Features:**
- Magic-link authentication (no password)
- View proposal PDF
- Accept/decline proposal
- Pre-workshop questionnaire
- Post-workshop feedback form
- Session history and notes

---

### 16. CRM Integrations

**Goal:** Sync leads and proposals with external CRM systems.

**Target Integrations:**
- HubSpot (most likely first)
- Salesforce
- Pipedrive
- Webhook-based custom integrations

**Implementation:**
- Outbound webhooks on lead status change
- Inbound API for CRM-initiated updates
- Field mapping configuration
- Conflict resolution (last-write-wins with audit log)

---

### 17. Email Automation (Resend)

**Goal:** Automated transactional emails at key pipeline moments.

**Emails:**

| Trigger | Recipient | Content |
|---------|-----------|---------|
| Lead created | Prospect | "Thank you, we received your information" |
| Proposal sent | Prospect | Proposal PDF attached |
| Follow-up due | Admin | Reminder with lead summary |
| Meeting booked | Both | Calendar confirmation |
| Post-workshop | Prospect | Feedback request |

**Stack:**
- Resend as the transactional email provider
- React Email for template rendering
- Unsubscribe handling

---

## Implementation Dependencies

```
P0-1: Discovery Flow
  |
P0-2: Recommendation Engine  <-- required by P0-3
  |
P0-3: Summary Page           <-- required by P0-4
  |
P0-4: Lead Creation          <-- required by P0-5
  |
P0-5: Admin Dashboard        <-- required by P0-6
  |
P0-6: Proposal Generation
  |
P0-7: EN/FR (parallel with all above)
  |
P0-8: Client Brief (parallel with P0-5, P0-6)

P1-9 through P1-12: independent of each other, all depend on P0

P2-13: depends on P0-1 (replaces discovery flow)
P2-14: depends on P0-2 (replaces recommendation engine)
P2-15: depends on P0-4 + Supabase Auth
P2-16: depends on P0-4
P2-17: depends on P0-4 + P0-6
```

---

## Definition of Done (per feature)

- [ ] Feature works in both EN and FR
- [ ] Mobile viewport tested (375px width)
- [ ] Tablet viewport tested (768px width)
- [ ] Desktop viewport tested (1280px width)
- [ ] Loading and error states handled
- [ ] TypeScript strict mode -- no `any` types
- [ ] Accessibility: keyboard navigation, screen reader labels
- [ ] Data persisted correctly to database
- [ ] API endpoint validates input (Pydantic/Zod)
- [ ] No console errors or warnings
