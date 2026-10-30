# Evoxim AI Experience Platform -- Beta Test Plan

---

## 1. Test Objectives

1. Validate that the discovery flow captures sufficient information to produce
   accurate recommendations
2. Confirm the recommendation engine maps inputs to the correct Evoxim service
   with appropriate confidence levels
3. Verify proposal generation produces professional, complete PDFs in both
   languages
4. Ensure the admin dashboard provides actionable lead management
5. Measure performance, accessibility, and usability across devices
6. Identify edge cases, confusing UX patterns, and data integrity issues
   before public launch

---

## 2. Test Personas

### Persona 1: Sarah -- HR Leader (English)

| Attribute | Value |
|-----------|-------|
| Name | Sarah Mitchell |
| Role | HR Director |
| Company | Maple Ridge Financial |
| Team size | 25 |
| Language | English |
| Context | Weekly meetings feel unproductive. Team members don't speak up. New hybrid policy has created communication gaps. |
| Objectives | `clearer_meetings`, `active_listening`, `participation` |
| Experience type | `team_program` |
| Expected recommendation | `exploration_discovery` (strong fit, high confidence) |
| Expected mechanics | `micro_game`, `small_game`, `flashes` |
| Reasoning | Mid-size team, introductory objectives focused on meeting fundamentals, wants sustained change over time. Exploration program is the right starting point. |

### Persona 2: James -- Event Director (English)

| Attribute | Value |
|-----------|-------|
| Name | James Thornton |
| Role | Director of Events |
| Company | TechNova Solutions |
| Team size | 150 |
| Language | English |
| Context | Annual company retreat. 150 attendees from 6 offices. Goal is to energize and connect people who rarely work together. One full day available. |
| Objectives | `participation`, `collective_creativity`, `collaboration` |
| Experience type | `one_time_event` |
| Expected recommendation | `event_integration` (strong fit, high confidence) |
| Expected mechanics | `big_game`, `macro_game`, `small_game` |
| Reasoning | Large group, one-time event, advanced objectives (creativity, collaboration), full day available. Integration event handles the scale and depth. |

### Persona 3: Maria -- Team Lead (English)

| Attribute | Value |
|-----------|-------|
| Name | Maria Chen |
| Role | Engineering Team Lead |
| Company | Streamline Digital |
| Team size | 12 |
| Language | English |
| Context | Small development team experiencing tension after a difficult project. Two team members aren't speaking. Need to rebuild trust and improve how conflicts are discussed. |
| Objectives | `psychological_safety`, `navigating_tensions`, `communication` |
| Experience type | `team_program` |
| Expected recommendation | `integration_autonomy` (strong fit, high confidence) |
| Expected mechanics | `small_game`, `big_game`, `flashes` |
| Reasoning | Although the team is small, the objectives are advanced (psychological safety, navigating tensions). This team needs the deeper Integration & Autonomy program, not the introductory Exploration. |

### Persona 4: Jean-Francois -- Quebec Organization (French)

| Attribute | Value |
|-----------|-------|
| Name | Jean-Francois Tremblay |
| Role | Directeur des ressources humaines |
| Company | Groupe Solidaire |
| Team size | 40 |
| Language | French |
| Context | Organisation communautaire au Quebec. 40 intervenants repartis dans 3 bureaux. Les reunions d'equipe manquent de dynamisme. Les gens veulent plus de collaboration mais ne savent pas comment. |
| Objectives | `collaboration`, `communication`, `participation` |
| Experience type | `unsure` |
| Expected recommendation | `exploration_discovery` (moderate fit, medium confidence) |
| Expected mechanics | `micro_game`, `small_game`, `big_game` |
| Reasoning | Mix of introductory and intermediate objectives. "Unsure" experience type lowers confidence. Team size (40) is medium. Engine should recommend Exploration as the entry point with moderate confidence, noting that Integration may be appropriate after an initial phase. |

### Persona 5: Victoria -- Large Corporate (English)

| Attribute | Value |
|-----------|-------|
| Name | Victoria Okafor |
| Role | Chief People Officer |
| Company | NorthStar Industries |
| Team size | 300 |
| Language | English |
| Context | Annual leadership summit for 300 directors and VPs. Two-day event at a conference center. CEO wants to transform the company's communication culture starting from the top. High-stakes, high-visibility. |
| Objectives | `collective_creativity`, `collaboration`, `psychological_safety`, `navigating_tensions` |
| Experience type | `one_time_event` |
| Expected recommendation | `event_integration` (strong fit, high confidence) |
| Expected mechanics | `macro_game`, `big_game`, `small_game` |
| Reasoning | Very large group, leadership audience, advanced objectives, event format. Integration event is the clear match. The scale and seniority of the audience call for the most immersive mechanics. |

