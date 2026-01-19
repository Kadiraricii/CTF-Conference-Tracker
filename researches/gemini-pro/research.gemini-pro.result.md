# **Global Cybersecurity Event Tracking & Intelligence Platform: Technical Design Report**

## **1\. Executive Summary**

The cybersecurity industry operates on a rhythm defined by its events: Capture The Flag (CTF) competitions that forge practical skills, and conferences (Black Hat, DEFCON, BSides) that disseminate cutting-edge research. However, the ecosystem handling this information is fractured. Critical intelligence is siloed across disparate platforms—structured APIs like CTFtime, decentralized community calendars, static HTML schedules, and ad-hoc GitHub repositories. This fragmentation creates a significant "intelligence gap" for security professionals, researchers, and teams who require a unified operational view of the global event landscape to manage skill development and knowledge acquisition effectively.  
This report presents a comprehensive technical specification for **CyberTracker**, a centralized intelligence platform designed to aggregate, normalize, and disseminate real-time data on cybersecurity events. Unlike passive calendars, CyberTracker is designed as an active Open Source Intelligence (OSINT) engine. It leverages a modular Microservices-based Monolith (Modulith) architecture, utilizing high-concurrency Python (FastAPI) ingestion pipelines to treat event data as actionable threat intelligence.  
The architecture prioritizes ethical data acquisition, respecting the strict Terms of Service (ToS) of primary providers like CTFtime while filling the gaps they leave behind—specifically, the aggregation of historical knowledge (write-ups, slides, and videos) linked directly to the events themselves. By integrating a robust notification engine with granular personalization, the platform moves beyond simple schedule management into the realm of proactive professional development operations (DevSecOps), ensuring that no critical vulnerability disclosure or skill-building opportunity is missed.

## ---

**A) Sources Table: The Intelligence Landscape**

The efficacy of the CyberTracker platform relies entirely on the reliability, legality, and freshness of its data ingestion layer. We categorize sources into three tiers based on their accessibility and structural integrity: **Tier 1 (Official APIs)**, **Tier 2 (Structured Feeds)**, and **Tier 3 (Unstructured/Scraped Data)**.  
The following table represents the result of a deep reconnaissance phase, identifying the primary data vectors required to build a "Single Pane of Glass" for cybersecurity events.

### **Comprehensive Data Sources Inventory**

| Event Domain | Source Name | Data Type | Coverage | Update Freq | Auth Required | Rate Limit / Constraints | Legal / ToS & Operational Notes |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **CTF** | **CTFtime** | API (JSON) | Global (Primary) | Real-time | No (Public) / Yes (Partner) | High sensitivity. "Clones" prohibited. 1 | **Strict Usage Policy:** The API is provided for data analysis and mobile applications only. Users "cannot use this API to run CTFtime clones".1 Platform must act as an aggregator/notifier, deep-linking back to CTFtime for voting and team management to respect ToS. |
| **Conf** | **Sched.com** | API (REST) | High (BSides, Black Hat) | Variable | Yes (API Key) | Standard API limits; strict User-Agent req 2 | Many hacker cons (BSides SF, BH USA) use Sched. The API allows structured retrieval of sessions, speakers, and venues.2 Requires event-specific API keys or public endpoint discovery. |
| **Conf** | **media.ccc.de** | API (JSON/GraphQL) | High (CCC, DeepSec) | Archive (High) | No | Polite use expected; no strict hard limit pub. | Excellent source for **archives** (videos/slides). Provides a public JSON/GraphQL API for conferences like Chaos Communication Congress.3 Open Data friendly. |
| **Conf** | **DEFCON** | HTML / Community | Global (Las Vegas) | Annual | No | N/A | No official public API. Official schedule is often a massive HTML file or PDF.5 Reliance on community-maintained JSONs (e.g., GitHub Gists) or custom HTML parsing is required.7 |
| **Conf** | **Black Hat** | HTML / Mobile App | Global (USA/EU/Asia) | Annual | No | N/A | Website relies heavily on dynamic content. Scraping requires robots.txt compliance.9 Schedule often segmented by "Briefings," "Arsenal," etc..10 |
| **Conf** | **OWASP** | GitHub / Meetup | Global (Chapters) | Monthly | Yes (GitHub/Meetup) | 5000 req/hr (GitHub Auth) 12 | OWASP events are often managed via GitHub repositories or Meetup.com. GitHub API is the primary ingestion vector for project updates and event repos.13 |
| **Archive** | **GitHub** | API (Search/REST) | Global | Constant | Yes (Token) | 30 search/min; 5000 core/hr 12 | The primary engine for finding **write-ups**. We must search for repositories tagged ctf-writeups or matching event names.14 Strict secondary rate limits apply.12 |
| **Archive** | **BSides Repos** | HTML / GitHub | Regional | Post-Event | Mixed | Varies | Individual BSides chapters (e.g., BSidesSF, BSidesLV) often publish archives to YouTube or individual sites. No centralized "BSides API" exists.16 |
| **Aggr** | **InfoSec-Conferences** | HTML | Global | Weekly | No | N/A | A broad aggregator site. Useful for "Discovery" of smaller events not on major radars. HTML scraping required; likely low frequency updates.18 |
| **ICS** | **CISA ICS Calendar** | HTML | US/Gov | Monthly | No | N/A | Specialized training calendar for Industrial Control Systems. Critical for niche "OT Security" tracking. Static HTML parsing required.19 |

