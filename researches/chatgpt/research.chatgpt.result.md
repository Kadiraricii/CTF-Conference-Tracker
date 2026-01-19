# 🏁 CTF & Conference Tracker

A Python-based platform that tracks **global cybersecurity CTFs and conferences**, lets users **filter by interests**, **subscribe to calendars**, and **browse archives** (write-ups, slides, videos).

## 🎯 Goals
- Track **Jeopardy-style CTFs** and major **cybersecurity conferences** worldwide
- Personalize by **category** (Web/Crypto/Pwn/etc.), **format**, **region**, **online/onsite**
- Provide **ICS calendar feeds** and **notifications**
- Preserve **archives** (CTF write-ups, conference slides/videos)

---

## 🧱 Tech Stack (MVP)
- **Backend:** FastAPI (async, simple, robust)
- **DB:** PostgreSQL (JSONB for flexible fields)
- **Cache/Jobs:** Redis + APScheduler (or Celery)
- **Frontend:** Next.js (optional for MVP UI)
- **Calendar:** iCalendar (.ics) feeds
- **Notifications:** Email (SMTP), optional Telegram/Discord later

---

## 🔎 Data Sources (Priority: API → Feeds → HTML)
| Source | Type | Coverage | Notes |
|---|---|---|---|
| **CTFtime API (official)** | REST (JSON) | Global CTF events | Primary source; curated |
| **CTFtime Calendar** | iCal/ICS | Same events | Personal use |
| **BSides** | HTML + ICS | Global community conferences | Public calendar |
| **Black Hat (official)** | HTML | Major conferences | ICS links available |
| **DEF CON (official)** | HTML | Annual conf + media | Open media server |
| **OWASP Events** | HTML/RSS | Global AppSec events | Attribution-friendly |
| **Community Aggregators** | HTML | Broad coverage | Scrape gently |
| **Archives** | HTML/JSON/Git | Slides, videos, write-ups | Respect licenses |

> Source details compiled from the project sources document. :contentReference[oaicite:0]{index=0}

---

## 🗂️ Core Features
- **Event Calendar:** Upcoming CTFs & conferences
- **Auto Ingestion:** API + ethical scraping (robots.txt, rate limits)
- **Personalization:** Interests, regions, formats
- **Calendar Feeds:** Global + per-user filtered `.ics`
- **Archives:** CTF write-ups; conference slides/videos
- **Notifications:** Email (digest or instant)

---

## 🧠 Data Model (High Level)
- **User** → preferences (JSONB)
- **Event** → common fields (date, location, online flag, tags)
- **CTFEvent / ConfEvent** → type-specific fields
- **Writeup / Talk** → archive content linked to events

---

## 🔄 ETL Pipeline
1. **Extract:** APIs/feeds/scrapers
2. **Normalize:** Dates (UTC), locations, tags
3. **Validate:** Schema checks
4. **Deduplicate:** IDs or (name + date)
5. **Load:** Upsert into DB
6. **Cache:** Hot paths (events, ICS)

---

## 🗓️ Calendar Integration
- **ICS feeds** (global + user-specific)
- One-way, widely supported (Google/Apple/Outlook)
- Optional refresh hints (TTL)
- UTC times for simplicity (TZ support later)

---

## 🔔 Notifications
- Channels: **Email** (MVP), optional **Telegram/Discord**
- Modes: **Instant** (high relevance) or **Digest**
- Anti-spam: frequency caps, relevance scoring

---

## 🔐 Security & Ethics
- Respect **robots.txt** and ToS
- Sanitize all external content (XSS-safe)
- Secrets via env vars (no hardcoding)
- Rate limiting on APIs and logins
- Dependency audits

---

## 🛣️ 4-Week MVP Roadmap
**Week 1:** FastAPI + DB, CTFtime ingest, basic UI  
**Week 2:** Conferences ingest, preferences, global ICS  
**Week 3:** Personalization, notifications, archives  
**Week 4:** Testing, security hardening, polish

---

## 📄 License & Attribution
- Respect original licenses for write-ups/slides
- Attribute sources where required

---

## 🚀 Status
Student MVP — production-minded, zero/minimal budget, open to extension.