---

## 3. Test Scenarios

### 3.1 Discovery Flow

For each persona, execute the complete discovery flow:

| # | Scenario | Steps | Expected Result |
|---|----------|-------|-----------------|
| D-1 | Complete flow (happy path) | Enter all fields per persona profile, advance through all 6 steps | Recommendation page loads with correct service |
| D-2 | Back navigation | Complete steps 1-4, go back to step 2, change team size, proceed | Recommendation reflects updated team size |
| D-3 | Minimum input | Enter only required fields, leave optional fields empty | Recommendation generated with lower confidence |
| D-4 | Maximum objectives | Select all 8 objectives | Engine handles gracefully, selects top-matching service |
| D-5 | Single objective | Select only 1 objective | Recommendation generated with appropriate reasoning |
| D-6 | Language switch mid-flow | Start in EN, switch to FR at step 3 | All subsequent steps in FR, answers preserved |
| D-7 | Very large team | Enter team size = 1000 | Engine handles gracefully, no UI overflow |
| D-8 | Very small team | Enter team size = 2 | Appropriate recommendation (possibly exploratory fit) |
| D-9 | Long text input | Enter 2000+ characters in situation description | No truncation, no UI break, stored correctly |
| D-10 | Special characters | Enter accented characters (e, a, c), apostrophes, quotes | Stored and displayed correctly |

### 3.2 Recommendation Validation

| # | Scenario | Input | Expected Output |
|---|----------|-------|-----------------|
| R-1 | Sarah (Persona 1) | See persona profile | `exploration_discovery`, strong, high |
| R-2 | James (Persona 2) | See persona profile | `event_integration`, strong, high |
| R-3 | Maria (Persona 3) | See persona profile | `integration_autonomy`, strong, high |
| R-4 | Jean-Francois (Persona 4) | See persona profile | `exploration_discovery`, moderate, medium |
| R-5 | Victoria (Persona 5) | See persona profile | `event_integration`, strong, high |
| R-6 | Conflicting signals | team_program + event-typical objectives | Engine picks best fit, confidence drops to medium |
| R-7 | All introductory objectives | `clearer_meetings`, `active_listening`, `communication` | Exploration variant |
| R-8 | All advanced objectives | `psychological_safety`, `navigating_tensions`, `collective_creativity` | Integration variant |
| R-9 | Unsure + sparse data | experienceType=unsure, 1 objective, no context | Low confidence, exploratory fit |
| R-10 | Edge: team size boundary | team_size=20 (boundary value) | Consistent assignment, no flip-flopping |

### 3.3 Proposal Generation

| # | Scenario | Steps | Expected Result |
|---|----------|-------|-----------------|
| P-1 | Generate from lead | Create lead, open admin, generate proposal | PDF preview renders all sections |
| P-2 | Edit before download | Modify recommended approach text | PDF reflects edits |
| P-3 | Download PDF | Click download | Valid PDF file, opens in reader |
| P-4 | French proposal | Lead with language=fr, generate proposal | All PDF text in French |
| P-5 | English proposal | Lead with language=en, generate proposal | All PDF text in English |
| P-6 | Long content | Lead with extensive situation description | PDF handles multi-page content |
| P-7 | Special characters in PDF | Accented characters, em dashes | Rendered correctly in PDF |
| P-8 | Multiple proposals | Generate 2 proposals for same lead | Both saved, version numbers increment |

### 3.4 Language Switching

| # | Scenario | Steps | Expected Result |
|---|----------|-------|-----------------|
| L-1 | EN discovery | Navigate to /en/discover | All text in English |
| L-2 | FR discovery | Navigate to /fr/discover | All text in Quebec French |
| L-3 | EN summary | Complete flow in EN | Summary page fully in English |
| L-4 | FR summary | Complete flow in FR | Summary page fully in French |
| L-5 | Admin EN | Toggle admin to EN | Dashboard labels in English |
| L-6 | Admin FR | Toggle admin to FR | Dashboard labels in French |
| L-7 | No missing keys | Switch language on every page | No raw dictionary keys visible |
| L-8 | French tone | Review FR strings | Natural Quebec French, not Paris French or machine translation |

### 3.5 Mobile / Tablet / Desktop