### **Strategic Analysis of Data Sources**

The CTFtime Constraint & Compliance:  
CTFtime is the definitive source of truth for the CTF ecosystem. However, their data usage policy is defensive to prevent the proliferation of low-quality clone sites that dilute their community effort. The snippet 1 explicitly warns: "You can not use this API to run CTFtime clones — most of the CTFtime data is moderated by humans, please, respect their time."

* **Implication:** CyberTracker cannot be a "replacement" interface. It must function as an *intelligence layer*. It will ingest metadata (dates, format, difficulty, weight) to populate the calendar and trigger notifications, but the "Scoreboard" and "Voting" features will remain deep links to CTFtime. This aligns with their "mobile applications" allowance by extending functionality (calendar sync, notifications) rather than replicating core web features.

The Conference Heterogeneity Problem:  
Unlike the centralized nature of CTFs, the conference landscape is heterogeneous. However, a pattern emerges in the research: a significant percentage of "hacker" conferences (BSides, Black Hat, specialized summits) utilize Sched.com for schedule management.2

* **Opportunity:** Building a robust SchedAdapter will instantly provide high-fidelity coverage for approximately 40-50% of the target ecosystem. Sched provides a structured API endpoint https://your\_conference.sched.com/api/session/list which is significantly more reliable than HTML scraping.  
* **Fallback:** For major events like DEFCON that rely on static HTML, "hacker" aesthetic sites, or PDF schedules 5, the platform must rely on bespoke scrapers. Interestingly, the community often "fixes" this data problem during the event by publishing cleaned JSONs on GitHub.7 CyberTracker should ingest these community-cleaned feeds where available to reduce parsing errors.

The Archive Gap:  
No single source maps past events to their educational resources (write-ups). GitHub is the de-facto archive for this. By using the GitHub Search API 12 to query for {Event Name} {Year} writeup, CyberTracker can dynamically link historical events to learning materials, creating a unique value proposition that neither CTFtime nor conference sites offer.

## ---

**B) Architecture (MVP): The Event-Driven Modular Monolith**

To handle the disparity between real-time notifications (which require low latency) and heavy historical archiving (which involves rate-limited crawling), the system requires an architecture that separates concerns while maintaining deployment simplicity. We propose an **Event-Driven Architecture (EDA)** utilizing a **Modular Monolith** pattern for the MVP. This allows for shared memory and simplified deployment (single container or pod) while maintaining strict boundary separation between the Ingestion, Core, and Notification domains.

### **Architectural Principles**

1. **Async-First:** Python's asyncio is the foundation. Network I/O (scraping 50 sources) must not block the API or notification dispatch.  
2. **Strict Rate Limiting:** Outbound requests must be governed by a "Token Bucket" implementation to prevent IP bans from source providers (SecOps requirement).  
3. **Data decoupling:** The ingestion layer puts "raw" data into the system; the normalization layer transforms it into the "canonical" model. This preserves the raw data for debugging when parsers inevitably break due to HTML changes.

### **High-Level Component Diagram**

Kod snippet'i

