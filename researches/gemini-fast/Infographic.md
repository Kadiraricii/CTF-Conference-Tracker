# **Product Specification: Global CTF & Conference Tracker Platform**

**Role:** Senior Cybersecurity Product Researcher  
**Date:** October 26, 2023  
**Status:** Draft / MVP Design

## **A) Sources Table (Data & Archives)**

This table prioritizes official APIs to reduce maintenance overhead and legal risk.

| Source | Type | Content | Update Freq | Auth/Rate Limit | Notes |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **CTFtime** | API | CTF schedules, weights, teams, write-ups | Daily | None (Polite) | GET /api/v1/events/. The gold standard for CTF data. |
| **InfoSec Conferences** | GitHub/JSON | Global conference dates, CFPs, locations | Weekly | None | Data stored in YAML/JSON in the infosec-conferences/infosec-conferences repo. |
| **Google Scholar / DBLP** | API/Scrape | Academic papers (USENIX, ACM CCS) | Monthly | Strict | Use for indexing academic proceedings. |
| **Official Con Sites** | HTML/RSS | Defcon, Black Hat, CCC schedules | Yearly | High Variance | Requires custom parsers per conference family. |
| **GitHub Search** | API | Write-ups (ctf-writeup topic) | Daily | OAuth Required | GET /search/repositories?q=topic:ctf-writeup. Rate limit: 5k/hr. |
| **YouTube Data API** | API | Conference talks (media archive) | Daily | API Key | Index channels: media.ccc.de, DEFCONConference, Black Hat. |

## **B) Architecture (MVP)**

**Design Philosophy:** Decoupled Ingestion. The frontend never scrapes; it only reads from the database. The "Collector" runs asynchronously.  
**Component Diagram:**  
\[External Sources\]  \<-- (HTTP/Polite) \--\>  \[Collector Engine (Python)\]  
       |                                          |  
       |                                  \[Task Queue (Redis)\]  
       |                                          |  
\[ User Clients \]    \<-- (HTTPS) \--\>       \[ API Gateway (FastAPI) \]  
       |                                          |  
    (Next.js)                             \[ PostgreSQL (Events/Users) \]

**Tech Stack Recommendation:**

* **Backend:** **Python (FastAPI)**. Strong typing (Pydantic) matches well with data validation needs, and Python dominates the OSINT/Scraping ecosystem.  
* **Database:** **PostgreSQL**. Robust handling of timezones and relational data. Use JSONB for flexible event metadata (e.g., prizes, disparate tag formats).  
* **Task Queue:** **Celery \+ Redis**. Essential for scheduling periodic scrapes and sending notifications without blocking the API.  
* **Frontend:** **Next.js (React)**. Server-side rendering (SSR) is crucial for SEO so the tracker itself ranks on Google.  
* **Hosting:** Railway or Render (easiest for full stack), or AWS/DigitalOcean (standard).

## **C) Data Model (Core Schema)**

**1\. Events Table**

* id (UUID, PK)  
* external\_id (String, unique constraints for deduplication)  
* title (String)  
* start\_time (Timestamp UTC)  
* end\_time (Timestamp UTC)  
* type (Enum: 'Jeopardy', 'Attack-Defense', 'Conference', 'Workshop')  
* is\_online (Boolean)  
* location (String, nullable)  
* weight (Float \- e.g., CTFtime points or conference tier)  
* tags (Array/JSONB \- e.g., \["web", "crypto"\])  
* metadata (JSONB \- prizes, CFP links, max\_team\_size)

**2\. Resources Table (The Archive)**

* id (UUID)  
* event\_id (FK)  
* resource\_type (Enum: 'Writeup', 'Slide', 'Video', 'Paper')  
* url (String)  
* author (String)  
* verified (Boolean \- community voting or admin approval)

**3\. Users & Subscriptions**

* id (UUID)  
* email (String)  
* preferences (JSONB \- stores filters like {"exclude\_local": true, "tags": \["pwn"\]})  
* notification\_settings (JSONB \- {"email": true, "discord\_webhook": "..."})

## **D) ETL & Scraping Strategy**

**Objective:** Robust, ethical, and idempotent data ingestion.  
**Phase 1: Ingestion (The Collector)**