| # | Viewport | Width | Test Focus |
|---|----------|-------|------------|
| V-1 | Mobile (iPhone SE) | 375px | Touch targets >= 44px, no horizontal scroll, readable text |
| V-2 | Mobile (iPhone 14) | 390px | Discovery step cards stack vertically |
| V-3 | Tablet (iPad) | 768px | Two-column layout where appropriate |
| V-4 | Tablet landscape | 1024px | Admin sidebar visible |
| V-5 | Desktop | 1280px | Full layout, admin table not cramped |
| V-6 | Wide desktop | 1920px | Content max-width prevents line length > 80ch |

---

## 4. Functional Test Checklist

### Discovery Flow

- [ ] Step 1: Language selection loads correct dictionary
- [ ] Step 2: Organization name accepts Unicode characters
- [ ] Step 2: Team size validates as positive integer
- [ ] Step 2: Team size has reasonable bounds (1-10000)
- [ ] Step 3: Context textarea has visible character guidance
- [ ] Step 4: Objective cards are selectable (multi-select)
- [ ] Step 4: At least 1 objective required to proceed
- [ ] Step 5: Situation description is optional but encouraged
- [ ] Step 6: Experience type selection is required
- [ ] Progress bar updates correctly on each step
- [ ] Back button returns to previous step with data intact
- [ ] Forward navigation blocked until required fields filled
- [ ] Keyboard navigation works through all steps (Tab, Enter, Space)
- [ ] Screen reader announces step changes

### Recommendation Engine

- [ ] Returns valid ServiceId for all input combinations
- [ ] FitLevel is never null/undefined
- [ ] Confidence correlates with input completeness
- [ ] Reasoning array has 3-5 items
- [ ] Suggested mechanics array is non-empty
- [ ] Facilitation notes are present
- [ ] Client summary is a coherent paragraph
- [ ] No invented services (only the 4 defined ServiceIds)
- [ ] No invented objectives (only the 8 defined ObjectiveIds)
- [ ] No invented mechanics (only the 5 defined MechanicIds)

### Lead Management

- [ ] Lead creation stores all discovery data
- [ ] Lead creation stores recommendation
- [ ] Lead status defaults to NEW
- [ ] Lead list shows all leads sorted by date
- [ ] Lead list filters by status
- [ ] Lead detail shows complete discovery answers
- [ ] Lead detail shows recommendation with confidence
- [ ] Status update persists immediately
- [ ] Recommendation override logs to feedback table
- [ ] Duplicate email shows warning (not error)

### Proposal Generation

- [ ] Proposal pre-populates from lead data
- [ ] All ProposalContent fields are editable
- [ ] PDF preview updates on edit
- [ ] PDF download produces valid file
- [ ] PDF contains all 8 template sections
- [ ] PDF renders in lead's language
- [ ] Proposal version increments on re-generation
- [ ] Proposal status transitions: DRAFT -> APPROVED -> SENT

### Admin Dashboard

- [ ] Dashboard loads without authentication (MVP)
- [ ] Lead count by status is accurate
- [ ] Recent leads shows last 7 days
- [ ] Search by name/company/email works
- [ ] Navigation between views is smooth
- [ ] Empty states show helpful messages

---

## 5. EN/FR Content Quality Tests

| # | Check | Pass Criteria |
|---|-------|---------------|
| FR-1 | All discovery step titles translated | No English text visible in FR mode |
| FR-2 | All button labels translated | "Next" becomes "Suivant", etc. |
| FR-3 | All error messages translated | Validation errors appear in active language |
| FR-4 | Objective names in French | Natural, profession-appropriate French |
| FR-5 | Service names in French | Consistent with Evoxim's French branding |
| FR-6 | Proposal template in French | Complete, no English fragments |
| FR-7 | Admin labels in French | All dashboard text available in FR |
| FR-8 | Quebec French tone | Uses Quebec conventions (e.g., "courriel" not "email", "rencontre" not "meeting" where appropriate) |
| FR-9 | Accented characters render correctly | e, a, c, u, o, e all display |
| FR-10 | No machine translation artifacts | No awkward phrasing, gender agreement correct |

---

## 6. PDF-Specific Tests

| # | Test | Expected |
|---|------|----------|
| PDF-1 | File opens in macOS Preview | Renders correctly |
| PDF-2 | File opens in Chrome PDF viewer | Renders correctly |
| PDF-3 | File opens in Adobe Acrobat | Renders correctly |
| PDF-4 | File size | Under 500KB for typical proposal |
| PDF-5 | Text is selectable | Not rasterized images of text |
| PDF-6 | Accented characters | e, c, a render correctly |
| PDF-7 | Page breaks | No content cut mid-sentence |
| PDF-8 | Consistent branding | Evoxim colors, fonts throughout |
| PDF-9 | Contact info present | Email, phone, website on last page |
| PDF-10 | Long proposal | 5+ page proposal handles pagination |