graph TD  
    User\[User / Client\] \--\>|HTTPS/REST| API\[FastAPI Gateway\]  
    API \--\>|Read| Cache  
    API \--\>|Read/Write| DB  
      
    subgraph "Ingestion Engine (SecOps)"  
        Scheduler \--\>|Trigger| Dispatcher  
        Dispatcher \--\>|Queue| ScraperQueue  
        ScraperQueue \--\>|Pop| AdapterCTF  
        ScraperQueue \--\>|Pop| AdapterSched  
        ScraperQueue \--\>|Pop| AdapterHTML  
          
        AdapterCTF & AdapterSched & AdapterHTML \--\>|Raw Data| Normalizer  
        Normalizer \--\>|Enrichment| Tagger  
        Tagger \--\>|Upsert| DB  
    end  
      
    subgraph "Notification Engine"  
        DB \--\>|New Event Trigger| Stream  
        Stream \--\>|Consume| Notifier  
        Notifier \--\>|Check Prefs| UserPrefs\[User Preferences\]  
        UserPrefs \--\>|Filter| Dispatch  
          
        Dispatch \--\>|Rate Limit| Discord  
        Dispatch \--\>|Rate Limit| Telegram  
        Dispatch \--\>|Batch| Email  
    end  
      
    subgraph "Archive Subsystem"  
        ArchiveScheduler \--\>|Trigger| GitHubWorker\[GitHub Crawler\]  
        GitHubWorker \--\>|Search API| GitHub  
        GitHubWorker \--\>|Index Writeups| DB  
    end

### **Technology Stack Recommendation**

* **Backend Framework:** **FastAPI (Python)**.  
  * *Justification:* Python is the lingua franca of security and scraping. FastAPI offers high-performance async capabilities essential for handling concurrent scraping tasks and websocket connections.22 It significantly outperforms Flask/Django in throughput and provides automatic OpenAPI documentation, which is crucial for potential future integrations.  
* **Database:** **PostgreSQL**.  
  * *Justification:* We need relational integrity for User-Event subscriptions but the extreme flexibility of NoSQL for event metadata (which varies wildly between CTFs and Conferences). Postgres' JSONB column type offers the best of both worlds, allowing us to store unstructured scraped attributes (like "prizes" or "hotel codes") without complex schema migrations.  
* **Task Queue:** **ARQ (Async Redis Queue)**.  
  * *Justification:* While Celery is the industry standard, it is heavy and synchronous-first. ARQ is built specifically for asyncio and integrates natively with FastAPI, allowing for lighter, faster background workers for I/O-bound scraping tasks.24 It uses Redis directly, simplifying the infrastructure.  
* **Caching & Broker:** **Redis**.  
  * *Justification:* Required for ARQ, but also essential for caching API responses (to respect CTFtime's rate limits) and deduplicating notification triggers.26 Redis Streams will handle the decoupling of ingestion and notification.  
* **Frontend:** **Next.js**.  
  * *Justification:* Server-side rendering (SSR) is critical for SEO if the archive is to be indexed by search engines. The React ecosystem allows for rich, interactive calendar components that can handle timezone complexities on the client side.

## ---

**C) Data Model: The Schema of Truth**

The database schema must be **polymorphic** to handle the divergent structures of CTFs (Teams, Flags, Points) and Conferences (Speakers, Tracks, Rooms, Villages). We will use a core events table with a heavy reliance on JSONB for domain-specific attributes.

### **Core Entities (Postgres Schema)**

Table: events  
This is the central registry. It normalizes time and identity.

| Field | Type | Description |
| :---- | :---- | :---- |
| id | UUID | Primary Key |
| external\_id | String | Unique ID from source (e.g., ctftime\_1234, sched\_bhusa25\_session1). Used for idempotent upserts. |
| source | Enum | ctftime, sched, defcon, blackhat\_html, manual |
| title | String | Event Name (e.g., "DEF CON 33", "Pwn2Own Vancouver") |
| start\_time | Timestamptz | **Normalized UTC Start**. Crucial for calendar generation. |
| end\_time | Timestamptz | **Normalized UTC End**. |
| type | Enum | ctf, conference, meetup, training |
| format | Enum | jeopardy, attack-defense, seminar, workshop, village |
| slug | String | URL-friendly identifier for the frontend. |
| metadata | JSONB | Stores flexible data: prizes, location (physical), ctf\_weight, cfp\_link, logo\_url. |
| tags | Array | web, crypto, pwn, iot, cloud (Enriched via NLP tagging). |
| is\_verified | Boolean | True if from Tier 1 source; False if scraped from community calendar. |

Table: resources (The Archive Layer)  
This table maps external knowledge artifacts to events.

