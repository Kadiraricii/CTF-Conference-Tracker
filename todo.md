# 🛡️ CyberTracker Tasks & Backlog

> **Status:** 🟢 Active Development | **Sprint:** "Operation Neon" (Q1 2026)  
> **Repository Health:** ![Lines of Code](https://img.shields.io/badge/LOC-Ok-green) ![Tests](https://img.shields.io/badge/Tests-Passing-success)

---

## 📊 Sprint Progress
**Overall Completion:**
`[██████████░░░░░░] 62%`

| Module | Status | Priority |
| :--- | :--- | :--- |
| **🔍 Intelligence** | `[████████░░]` 80% | 🔥 **Critical** |
| **🎨 User Interface** | `[██████░░░░]` 60% | ⭐ **High** |
| **🔐 Cybersecurity** | `[██░░░░░░░░]` 20% | 🛡️ **Medium** |
| **📡 Telemetry** | `[████░░░░░░]` 40% | ☁️ **Low** |

---

## 🚀 Active Tasks (To-Do)

### � Intelligence & AI Layer
*Focus: Enhancing data richness and autonomy.*
- [ ] ![Priority: High](https://img.shields.io/badge/-High-red) **Deep Summarization (LLM)**  
  Integrate Llama/GPT-4 to rewrite complex event descriptions into 1-line "executive summaries".
- [ ] ![Priority: Med](https://img.shields.io/badge/-Medium-yellow) **Anomaly Detection Logic**  
  Implement heuristic checks to flag "Capture The Flag" events with suspicious URLs or descriptions.
- [ ] ![Priority: Med](https://img.shields.io/badge/-Medium-yellow) **RSS Source Expansion**  
  Add `OWASP` and `SANS` feed parsers to `src/app/workers/scrapers/`.

### 🎨 The Cyber Dashboard
*Focus: Visual impact and user retention.*
- [ ] ![Priority: High](https://img.shields.io/badge/-High-red) **Interactive World Map**  
  Visualize incoming conference data on a WebGL 3D globe (Three.js/D3.js).
- [ ] ![Priority: Low](https://img.shields.io/badge/-Low-blue) **"Hacker Mode" Theme**  
  Create a secondary retro-terminal theme (Green/Black monospace) togglable in settings.
- [ ] ![Priority: Med](https://img.shields.io/badge/-Medium-yellow) **Mobile-First Refactor**  
  Optimize grid layouts for iPhone/Android viewports (Touch targets > 44px).

### �️ Security & Access Control
*Focus: Protecting user data.*
- [ ] ![Priority: Critical](https://img.shields.io/badge/-Critical-cf000f) **JWT Authentication Flow**  
  Implement `OAuth2` with Bearer tokens for API endpoints.
- [ ] ![Priority: Critical](https://img.shields.io/badge/-Critical-cf000f) **Rate Limiting (Redis)**  
  Protect Scraper endpoints from abuse (Max 10 req/min).

---

## ✅ Accomplished (Done)

<details>
<summary><strong>📂 Click to view completed tasks</strong></summary>

### Core Infrastructure
- [x] **Project Skeleton**: FastAPI + Docker Compose setup.
- [x] **Database Design**: PostgreSQL schema with Alembic migrations.
- [x] **Self-Healing Checks**: `manage.py self-check` implementation.

### Intelligence
- [x] **CTFtime Integration**: Full data ingestion from CTFtime public API.
- [x] **Smart Tagging**: Keyword-based automatic categorization.

### Frontend
- [x] **Glassmorphism UI**: Tailwind implementation of blur and translucency.
- [x] **TR/EN Localization**: i18n support for UI text.
- [x] **Animation Engine**: CSS Pulse and transitions for live events.

### Notifications
- [x] **Telegram Bot**: `aiogram` based push notification service.

</details>

---

## 🐞 Bugs & Fixes
- [ ] **Fix:** Scraper fails when RSS feed encoding is non-UTF-8.
- [ ] **Fix:** "Load More" button sometimes duplicates events on the dashboard.

---

> [!TIP]
> **Contributors:** Please pick tasks tagged with ![Good First Issue](https://img.shields.io/badge/-Good_First_Issue-7057ff) if you are new to the codebase.

> [!IMPORTANT]
> All new features must pass `pytest` and include type hints (`mypy` compliant).

---

*Last Refreshed: January 21, 2026*
