<p align="center">
  <img src="assets/evoxim_mark.png" alt="Evoxim Logo" width="120">
</p>

<h1 align="center">Evoxim Interactive Studio</h1>

<p align="center">
  <strong>AI-powered client experience platform for collective communication</strong>
</p>

<p align="center">
  <a href="https://evoxim-interactive-studio.vercel.app">
    <img src="https://img.shields.io/badge/Live%20Demo-Visit%20Site-brightgreen?style=for-the-badge" alt="Live Demo">
  </a>
</p>

<p align="center">
  A cinematic, interactive platform that turns facilitation services into a self-service digital experience.<br>
  Built with Three.js, GSAP, WebGL, and a deterministic AI recommendation engine.
</p>

---

## Demo

https://github.com/user-attachments/assets/REPLACE-WITH-YOUR-VIDEO-ID

> **[Try it live](https://evoxim-interactive-studio.vercel.app)** — scroll through the full experience, configure a workshop, and generate a PDF proposal.

---

## What It Does

Organizations struggle with broken meeting culture — a few voices dominate while others disengage. This platform lets potential clients **configure their needs, see a live recommendation, and generate a branded PDF proposal** — all in under 60 seconds.

### How It Works

1. **Set team size** — slider from 5 to 250+ participants, auto-classifies group type
2. **Choose a formula** — Exploration, Integration, or Event formats with detailed breakdowns
3. **Select objectives** — reduce mental load, unlock collective intelligence, de-escalate tensions
4. **Describe the situation** — free text input for context
5. **Get an AI recommendation** — programme structure, game mechanics breakdown, Collective Intelligence Index
6. **Download a PDF proposal** — branded, bilingual, executive-ready

---

## Screenshots

| Hero + WebGL Particles | Interactive Configurator |
|:---:|:---:|
| ![Hero](screenshots/hero.jpg) | ![Configurator](screenshots/configurator.jpg) |

| Live Results Dashboard | Collective Intelligence Index |
|:---:|:---:|
| ![Dashboard](screenshots/dashboard.jpg) | ![CI Index](screenshots/ci-index.jpg) |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **3D Graphics** | Three.js r128, custom GLSL vertex/fragment shaders, WebGL |
| **Animation** | GSAP 3 + ScrollTrigger, CSS 3D perspective transforms |
| **Generative Art** | Canvas2D procedural generation (bloom, orbit, wave, shard, nebula) |
| **Recommendation Engine** | Deterministic rules-based matching (no external API calls) |
| **PDF Generation** | jsPDF client-side rendering with branded templates |
| **Internationalization** | Static i18n dictionary (EN/FR) with instant switching |
| **Audio** | Web Audio API for tactile interaction sounds |
| **Architecture** | Single-file HTML (~360KB, zero build dependencies) |
| **Deployment** | Vercel (static) |
| **Backend** | FastAPI (Python) — lead storage, proposals, analytics |

## Architecture

```
index.html (360KB)            <- Everything in one file
  ├── Three.js WebGL          <- 3D particle morphing system
  ├── GSAP ScrollTrigger      <- Scroll-driven animations
  ├── Canvas2D GenArt          <- Procedural background art
  ├── Configurator UI          <- Multi-step form engine
  ├── Recommendation Engine    <- Deterministic service matcher
  ├── PDF Generator            <- jsPDF branded proposals
  ├── I18N System              <- EN/FR bilingual support
  └── Web Audio                <- Tactile sound effects

backend/                       <- FastAPI REST API
  ├── leads                    <- Lead capture & storage
  ├── proposals                <- Proposal generation
  ├── analytics                <- Usage tracking
  └── recommendation           <- Server-side matching

admin.html                     <- Admin dashboard
```

## Key Features

- **Zero Build Step** — Pure HTML/CSS/JS, no webpack/vite/npm required
- **Fully Bilingual** — EN/FR toggle switches all content instantly
- **Offline-Capable** — Recommendation engine runs entirely client-side
- **PDF Export** — One-click branded executive proposals
- **Responsive** — Desktop, tablet, and mobile
- **Cinematic UX** — WebGL particles, scroll animations, generative art, spatial audio
- **Privacy-First** — All computation in the browser, no data sent to third parties

## Getting Started

```bash
# Clone the repo
git clone https://github.com/Majeedkhan05/evoxim-interactive-studio.git

# Open in browser
open index.html

# Or serve locally
python3 -m http.server 8080
```

For the backend API:
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Live Demo

**[https://evoxim-interactive-studio.vercel.app](https://evoxim-interactive-studio.vercel.app)**

---

<p align="center">
  Built by <a href="https://github.com/Majeedkhan05">Majeed Khan</a>
</p>