---

## 7. Security Tests

| # | Test | Expected |
|---|------|----------|
| S-1 | SQL injection in name field | Input sanitized, no DB error |
| S-2 | XSS in situation description | HTML entities escaped on display |
| S-3 | CSRF on lead creation | Request rejected without valid origin |
| S-4 | Rate limiting on API | 429 after excessive requests |
| S-5 | Admin routes without auth | Redirected or blocked (production) |
| S-6 | Direct API access to leads | Requires authentication (production) |
| S-7 | Email enumeration | Lead list not accessible without auth |
| S-8 | Path traversal in lead ID | 400 error, no file system access |
| S-9 | Oversized payload | 413 error, server remains stable |
| S-10 | CORS enforcement | Only allowed origins can call API |

---

## 8. Performance Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| Largest Contentful Paint (LCP) | < 2.5 seconds | Lighthouse, on 4G throttle |
| Cumulative Layout Shift (CLS) | < 0.05 (approximately 0) | Lighthouse |
| First Input Delay (FID) | < 100ms | Lighthouse |
| Time to Interactive (TTI) | < 3.5 seconds | Lighthouse |
| Recommendation latency | < 200ms | Client-side measurement |
| Lead creation latency | < 500ms | Network tab |
| PDF generation time | < 2 seconds | Client-side measurement |
| Page weight (initial) | < 300KB transferred | Network tab |
| Lighthouse Performance score | >= 90 | Lighthouse |
| Lighthouse Accessibility score | >= 90 | Lighthouse |

---

## 9. Accessibility Checklist

| # | Requirement | Standard |
|---|------------|----------|
| A-1 | All interactive elements keyboard-accessible | WCAG 2.1 2.1.1 |
| A-2 | Visible focus indicators on all focusable elements | WCAG 2.1 2.4.7 |
| A-3 | Color contrast ratio >= 4.5:1 for normal text | WCAG 2.1 1.4.3 |
| A-4 | Color contrast ratio >= 3:1 for large text | WCAG 2.1 1.4.3 |
| A-5 | Form inputs have associated labels | WCAG 2.1 1.3.1 |
| A-6 | Error messages identify the field and the error | WCAG 2.1 3.3.1 |
| A-7 | Page has a logical heading hierarchy | WCAG 2.1 1.3.1 |
| A-8 | Images have alt text | WCAG 2.1 1.1.1 |
| A-9 | Step changes announced to screen readers | WCAG 2.1 4.1.3 |
| A-10 | Language attribute matches content language | WCAG 2.1 3.1.1 |
| A-11 | Touch targets >= 44x44 CSS pixels | WCAG 2.1 2.5.5 |
| A-12 | No content requires horizontal scrolling at 320px | WCAG 2.1 1.4.10 |
| A-13 | Animations respect prefers-reduced-motion | WCAG 2.1 2.3.3 |
| A-14 | No ARIA misuse (correct roles, states, properties) | WCAG 2.1 4.1.2 |

---

## 10. Test Execution Plan

### Phase 1: Automated (during development)

- TypeScript strict mode compilation (no `any`)
- ESLint with Next.js and accessibility rules
- Unit tests for recommendation engine (all 10 R-scenarios)
- Lighthouse CI on every PR

### Phase 2: Manual (before beta launch)

- Walk through all 5 personas end-to-end
- Test all 6 viewports
- Review all FR strings with a native Quebec French speaker
- PDF generation on 3 different PDF readers
- Security test suite

### Phase 3: Beta users (2-3 week window)

- 5-10 real prospects use the discovery flow
- Maxime reviews recommendations for accuracy
- Feedback collected on UX, language quality, and recommendation relevance
- Analytics reviewed for drop-off points
- Performance monitoring via Vercel Analytics

### Exit Criteria

The platform is ready for production when:

- [ ] All 5 persona scenarios produce correct recommendations
- [ ] All functional test checklist items pass
- [ ] Lighthouse Performance >= 90, Accessibility >= 90
- [ ] LCP < 2.5s, CLS < 0.05 on mobile
- [ ] Zero critical or high-severity bugs open
- [ ] FR content reviewed and approved by native speaker
- [ ] PDF generation works on all 3 target viewers
- [ ] Maxime has reviewed and approved 3+ real proposals
- [ ] No security vulnerabilities in OWASP top 10 categories