| Field | Type | Description |
| :---- | :---- | :---- |
| id | UUID | Primary Key |
| event\_id | UUID | Foreign Key to events. |
| resource\_type | Enum | writeup, slide, video, code, tool |
| url | String | URL to GitHub/YouTube/PDF. |
| author | String | Author/Speaker Name (e.g., "LiveOverflow", "Gynvael Coldwind"). |
| challenge\_name | String | (Nullable) Specific CTF challenge name (e.g., "heap-of-trouble"). |
| difficulty | Integer | 1-5 Scale (inferred from write-up keywords or CTF points). |
| stars | Integer | (Nullable) Quality metric (e.g., GitHub stars) to sort high-quality writeups.27 |

Table: subscriptions (Personalization)  
Handles the many-to-many relationship between users and their interests.

| Field | Type | Description |
| :---- | :---- | :---- |
| user\_id | UUID | Foreign Key to Users. |
| filter\_config | JSONB | { "tags": \["pwn", "rev"\], "min\_weight": 20, "region": "EU" }. Defines *what* they want. |
| channels | JSONB | { "discord": "webhook\_url", "email": true, "telegram": "chat\_id" }. Defines *where* they want it. |
| digest\_frequency | Enum | realtime, daily\_digest, weekly\_digest. |

## ---

**D) ETL & Scraping Strategy: The OSINT Pipeline**

The ingestion pipeline must be robust against "DOM drift" (HTML structure changes) and respectful of rate limits to avoid IP bans. It operates as a continuous loop of Discovery, Extraction, Normalization, and Enrichment.

### **Step 1: The Collector Layer (Ingestion)**

The Scheduler triggers specific adapters based on update frequency tiers.

* **CTFtime Adapter:** Runs hourly. Hits https://ctftime.org/api/v1/events/. Checks start and finish timestamps.  
* **Sched Adapter:** Runs daily. Hits https://\[conference\].sched.com/api/session/list. Requires an index of known Sched URLs (e.g., maintain a config list of bsidessf2025, blackhat2025).  
* **HTML Scrapers:** Run weekly. Used for DEFCON/Black Hat main sites. Implements Playwright only if necessary (for SPAs), otherwise uses httpx and BeautifulSoup4 for speed.

### **Step 2: The Normalizer Layer**

Data arrives in chaotic formats. This layer standardizes it.

* **Timezone Normalization:** The single biggest point of failure. Sched.com events often lack timezone offsets in the export. The normalizer must geo-locate the event (e.g., "Las Vegas") to determine the IANA timezone (America/Los\_Angeles) and convert all timestamps to **UTC** before storage.  
* **Category Mapping:** A Black Hat "Briefing" and a CTFtime "Jeopardy" are both "events" but need distinct handling. We map source-specific types to our internal Enum.

### **Step 3: The OSINT Enrichment Layer**

This is where raw data becomes intelligence.

* **Tagging:** We apply a keyword extraction implementation (using nltk or simple regex) on event descriptions.  
  * *Keywords:* "heap", "rop", "kernel" \-\> Tag: pwn.  
  * *Keywords:* "smart contract", "solidity" \-\> Tag: blockchain.  
  * *Keywords:* "lockpicking", "physical" \-\> Tag: physical-security.  
* **Difficulty Inference:** For CTFs, we map the CTFtime weight field to a normalized 1-5 difficulty scale. For conferences, we look for "beginner" vs "advanced" tracks in the Sched metadata.2

### **Step 4: Deduplication & Validation**

Before writing to the DB, we generate a **Fingerprint Hash** (SHA256 of title \+ start\_time\_iso \+ source\_domain). We check a Redis Bloom Filter or Set to see if this event fingerprint exists.

* *Why?* To prevent "Notification Storms." If a scraper runs and finds the same 50 events, we must not trigger 50 webhooks. We only upsert if the hash differs (indicating an update) or is new.

### **Failure Modes & Mitigations**

1. **Source Blocking (429/403):**  
   * *Mitigation:* Implement exponential backoff (retries). Rotate User-Agents. Use a proxy pool if necessary (though Tier 1 sources usually don't require this if rate limits are respected).  
2. **Schema Change (DOM Drift):**  
   * *Mitigation:* Use Pydantic models for validation. If the scraped data fails validation (e.g., title is missing), the item is quarantined, and a SecOps alert is sent to the admin. The pipeline does *not* crash; it skips the malformed item.  
3. **Android Webcal Failure:**  
   * *Mitigation:* Android devices do not handle webcal:// links natively.28 The frontend must detect the User-Agent. If Android, serve an https:// link to the .ics file instead of webcal://.

## ---

**E) Calendar Integration Recommendation**