1. **Orchestrator:** Celery beat triggers fetch\_ctftime\_events every 6 hours and fetch\_github\_writeups every 24 hours.  
2. **Request Layer:** Use httpx (Python) with a robust configuration:  
   * **User-Agent:** Bot/1.0 (+https://your-domain.com/bot-info; contact@your-email.com). *Transparency is key in SecOps.*  
   * **Backoff:** Implement exponential backoff (retrying 429/5xx errors).  
   * **Cache-Control:** Respect ETag/Last-Modified headers to save bandwidth.

**Phase 2: Normalization & Validation**

1. **Time Normalization:** Convert ALL incoming datetimes to **UTC** immediately. Store original timezone in metadata if needed.  
2. **Tag Mapping:** Map disparate source tags to a canonical set.  
   * *Input:* "binary-exploitation", "bin-exp", "reverse-engineering"  
   * *Canonical:* "Pwn", "Rev"  
3. **Deduplication:** Generate a deterministic hash based on (event\_name, start\_date) to detect duplicates across different sources (e.g., a CTF listed on both CTFtime and a community calendar).

**Phase 3: Storage**

* **Upsert Strategy:** Use Postgres ON CONFLICT DO UPDATE. If an event date changes, update it; otherwise, do nothing.

## **E) Calendar Integration Recommendation**

**Chosen Strategy:** **Passive Subscription (ICS Feed)**  
Direct integration (writing to a user's Google Calendar) requires complex OAuth scopes (calendar.events.rw) and security audits. An ICS feed is safer, simpler, and privacy-friendly.  
**Implementation Plan:**

1. **Library:** Use ics (Python) or icalendar.  
2. **Endpoint:** GET /api/v1/calendar/{user\_id}/events.ics  
3. **Logic:**  
   * Fetch events matching user\_id preferences.  
   * Generate a VCALENDAR object.  
   * Set X-WR-CALNAME to "My CTF Tracker".  
   * Set REFRESH-INTERVAL;VALUE=DURATION:PT12H (suggests clients update every 12h).  
4. **User Experience:** User clicks "Subscribe", gets a webcal:// URL, adds it to Google/Apple/Outlook once. The calendar stays in sync automatically.

## **F) Notification \+ Personalization Spec**

**Preference Schema (JSONB):**  
{  
  "categories": \["Web", "Crypto"\],  
  "difficulty": \["Beginner", "Intermediate"\],  
  "format": \["Jeopardy"\],  
  "alert\_triggers": {  
    "new\_event": true,  
    "start\_reminder\_24h": true,  
    "cfp\_closing\_7d": true  
  }  
}

**Notification Channels:**

1. **Discord Webhooks:** High value for CTF teams. The platform sends a POST payload to a channel URL provided by the user.  
2. **Email (Digest):** Use SendGrid or AWS SES. *Critical:* Implement "Weekly Digest" vs "Instant Alert" to prevent spam fatigue.  
3. **RSS Feeds:** Generate custom RSS feeds per user query (e.g., /rss/category/pwn).

**Anti-Spam Logic:**

* **Rate Limit:** Max 3 notifications per user per hour.  
* **Dedup:** If a "New Event" alert is sent, suppress the "24h Reminder" if the event starts tomorrow.

## **G) Security/Threat Model \+ SecOps Checklist**

**Threat Model:**

1. **SSRF (Server-Side Request Forgery):** If the scraper fetches URLs provided by users (e.g., "Add this CTF URL"), an attacker could probe internal networks.  
   * *Mitigation:* Validate all URLs against a strict allowlist of protocols (http/s) and block internal IP ranges (127.0.0.1, 10.0.0.0/8, etc.).  
2. **XSS via Scraped Content:** A malicious CTF organizer puts \<script\> tags in their event description on CTFtime.  
   * *Mitigation:* Sanitize ALL HTML on the frontend (e.g., using DOMPurify in React) and backend.  
3. **Denial of Service (DoS):** Triggering heavy export jobs (Calendar/PDF) repeatedly.  
   * *Mitigation:* Rate limiting on API endpoints (e.g., slowapi or Nginx limits).

**SecOps Checklist:**

* \[ \] **Secrets Management:** Store API keys (SendGrid, DB URLs) in environment variables (.env), never in Git.  
* \[ \] **Logging:** log structured JSON events for scraper failures (to detect layout changes) and security anomalies.  
* \[ \] **Dependency Scanning:** Use Dependabot or Snyk to catch vulnerable Python/Node libraries.  
* \[ \] **Database Backups:** Daily automated dumps to S3/Object Storage.

## **H) MVP Roadmap (4 Weeks)**

**Week 1: Core Data Pipeline**

* Set up Postgres & FastAPI.  
* Build the CTFtime collector (Ingest basic JSON).  
* Design database schema and migration scripts.  
* **Milestone:** DB populated with real data from CTFtime.

**Week 2: API & Basic Frontend**

* Build GET /events with filters (date, tag, weight).  
* Initialize Next.js project; build "Event Card" and "Grid View".  
* Implement basic Search functionality.  
* **Milestone:** A browsable read-only list of CTFs.

**Week 3: User Accounts & Personalization**

* Implement Auth (OAuth with GitHub/Google is easiest).  
* Create "Saved Events" / "Favorites" feature.  
* Build the ICS Feed generator based on favorites.  
* **Milestone:** Users can log in and subscribe to a calendar.

**Week 4: Enrichment & Polish**

* Add the Resource collector (Github write-ups).  
* Link write-ups to past events.  
* Deploy to staging (Railway/Vercel).  
* Perform security audit (SSRF check, XSS check).  
* **Milestone:** Launch MVP.

## **I) Citations & Resources**

* **CTFtime API:** [https://ctftime.org/api/](https://ctftime.org/api/)  
* **InfoSec Conferences Repo:** [https://github.com/infosec-conferences/infosec-conferences](https://www.google.com/search?q=https://github.com/infosec-conferences/infosec-conferences)  
* **iCalendar Spec (RFC 5545):** [https://tools.ietf.org/html/rfc5545](https://tools.ietf.org/html/rfc5545)  
* **OWASP SSRF Cheat Sheet:** [https://cheatsheetseries.owasp.org/cheatsheets/Server\_Side\_Request\_Forgery\_Prevention\_Cheat\_Sheet.html](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html)  
* **Celery (Task Queue):** [https://docs.celeryq.dev/en/stable/](https://docs.celeryq.dev/en/stable/)