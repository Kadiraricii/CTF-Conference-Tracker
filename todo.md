# 🛡️ CyberTracker Roadmap & Task List

Welcome to the **CyberTracker** development hub. This document tracks our progress from a simple scraper to a full-scale **SecOps Intelligence Platform**.

---

## ⚡ Current Sprint: "Operation Neon"
*Goal: Enhance user engagement and AI precision.*

### 🛠️ Core & Security
- [ ] **Auth Layer**: Implement JWT-based authentication for private event tracking.
- [ ] **RBAC**: Add different permission levels for staff and regular users.
- [ ] **Audit Logs**: Track all scraper activity and AI modifications in the DB.

### 🤖 Intelligence & AI
- [x] **AI Tagging**: Automated category assignment (Pwn, Web, Crypto).
- [ ] **Deep Analysis**: Use LLMs to summarize long conference descriptions.
- [ ] **Anomaly Detection**: Flag potentially fake or suspicious event listings.
- [ ] **RSS+**: Add 5+ new sources (OWASP, SANS, InfoSec Conferences).

### 🎨 Frontend (The Cyber UI)
- [x] **Glassmorphism**: Modern look with frosted glass effects.
- [x] **TR/EN Switch**: Instant localizations.
- [ ] **Interactive Map**: Visualize conferences around the globe.
- [ ] **Dark/Light**: Fine-tune the "High-Contrast" mode for accessibility.
- [ ] **Mobile App**: Convert the web app to a PWA for on-the-go alerts.

### 📢 Communication
- [x] **Telegram Bot**: Real-time push notifications.
- [ ] **Discord Integration**: Dedicated channel for new CTF releases.
- [ ] **Calendar**: One-click "Add to Google/Outlook Calendar" buttons.

---

## ✅ Completed Milestones
- [x] **V1.0.0 Launch**: Core FastAPI & Docker architecture.
- [x] **CTFtime Integration**: Automated ingestion of global CTFs.
- [x] **Dynamic Dashboard**: Responsive UI with Tailwind and Alpine.js.
- [x] **Self-Healing**: Automated system checks and health reporting.

---

## 🛠️ Tech Stack Evolution
| Module | Current | Future |
| :--- | :--- | :--- |
| **Backend** | FastAPI / Python | High-speed Go Microservices? |
| **Database** | PostgreSQL | Vector DB for AI Embeddings |
| **Cache** | Redis | Redis Streams for Real-time |
| **Frontend** | Vanilla + Alpine | Next.js (if complexity grows) |

---

> [!TIP]
> Use `python manage.py check` to verify system health before starting new tasks.

> [!IMPORTANT]
> Always contribute via Feature Branches: `git checkout -b feature/your-task`

---

*“Stay ahead of the threat, one event at a time.”* 🚀