Users require seamless integration with their existing workflows (Google Calendar, Outlook, Apple Calendar). The "Subscribe" model is superior to "Import" because it allows for dynamic updates (e.g., if a CTF start time changes).

### **Recommended Approach: Dynamic Webcal Subscription**

We will generate dynamic .ics feeds accessible via the webcal:// protocol.

* **Endpoint:** GET /calendar/{user\_api\_key}/feed.ics  
* **Library:** ics.py 29 or icalendar.30 These libraries handle the RFC 5545 complexity (folding lines, date formatting).  
* **Technical Implementation:**  
  * **Headers:** Serve with Content-Type: text/calendar; charset=utf-8 and Cache-Control: no-cache to force clients to refresh.  
  * **UID Persistence:** Critical. The UID field in the .ics file must be deterministic (e.g., UUIDv5(namespace, event\_id)). If the UID changes between fetches, the client (Google Calendar) will duplicate the event rather than update it.  
  * **Alarms:** Include a VALARM component (reminder) set to \-PT1H (1 hour before) for all subscribed events.

### **"Nice-to-Have" Integrations**

* **Direct Google Calendar API:** Allow users to "Push" specific events to their calendar via OAuth. This is useful for "picking" single events rather than subscribing to a whole feed. However, it requires significant OAuth scope (calendar.events.owned) which increases security risk/friction.  
* **CalDAV:** While powerful, implementing a full CalDAV server (RFC 4791\) is overkill for an MVP. Webcal (read-only subscription) covers 95% of user needs with 10% of the complexity.

## ---

**F) Notification & Personalization Spec**

To prevent "alert fatigue," the notification system must use a highly specific "negative-filtering" model. Security professionals are busy; spamming them with every "Beginner CTF" will cause them to mute the bot.

### **User Preference Model**

Users define a NotificationProfile JSON blob:

JSON

{  
  "filters": {  
    "include\_tags": \["web", "pwn", "cloud", "defcon"\],  
    "exclude\_tags": \["forensics", "osint"\],  
    "min\_ctf\_weight": 25.0,  
    "event\_types": \["ctf", "conference"\],  
    "location\_proximity": "remote\_only"  
  },  
  "channels": {  
    "discord\_webhook": "https://discord.com/api/webhooks/...",  
    "telegram\_chat\_id": "12345678"  
  },  
  "frequency": "digest\_daily"  
}

### **Notification Logic & Scoring**

We assign a **Relevance Score** to every event for every user.

* *Formula:* Score \= (Base\_Weight) \+ (Tag\_Match \* 10\) \+ (Region\_Match \* 5\)  
* *Threshold:* If Score \> User\_Threshold, send notification.

### **Channel-Specific Constraints**

* **Discord:**  
  * *Limit:* 5 requests per 2 seconds per webhook.31  
  * *Content:* Max 2000 chars. Use Embeds for richer data (Titles, URLs, Images).32  
  * *Strategy:* Use a Redis-backed Token Bucket limiter per webhook ID to queue messages.  
* **Telegram:**  
  * *Limit:* 4096 characters per message.33  
  * *Strategy:* Truncate event descriptions. If a "Digest" is too long, split it into multiple messages with pagination (e.g., "Page 1/3").  
* **Anti-Spam Rules:**  
  * **Frequency Cap:** Max 3 notifications per hour per user (unless "Realtime" is explicitly requested).  
  * **Digest Mode:** For "Daily" users, events are pushed to a notification\_buffer table. A scheduled task runs at 09:00 UTC, aggregates pending events into a single summary, and dispatches it.

## ---

**G) Security & SecOps: Threat Model & Controls**

As a tool for security professionals, CyberTracker will be scrutinized. It must model exemplary security posture.

### **Threat Model**

1. **SSRF (Server-Side Request Forgery):**  
   * *Vector:* Scrapers fetching URLs provided by users (e.g., if we allow users to submit "Custom Feeds") or compromised event sources redirecting to internal IPs.  
   * *Impact:* Access to internal metadata services (AWS IMDS), local Redis instance, or container network.  
2. **Scraping Infrastructure Abuse:**  
   * *Vector:* Aggressive scraping triggering IP bans from CTFtime or Black Hat.  
   * *Impact:* Denial of Service (DoS) for the platform's core data stream.  
