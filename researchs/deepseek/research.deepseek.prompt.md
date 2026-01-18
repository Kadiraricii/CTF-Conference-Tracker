ROLE: You are a senior cybersecurity product researcher + OSINT/SecOps engineer. 
GOAL: Design a “CTF & Conference Tracker” platform that tracks global cybersecurity CTFs and conferences (e.g., Black Hat, DEFCON), filters by user interests (Web/Crypto/Pwn/etc.), sends notifications, and provides an archive of write-ups and slides.

DEEPSEARCH TASKS (must browse and cite sources with links):
1) DATA SOURCES (CTF + Conferences)
   - Find the most reliable, up-to-date sources/APIs for CTF events (start/end dates, format, platform links, tags, prizes if any).
   - Specifically check CTFtime: official API endpoints, rate limits, data fields, and terms of use.
   - For conferences (Black Hat, DEFCON, RSA, BSides, CCC, OWASP, etc.): find official event pages, schedules, CFP pages, RSS/ICS feeds if available.
   - Identify alternative sources: community calendars, event aggregators, public datasets.
   - Output: a table of sources with (Source, Type=API/RSS/HTML, Coverage, Update frequency, Auth needed, Rate limit, Legal/ToS notes).

2) SCRAPING & OSINT PIPELINE (Ethical + Robust)
   - Recommend a data ingestion strategy prioritizing official APIs, then RSS/ICS, and only then scraping.
   - For scraping: best practices (robots.txt, ToS compliance, caching, retries, backoff, user-agent, polite crawling), and anti-break strategies (selectors, structured extraction, schema validation).
   - Propose an OSINT enrichment layer: tagging events by category (Web/Crypto/Pwn/Forensics/Rev), difficulty, team size, online vs onsite, region/timezone normalization, and deduplication across sources.
   - Output: an ETL/ELT pipeline design (collector → normalizer → validator → storage → notifier) + failure modes and mitigations.

3) CALENDAR INTEGRATION (ICS / CalDAV / Google / Apple)
   - Research best ways to publish events as iCal (.ics) feeds and allow users to subscribe.
   - Compare: generating ICS feed vs direct Google Calendar API insertion vs CalDAV.
   - Include timezone/DST handling, reminders/alarms, recurring events (if any), last-modified/ETag for feed updates.
   - Output: recommended approach for MVP + “nice-to-have” integrations.

4) PERSONALIZATION & NOTIFICATIONS
   - Design a user preference model: categories (Web/Crypto/Pwn/etc.), formats (Jeopardy/Attack-Defense), online/onsite, region, date range, team size, duration.
   - Notification channels: email, push (web/mobile), Telegram/Discord, RSS digest. 
   - Suggest anti-spam rules: frequency caps, priority scoring, digest mode.
   - Output: preference schema + notification rules + scoring formula example.

5) ARCHIVE (Write-ups, Slides, Videos)
   - Identify reputable sources for past write-ups and conference materials: GitHub repos, official video channels, proceedings, community sites.
   - Propose metadata strategy: event ↔ talks ↔ speakers ↔ resources; CTF ↔ challenges ↔ write-ups.
   - Output: archive data model + acquisition plan + copyright considerations.

6) SECURITY & SECOPS (because this is a security platform)
   - Threat model: scraping infrastructure abuse, SSRF, injection via scraped content, supply-chain risks, API key leaks, account takeover.
   - SecOps plan: logging, monitoring, rate limiting, secrets management, WAF basics, abuse prevention.
   - Output: concise threat model + security controls checklist.

7) MVP SPEC + TECH STACK RECOMMENDATION
   - Propose an MVP scope that can be built fast (2–4 weeks) and scales later.
   - Recommend a pragmatic stack (example options): 
     - Backend: Python (FastAPI) or Node.js (NestJS)
     - Scraping: Playwright / Requests+BS4 / Scrapy
     - Scheduler: Celery/Redis, APScheduler, or cron + queue
     - DB: Postgres (with JSONB) + Redis cache
     - Search: Meilisearch/Elastic (optional)
     - Frontend: Next.js
   - Output: component diagram + endpoints list + minimal database schema.

OUTPUT FORMAT (strict):
A) “Sources Table” (CTF + conferences + archive)
B) “Architecture (MVP)” (bullets + diagram text)
C) “Data Model” (tables/fields)
D) “ETL & Scraping Strategy” (step-by-step)
E) “Calendar Integration Recommendation”
F) “Notification + Personalization Spec”
G) “Security/Threat Model + SecOps Checklist”
H) “MVP Roadmap (Week-by-week)” with milestones
I) Citations: provide links for every key claim (APIs, ToS, ICS specs, etc.)

CONSTRAINTS:
- Prioritize official APIs/feeds.
- Respect ToS/robots.txt and include legal/ethical notes.
- Make recommendations that are realistic for a student project but production-minded.