3. **Injection via Scraped Content:**  
   * *Vector:* An event organizer inserts \<script\>alert(1)\</script\> into their Sched.com description.  
   * *Impact:* Stored XSS affecting CyberTracker administrators or users viewing the dashboard.  
4. **Information Leakage via Calendar:**  
   * *Vector:* Users sharing their private webcal URL.  
   * *Impact:* Leakage of personal subscription preferences (low impact, but privacy violation).

### **SecOps Controls Checklist**

* \[ \] **Network Isolation:** Scrapers must run in a restricted Docker network namespace with *no access* to internal services. Block outbound traffic to private IP ranges (10.0.0.0/8, 169.254.169.254, etc.) at the firewall level.  
* \[ \] **Input Sanitization:** Strict sanitization of all HTML/Text fields from scrapers using a library like bleach (Python) before storage. Treat all scraped data as untrusted user input.  
* \[ \] **Secrets Management:** Use .env files loaded via Pydantic Settings. Never commit API keys. Use GitHub Secret Scanning in the repo.34  
* \[ \] **Rate Limiting (Outbound):** Implement a Global Rate Limiter (Token Bucket) on outbound requests per domain. Respect Crawl-delay in robots.txt.9  
* \[ \] **Rate Limiting (Inbound):** Limit API consumers (users) to preventing DDoS (e.g., 60 req/min).  
* \[ \] **Dependency Scanning:** Automated GitHub workflow (Dependabot or Snyk) to check for vulnerable Python libraries in the supply chain.34

## ---

**H) MVP Roadmap (4 Weeks)**

**Week 1: Foundation & Ingestion Core**

* **Architecture:** Setup FastAPI \+ Postgres \+ Redis \+ Docker Compose.  
* **Ingestion:** Implement CTFtimeAdapter (JSON) and SchedAdapter.  
* **Database:** Design schema via SQLAlchemy/SQLModel. Run migrations (Alembic).  
* **Milestone:** Database is populated with the next 30 days of global events.

**Week 2: Core Logic & Calendar Output**

* **API:** Implement GET /events with query parameter filtering (tags, dates).  
* **Calendar:** Implement GET /calendar/{uid}/feed.ics using ics.py. Handle timezone normalization logic.  
* **Frontend:** Scaffold Next.js app. Create "Event List" view.  
* **Milestone:** Users can subscribe to a generic calendar feed that updates automatically.

**Week 3: Notification Engine & Personalization**

* **Queue:** Integrate ARQ (Redis Queue).  
* **Dispatch:** Build DiscordDispatcher and TelegramDispatcher. Implement rate limiting logic.  
* **User Prefs:** Build simple UI for selecting tags and inputting Webhook URLs.  
* **Milestone:** Real-time alert sent to a test Discord server when a new event is added to the DB.

**Week 4: Archive Subsystem & Polish**

* **Archive Crawler:** Build GitHubWorker using Search API. Link write-ups to existing Event IDs.  
* **Refinement:** Implement robots.txt middleware. Add "Verify" badges for official events.  
* **Deployment:** Deploy to cloud (e.g., DigitalOcean App Platform or Railway).  
* **Milestone:** Product Launch (Alpha) with 3 key features: Calendar, Notifications, and Write-up Search.

## ---

**I) Archive Strategy: The "Write-Up" Crawler**

The platform's unique value proposition is the **Archive**. While CTFtime links to write-ups, it often misses those hosted in personal repos or gists. We will utilize the GitHub Search API to find write-ups automatically.

### **Acquisition Plan**

1. **Trigger:** 24 hours after a CTF event concludes (end\_time), trigger the ArchiveWorker.  
2. **Query Heuristic:** Construct queries targeting specific naming conventions:  
   * "{CTF\_NAME} {YEAR}" writeup  
   * "{CHALLENGE\_NAME}" CTF  
   * extension:md (Markdown files are standard for write-ups).  
3. **Rate Limits:** GitHub allows 30 search requests per minute for authenticated users.12 The worker must throttle itself.  
4. **Metadata Extraction:** Parse the README.md to extract:  
   * Challenge Category (often in headers).  
   * Tools used (regex match for gdb, burpsuite, ghidra).  
5. **Quality Control:** Only index repositories with \>0 Stars or from known reputable teams (allowlist).  
6. **Copyright:** Store *links*, not content. This avoids copyright infringement. Display the License type (MIT, GPL) if detected in the repo.14

### **Metadata Strategy**

We map the graph:

* **Event** (DEFCON 33\) \<-\> **Resource** (YouTube Video ID)  
* **Event** (DEFCON 33\) \<-\> **Resource** (Slide Deck PDF)  
* **CTF** (Google CTF) \<-\> **Challenge** (Log4j) \<-\> **Resource** (Writeup URL)

By executing this roadmap, CyberTracker will evolve from a simple list of dates into a dynamic intelligence tool, directly supporting the operational readiness of the cybersecurity community.

#### **Alıntılanan çalışmalar**

1. CTFtime.org / API, erişim tarihi Ocak 19, 2026, [https://ctftime.org/api/](https://ctftime.org/api/)  
2. API Documentation \- Sched, erişim tarihi Ocak 19, 2026, [https://sched.com/api](https://sched.com/api)  
3. about media.ccc.de, erişim tarihi Ocak 19, 2026, [https://media.ccc.de/about.html](https://media.ccc.de/about.html)  
4. percidae/media.ccc.de \- GitHub, erişim tarihi Ocak 19, 2026, [https://github.com/percidae/media.ccc.de](https://github.com/percidae/media.ccc.de)  
5. One Page Schedule \- DEF CON.outel.org, erişim tarihi Ocak 19, 2026, [https://defcon.outel.org/defcon31/dc31-consolidated\_page.html](https://defcon.outel.org/defcon31/dc31-consolidated_page.html)  
6. The ONE\! One Schedule to Rule them All\!, erişim tarihi Ocak 19, 2026, [https://defcon.outel.org/archive/dc29\_schedule.pdf](https://defcon.outel.org/archive/dc29_schedule.pdf)  
7. Defcon schedule as JSON \- GitHub Gist, erişim tarihi Ocak 19, 2026, [https://gist.github.com/azeemba/a27689e1252711159d602abac6237366](https://gist.github.com/azeemba/a27689e1252711159d602abac6237366)  
8. Defcon 27 JSON Schedule \- GitHub Gist, erişim tarihi Ocak 19, 2026, [https://gist.github.com/jgamblin/18232aa92dc9408e306b07f339dfe057](https://gist.github.com/jgamblin/18232aa92dc9408e306b07f339dfe057)  
9. An introduction to robots.txt files \- Digital.gov, erişim tarihi Ocak 19, 2026, [https://digital.gov/resources/introduction-robots-txt-files](https://digital.gov/resources/introduction-robots-txt-files)  
10. Black Hat USA 2025 | Conference at a Glance, erişim tarihi Ocak 19, 2026, [https://blackhat.com/us-25/schedule.html](https://blackhat.com/us-25/schedule.html)  
11. Black Hat USA 2025 | Arsenal Schedule, erişim tarihi Ocak 19, 2026, [https://blackhat.com/us-25/arsenal/schedule/](https://blackhat.com/us-25/arsenal/schedule/)  
12. Rate limits for the REST API \- GitHub Docs, erişim tarihi Ocak 19, 2026, [https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api)  
13. Setting Up Events \- OWASP Foundation, erişim tarihi Ocak 19, 2026, [https://owasp.org/www-staff/procedures/event\_site\_setup](https://owasp.org/www-staff/procedures/event_site_setup)  
14. CSYClubIIITK/CTF-Writeups: This is a repository for all the writeups of CTFs organized by us. \- GitHub, erişim tarihi Ocak 19, 2026, [https://github.com/CSYClubIIITK/CTF-Writeups](https://github.com/CSYClubIIITK/CTF-Writeups)  
15. ctf-writeup · GitHub Topics, erişim tarihi Ocak 19, 2026, [https://github.com/topics/ctf-writeup?o=asc\&s=stars](https://github.com/topics/ctf-writeup?o=asc&s=stars)  
16. BSides Las Vegas, erişim tarihi Ocak 19, 2026, [https://bsideslv.org/](https://bsideslv.org/)  
17. BSidesSF, erişim tarihi Ocak 19, 2026, [https://bsidessf.org/](https://bsidessf.org/)  
18. Cybersecurity Conferences 2026 \- 2027 | Over 3.4K Events | Concise AC, erişim tarihi Ocak 19, 2026, [https://infosec-conferences.com/](https://infosec-conferences.com/)  
19. ICS Training Calendar \- CISA, erişim tarihi Ocak 19, 2026, [https://www.cisa.gov/ics-training-calendar](https://www.cisa.gov/ics-training-calendar)  
20. BSidesSF 2025: Schedule, erişim tarihi Ocak 19, 2026, [https://bsidessf2025.sched.com/](https://bsidessf2025.sched.com/)  
21. How to search for code in GitHub with GitHub API? \- Stack Overflow, erişim tarihi Ocak 19, 2026, [https://stackoverflow.com/questions/24132790/how-to-search-for-code-in-github-with-github-api](https://stackoverflow.com/questions/24132790/how-to-search-for-code-in-github-with-github-api)  
22. NestJS vs. FastAPI: which one's better to specialize in for backend? \- Reddit, erişim tarihi Ocak 19, 2026, [https://www.reddit.com/r/PinoyProgrammer/comments/1nurt7z/nestjs\_vs\_fastapi\_alin\_mas\_okay\_ispecialize\_for/?tl=en](https://www.reddit.com/r/PinoyProgrammer/comments/1nurt7z/nestjs_vs_fastapi_alin_mas_okay_ispecialize_for/?tl=en)  
23. FastAPI vs Spring Boot / NestJS for scalable, AI-driven SaaS backends? \- Reddit, erişim tarihi Ocak 19, 2026, [https://www.reddit.com/r/Backend/comments/1nz2ofu/fastapi\_vs\_spring\_boot\_nestjs\_for\_scalable/](https://www.reddit.com/r/Backend/comments/1nz2ofu/fastapi_vs_spring_boot_nestjs_for_scalable/)  
24. Celery Versus ARQ Choosing the Right Task Queue for Python Applications | Leapcell, erişim tarihi Ocak 19, 2026, [https://leapcell.io/blog/celery-versus-arq-choosing-the-right-task-queue-for-python-applications](https://leapcell.io/blog/celery-versus-arq-choosing-the-right-task-queue-for-python-applications)  
25. Managing Background Tasks in FastAPI: BackgroundTasks vs ARQ \+ Redis \- David Muraya, erişim tarihi Ocak 19, 2026, [https://davidmuraya.com/blog/fastapi-background-tasks-arq-vs-built-in/](https://davidmuraya.com/blog/fastapi-background-tasks-arq-vs-built-in/)  
26. Redis and its role in System Design \- GeeksforGeeks, erişim tarihi Ocak 19, 2026, [https://www.geeksforgeeks.org/system-design/redis-and-its-role-in-system-design/](https://www.geeksforgeeks.org/system-design/redis-and-its-role-in-system-design/)  
27. ilanami/ctf\_writeup\_builder: "A modern and private application for creating, organizing and exporting CTF write-ups with AI assistance" \- GitHub, erişim tarihi Ocak 19, 2026, [https://github.com/ilanami/ctf\_writeup\_builder](https://github.com/ilanami/ctf_writeup_builder)  
28. Cannot subscribe to calendars using the webcal:// scheme on Android \- Issue Tracker, erişim tarihi Ocak 19, 2026, [https://issuetracker.google.com/issues/465755643](https://issuetracker.google.com/issues/465755643)  
29. Ics.py : iCalendar for Humans — ics.py 0.7.2 documentation, erişim tarihi Ocak 19, 2026, [https://icspy.readthedocs.io/](https://icspy.readthedocs.io/)  
30. Internet Calendaring and Scheduling (iCalendar) for Python — icalendar 6.3.2 documentation, erişim tarihi Ocak 19, 2026, [https://icalendar.readthedocs.io/](https://icalendar.readthedocs.io/)  
31. Rate Limits \- Discord Webhooks Guide, erişim tarihi Ocak 19, 2026, [https://birdie0.github.io/discord-webhooks-guide/other/rate\_limits.html](https://birdie0.github.io/discord-webhooks-guide/other/rate_limits.html)  
32. Field Limits \- Discord Webhooks Guide, erişim tarihi Ocak 19, 2026, [https://birdie0.github.io/discord-webhooks-guide/other/field\_limits.html](https://birdie0.github.io/discord-webhooks-guide/other/field_limits.html)  
33. Telegram \- CM.com Developers Portal, erişim tarihi Ocak 19, 2026, [https://developers.cm.com/messaging/docs/telegram](https://developers.cm.com/messaging/docs/telegram)  
34. Free for Open Source Application Security Tools \- OWASP Foundation, erişim tarihi Ocak 19, 2026, [https://owasp.org/www-community/Free\_for\_Open\_Source\_Application\_Security\_Tools](https://owasp.org/www-community/Free_for_Open_Source_Application_Security_Tools)