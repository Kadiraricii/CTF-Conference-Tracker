# CTF & Conference Tracker Platform: Complete Research & Design Document

**Role:** Senior Cybersecurity Product Researcher + OSINT/SecOps Engineer  
**Date:** January 19, 2026  
**Objective:** Design a production-ready platform for tracking global cybersecurity CTFs and conferences with personalization, notifications, and archival features.

---

## A) SOURCES TABLE

### CTF Event Sources

| Source | Type | Coverage | Update Frequency | Auth Needed | Rate Limit | Legal/ToS Notes | URL |
|--------|------|----------|------------------|-------------|------------|-----------------|-----|
| **CTFtime API** | REST API | Global CTFs, teams, events, ratings | Real-time | No | Not officially documented (recommend 1 req/sec) | Free for data analysis & mobile apps; cannot clone CTFtime; respect human moderators | https://ctftime.org/api/ |
| CTFtime Events Endpoint | JSON | Past/upcoming events with metadata | Daily | No | 100 events/request max | Available fields: start/end timestamps, format, weight, organizers, URL, restrictions | https://ctftime.org/api/v1/events/ |
| CTFtime Team Info | JSON | Team rankings, country data | Updated after events | No | Same as above | Top teams by year/country available | https://ctftime.org/api/v1/teams/ |
| CTFtime Write-ups | HTML Scraping | Challenge write-ups with links | Post-event | No | Polite crawling | Not exposed via API; link to original writeups | https://ctftime.org/writeups |
| **GitHub CTF Repos** | Git/HTML | Historical write-ups (2012-2018+) | Static archives | No | GitHub API: 5000/hr authenticated | Community-maintained; respect licenses | https://github.com/ctfs |
| CTF Write-ups 2015-2018 | Git Repository | Organized by year/event | Static | No | N/A | Creative Commons licenses | https://github.com/ctfs/write-ups-* |
| Individual Team Repos | Git Repository | Personal CTF solutions | Variable | No | N/A | Various licenses; check each repo | GitHub search: "ctf-writeup" |

### Conference Event Sources

| Source | Type | Coverage | Update Frequency | Auth Needed | Rate Limit | Legal/ToS Notes | URL |
|--------|------|----------|------------------|-------------|------------|-----------------|-----|
| **Black Hat Official** | HTML | USA, Europe, Asia, MEA events | 3-6 months pre-event | No | Polite crawling | Check robots.txt; materials 2 weeks post-event | https://blackhat.com/ |
| Black Hat Archives | HTML/Video | Presentations 1997-present | 90-120 days post-event | No | Polite crawling | Audio/video on YouTube channel | https://blackhat.com/html/archives.html |
| Black Hat YouTube | Video/API | Conference talks | Post-event | YouTube API key | 10,000 units/day | YouTube ToS applies | https://www.youtube.com/c/BlackHatOfficialYT |
| **DEF CON Media** | HTML/Archive | Talks, slides, villages | Post-event | No | Polite crawling | Comprehensive archives with CTF data | https://media.defcon.org/ |
| DEF CON Archives | RAR/Torrent | Presentations, workshops, docs | Post-event | No | N/A | Download archives per year | https://defcon.org/html/links/dc-archives/ |
| **RSA Conference** | HTML | RSAC sessions, innovation sandbox | Annual (April) | No | Polite crawling | 45k+ attendees; vendor content | https://www.rsaconference.com/ |
| **OWASP Events** | HTML/iCal | Global & regional AppSec events | Ongoing | No | Polite crawling | .ics calendar feeds available | https://owasp.org/events/ |
| OWASP Sched | API/HTML | Event schedules, speakers | Pre/during event | No | Moderate | Event-specific subdomains | https://owasp2025globalappseceu.sched.com/ |
| **BSides Events** | HTML | Community-driven local events | Regional/ongoing | No | Polite crawling | Decentralized; check individual BSides sites | http://www.securitybsides.com/ |
| **CCC (Chaos Computer Club)** | HTML | Annual Congress (Dec 27-30) | Annual | No | Polite crawling | Tickets ~€175; media archives available | https://www.ccc.de/ |
| **InfoCon** | Archive | Multi-conference videos/docs | Historical | No | N/A | Aggregated conference materials | https://infocon.org/ |

### Community Aggregators

| Source | Type | Coverage | Update Frequency | Auth Needed | Rate Limit | Legal/ToS Notes | URL |
|--------|------|----------|------------------|-------------|------------|-----------------|-----|
| Conference List Repos | GitHub | APAC, global conference calendars | Community updates | No | N/A | Check individual event policies | https://github.com/Infosec-Community/APAC-Conferences |
| Base Cyber Security Calendar | HTML | European security events | Seasonal | No | Polite crawling | Aggregated from multiple sources | https://basecybersecurity.com/cyber-security-events-* |

**Key Findings:**
- **CTFtime API** is the authoritative source for CTF data but has no official rate limits; recommend conservative 1 req/second
- **No official conference APIs** exist; must scrape HTML or use event-specific .ics feeds where available
- **Write-ups** are decentralized across GitHub, CTFtime, and individual blogs
- **Video archives** available 90-120 days post-event for major conferences
- **Legal compliance critical**: CTFtime explicitly forbids cloning; respect robots.txt for all scrapers

---

## B) ARCHITECTURE (MVP)

### System Components

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Web App     │  │  Mobile PWA  │  │  RSS Feed    │          │
│  │  (Next.js)   │  │              │  │  (.ics gen)  │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                             ↓ HTTPS
┌─────────────────────────────────────────────────────────────────┐
│                      API GATEWAY LAYER                           │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Nginx / Cloudflare (WAF, DDoS protection, rate limiting)│   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                             │
│  ┌─────────────────────┐  ┌────────────────────┐               │
│  │  FastAPI Backend    │  │  Auth Service      │               │
│  │  - REST API         │  │  - JWT tokens      │               │
│  │  - WebSocket (opt)  │  │  - OAuth2          │               │
│  └─────────────────────┘  └────────────────────┘               │
└─────────────────────────────────────────────────────────────────┘
        ↓                ↓                    ↓
┌──────────────┐  ┌──────────────┐  ┌────────────────────┐
│  Scheduler   │  │   Cache      │  │   Search Index     │
│  (Celery +   │  │   (Redis)    │  │   (Meilisearch/    │
│   Redis)     │  │              │  │    Elasticsearch)  │
└──────────────┘  └──────────────┘  └────────────────────┘
        ↓
┌─────────────────────────────────────────────────────────────────┐
│                   SCRAPING / ETL LAYER                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  CTFtime     │  │  Conference  │  │  Write-up    │          │
│  │  Collector   │  │  Scrapers    │  │  Scraper     │          │
│  │  (API poll)  │  │  (Playwright)│  │  (GitHub)    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
        ↓                       ↓                      ↓
┌─────────────────────────────────────────────────────────────────┐
│              DATA PROCESSING / VALIDATION                        │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  - Schema validation (Pydantic)                          │   │
│  │  - Deduplication (fuzzy matching)                        │   │
│  │  - Enrichment (category tagging, timezone normalization) │   │
│  │  - OSINT processing (difficulty estimation, team size)   │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                      STORAGE LAYER                               │
│  ┌─────────────────────┐  ┌────────────────────┐               │
│  │  PostgreSQL         │  │  Object Storage    │               │
│  │  - Events           │  │  (S3/MinIO)        │               │
│  │  - Users            │  │  - Slides/videos   │               │
│  │  - Preferences      │  │  - Write-up PDFs   │               │
│  │  - Archive metadata │  │                    │               │
│  └─────────────────────┘  └────────────────────┘               │
└─────────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                  NOTIFICATION LAYER                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Email       │  │  Telegram    │  │  Discord     │          │
│  │  (SendGrid)  │  │  Bot API     │  │  Webhook     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

### Key Design Decisions

1. **FastAPI Backend**: Type-safe, async, auto-generated docs, excellent for MVP speed
2. **Celery + Redis**: Distributed task queue for scheduled scraping, decoupled from API
3. **PostgreSQL with JSONB**: Relational structure + flexible schema for event metadata
4. **Meilisearch**: Lightweight, typo-tolerant search with faceted filters (vs. Elasticsearch for MVP)
5. **Playwright over Selenium**: Modern, faster, better API for JavaScript-heavy sites
6. **Next.js SSR**: SEO-friendly, fast initial load, API routes for serverless functions

### MVP Endpoints (Core)

```
POST   /api/auth/register          - User registration
POST   /api/auth/login             - JWT authentication
GET    /api/events                 - List events (CTF + conferences)
GET    /api/events/{id}            - Event details
POST   /api/preferences            - Set user notification preferences
GET    /api/calendar.ics           - Generate personalized iCal feed
GET    /api/archive/writeups       - Search write-ups
GET    /api/archive/materials      - Search conference materials
POST   /api/notifications/test     - Test notification channels
GET    /api/search?q=...           - Full-text search across events
```

---

## C) DATA MODEL

### Core Schema (PostgreSQL)

```sql
-- Events table (unified CTF + conferences)
CREATE TABLE events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id VARCHAR(255) UNIQUE,  -- External ID (e.g., CTFtime event ID)
    source VARCHAR(50) NOT NULL,     -- 'ctftime', 'blackhat', 'defcon', etc.
    type VARCHAR(20) NOT NULL,       -- 'ctf', 'conference', 'workshop'
    title VARCHAR(500) NOT NULL,
    description TEXT,
    start_time TIMESTAMPTZ NOT NULL,
    end_time TIMESTAMPTZ NOT NULL,
    timezone VARCHAR(50),
    
    -- Location
    format VARCHAR(20),              -- 'online', 'onsite', 'hybrid'
    location_city VARCHAR(255),
    location_country VARCHAR(2),     -- ISO 3166-1 alpha-2
    venue TEXT,
    
    -- CTF-specific
    ctf_weight DECIMAL(5,2),         -- CTFtime weight
    ctf_format VARCHAR(50),          -- 'jeopardy', 'attack-defense', 'mixed'
    team_size_min INT,
    team_size_max INT,
    restrictions JSONB,              -- {academic_only: bool, region: [], etc.}
    
    -- Conference-specific
    tracks JSONB,                    -- ['keynote', 'technical', 'training']
    estimated_attendees INT,
    
    -- Common metadata
    categories JSONB NOT NULL,       -- ['web', 'crypto', 'pwn', 'forensics', 'devsecops']
    difficulty VARCHAR(20),          -- 'beginner', 'intermediate', 'advanced', 'expert'
    prize_pool DECIMAL(12,2),
    organizer VARCHAR(255),
    url TEXT,
    registration_url TEXT,
    registration_deadline TIMESTAMPTZ,
    
    -- Housekeeping
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    last_scraped TIMESTAMPTZ,
    is_verified BOOLEAN DEFAULT FALSE
);

CREATE INDEX idx_events_start_time ON events(start_time);
CREATE INDEX idx_events_categories ON events USING GIN(categories);
CREATE INDEX idx_events_type ON events(type);
CREATE INDEX idx_events_format ON events(format);

-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255),      -- NULL for OAuth users
    oauth_provider VARCHAR(50),      -- 'google', 'github', null
    oauth_id VARCHAR(255),
    display_name VARCHAR(255),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    last_login TIMESTAMPTZ,
    email_verified BOOLEAN DEFAULT FALSE
);

-- User preferences
CREATE TABLE user_preferences (
    user_id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    
    -- Event filters
    categories JSONB,                -- ['web', 'crypto']
    formats JSONB,                   -- ['jeopardy', 'online']
    difficulty_levels JSONB,         -- ['intermediate', 'advanced']
    regions JSONB,                   -- ['US', 'EU', 'APAC']
    event_types JSONB,               -- ['ctf', 'conference']
    team_size_range INT[],           -- [2, 5]
    
    -- Notification settings
    notify_email BOOLEAN DEFAULT TRUE,
    notify_telegram BOOLEAN DEFAULT FALSE,
    notify_discord BOOLEAN DEFAULT FALSE,
    telegram_chat_id VARCHAR(255),
    discord_webhook_url TEXT,
    
    -- Notification timing
    notify_days_before INT DEFAULT 7,
    notify_on_registration_open BOOLEAN DEFAULT TRUE,
    notify_on_schedule_published BOOLEAN DEFAULT FALSE,
    
    -- Digest mode
    digest_enabled BOOLEAN DEFAULT FALSE,
    digest_frequency VARCHAR(20),    -- 'daily', 'weekly', 'monthly'
    digest_day_of_week INT,          -- 0-6 for weekly
    
    -- Rate limiting
    max_notifications_per_day INT DEFAULT 10,
    
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- User event subscriptions (explicit follows)
CREATE TABLE event_subscriptions (
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    event_id UUID REFERENCES events(id) ON DELETE CASCADE,
    subscribed_at TIMESTAMPTZ DEFAULT NOW(),
    notify_on_update BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (user_id, event_id)
);

-- Archive: Write-ups
CREATE TABLE writeups (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_id UUID REFERENCES events(id) ON DELETE SET NULL,
    challenge_name VARCHAR(500),
    category VARCHAR(100),          -- 'web', 'crypto', etc.
    author VARCHAR(255),
    team_name VARCHAR(255),
    source_url TEXT NOT NULL,
    content_url TEXT,               -- S3/MinIO if scraped
    platform VARCHAR(50),           -- 'github', 'medium', 'ctftime'
    published_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_writeups_event ON writeups(event_id);
CREATE INDEX idx_writeups_category ON writeups(category);

-- Archive: Conference materials
CREATE TABLE conference_materials (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_id UUID REFERENCES events(id) ON DELETE SET NULL,
    type VARCHAR(50),               -- 'slides', 'video', 'whitepaper', 'recording'
    title VARCHAR(500) NOT NULL,
    speaker_name VARCHAR(255),
    track VARCHAR(255),
    abstract TEXT,
    file_url TEXT,
    storage_url TEXT,               -- S3/MinIO if mirrored
    duration_minutes INT,
    published_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_materials_event ON conference_materials(event_id);
CREATE INDEX idx_materials_type ON conference_materials(type);

-- Notification log (for debugging + rate limiting)
CREATE TABLE notification_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    event_id UUID REFERENCES events(id) ON DELETE SET NULL,
    channel VARCHAR(50),            -- 'email', 'telegram', 'discord'
    status VARCHAR(20),             -- 'sent', 'failed', 'skipped'
    error_message TEXT,
    sent_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_notification_log_user_date ON notification_log(user_id, sent_at);
```

### Sample JSON Structures

**Event categories (JSONB)**:
```json
["web", "crypto", "pwn", "forensics", "reverse-engineering", "misc", "osint", "steganography", "blockchain", "ai-ml"]
```

**Restrictions (JSONB)**:
```json
{
  "academic_only": false,
  "regions_allowed": ["US", "EU", "APAC"],
  "min_rating": 0,
  "blacklisted_teams": []
}
```

**Conference tracks (JSONB)**:
```json
["keynote", "technical-briefings", "arsenal", "training", "business-hall", "villages"]
```

---

## D) ETL & SCRAPING STRATEGY

### ETL Pipeline Flow

```
┌────────────────────────────────────────────────────────────┐
│  STEP 1: COLLECTION (Scheduled via Celery)                │
├────────────────────────────────────────────────────────────┤
│  CTFtime Collector (every 6 hours)                         │
│   → GET /api/v1/events/?limit=100&start={now}&finish={+1y}│
│   → Parse JSON, extract event data                         │
│                                                             │
│  Conference Scrapers (daily)                               │
│   → Playwright headless browser                            │
│   → Check robots.txt first                                 │
│   → Extract: title, dates, location, agenda, speakers      │
│   → Respect crawl-delay (1-5 sec between requests)         │
│                                                             │
│  Write-up Scraper (weekly)                                 │
│   → Poll CTFtime /writeups                                 │
│   → GitHub API search: "ctf writeup" repos                 │
│   → Extract links, metadata                                │
└────────────────────────────────────────────────────────────┘
              ↓
┌────────────────────────────────────────────────────────────┐
│  STEP 2: NORMALIZATION                                     │
├────────────────────────────────────────────────────────────┤
│  Schema Mapping:                                           │
│   → Standardize date formats → UTC timestamps              │
│   → Normalize timezones (pytz)                             │
│   → Extract categories from description (NLP/keywords)     │
│   → Map conference tracks to CTF categories                │
│   → Geocode locations → ISO country codes                  │
│                                                             │
│  Enrichment:                                               │
│   → Estimate difficulty (heuristics: weight, prize pool)   │
│   → Infer format (keywords: "online", "hybrid", venue)     │
│   → Extract team size from rules text                      │
└────────────────────────────────────────────────────────────┘
              ↓
┌────────────────────────────────────────────────────────────┐
│  STEP 3: VALIDATION                                        │
├────────────────────────────────────────────────────────────┤
│  Pydantic Models:                                          │
│   → Required fields check (title, start_time, source)      │
│   → Type validation (URLs, timestamps, enums)              │
│   → Range checks (prize_pool >= 0, weight 0-100)           │
│                                                             │
│  Business Logic:                                           │
│   → Reject events with start_time < now (stale data)       │
│   → Flag suspicious data (e.g., duration > 30 days)        │
│   → Validate URLs are reachable (HEAD request)             │
└────────────────────────────────────────────────────────────┘
              ↓
┌────────────────────────────────────────────────────────────┐
│  STEP 4: DEDUPLICATION                                     │
├────────────────────────────────────────────────────────────┤
│  Strategy:                                                 │
│   1. Check source_id for exact match (fast path)           │
│   2. Fuzzy title matching (Levenshtein distance < 3)       │
│   3. Date overlap check (same start_time ± 1 hour)         │
│   4. URL normalization + comparison                        │
│                                                             │
│  Conflict Resolution:                                      │
│   → Prefer official sources (CTFtime > scraped data)       │
│   → Merge metadata (union of categories, keep best desc)   │
│   → Update updated_at timestamp                            │
└────────────────────────────────────────────────────────────┘
              ↓
┌────────────────────────────────────────────────────────────┐
│  STEP 5: STORAGE                                           │
├────────────────────────────────────────────────────────────┤
│  PostgreSQL:                                               │
│   → UPSERT into events table (ON CONFLICT UPDATE)          │
│   → Track last_scraped timestamp                           │
│                                                             │
│  Search Index:                                             │
│   → Push to Meilisearch (async)                            │
│   → Index: title, description, categories, location        │
│                                                             │
│  Cache Invalidation:                                       │
│   → Clear Redis cache for affected event pages             │
└────────────────────────────────────────────────────────────┘
              ↓
┌────────────────────────────────────────────────────────────┐
│  STEP 6: NOTIFICATION TRIGGERING                           │
├────────────────────────────────────────────────────────────┤
│  Event Matching:                                           │
│   → Query user_preferences for matching filters            │
│   → Score events (0-100) based on preference alignment     │
│   → Apply rate limits (max_notifications_per_day)          │
│                                                             │
│  Scheduling:                                               │
│   → Queue notifications via Celery (delay = days_before)   │
│   → Dedup: check notification_log for recent sends         │
└────────────────────────────────────────────────────────────┘
```

### Scraping Best Practices (Ethical + Robust)

#### Robots.txt Compliance
```python
# Example: Check robots.txt before scraping
from urllib.robotparser import RobotFileParser

def check_robots(base_url: str, user_agent: str = "CTFTrackerBot/1.0") -> bool:
    rp = RobotFileParser()
    rp.set_url(f"{base_url}/robots.txt")
    rp.read()
    return rp.can_fetch(user_agent, base_url)
```

**Requirements:**
- Read `robots.txt` for every domain
- Respect `Disallow` directives (do NOT scrape blocked paths)
- Honor `Crawl-delay` (default: 5 seconds if not specified)
- Use descriptive User-Agent: `CTFTrackerBot/1.0 (+https://yoursite.com/bot-info)`

#### Rate Limiting & Polite Crawling

**Implementation:**
```python
import time
import random
from ratelimit import limits, sleep_and_retry

@sleep_and_retry
@limits(calls=1, period=5)  # Max 1 request per 5 seconds
def fetch_page(url: str):
    # Add jitter to avoid synchronized bursts
    time.sleep(random.uniform(0, 1))
    response = requests.get(url, timeout=10)
    return response

# Exponential backoff on 429 (Too Many Requests)
def fetch_with_retry(url: str, max_retries: int = 3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url)
            if response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', 60))
                time.sleep(retry_after * (2 ** attempt))  # Exponential backoff
                continue
            return response
        except requests.RequestException as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)
```

**Best Practices:**
- **Default rate**: 1 request per 5 seconds for HTML scraping
- **CTFtime API**: 1 request per second (conservative estimate)
- **Crawl during off-peak hours** (00:00-06:00 UTC for US sites)
- **Cache aggressively**: Store raw HTML for 24h, avoid re-fetching
- **Monitor 429 responses**: Implement exponential backoff

#### Anti-Breakage Strategies

**Selector Resilience:**
```python
# Bad: Fragile CSS selector
title = soup.select_one('div.container > div:nth-child(3) > h2').text

# Good: Multiple fallback selectors
TITLE_SELECTORS = [
    'h1.event-title',
    '[data-testid="event-title"]',
    'h1',  # Last resort
]

def extract_title(soup):
    for selector in TITLE_SELECTORS:
        elem = soup.select_one(selector)
        if elem and elem.text.strip():
            return elem.text.strip()
    return None
```

**Schema Validation:**
```python
from pydantic import BaseModel, HttpUrl, validator
from datetime import datetime

class EventSchema(BaseModel):
    title: str
    start_time: datetime
    end_time: datetime
    url: HttpUrl
    categories: list[str] = []
    
    @validator('end_time')
    def end_after_start(cls, v, values):
        if 'start_time' in values and v < values['start_time']:
            raise ValueError('end_time must be after start_time')
        return v
```

#### Failure Modes & Mitigations

| Failure Mode | Detection | Mitigation |
|--------------|-----------|------------|
| **Selector changed** | Empty extraction | Alert + manual review; version selectors |
| **Rate limit hit** | HTTP 429 | Exponential backoff; reduce frequency |
| **Timeout** | RequestException | Retry with backoff; longer timeout |
| **Invalid data** | Pydantic ValidationError | Log + skip; alert if >5% failure rate |
| **Source unavailable** | DNS/connection error | Retry later; use cached data |
| **Encoding issues** | UnicodeDecodeError | Try multiple encodings; default to UTF-8 |

---

## E) CALENDAR INTEGRATION

### ICS Feed Generation (Recommended Approach for MVP)

**Why ICS over Direct API Integration:**
- **Universal compatibility**: Works with Google Calendar, Apple Calendar, Outlook, Thunderbird
- **No API keys required**: No OAuth2 flow, rate limits, or maintenance burden
- **User control**: Users subscribe to URL, manage subscription in their calendar app
- **Automatic updates**: Calendar apps re-fetch ICS periodically (default: 1-24h)

**Implementation (RFC 5545 compliant):**

```python
from icalendar import Calendar, Event, vText
from datetime import datetime, timedelta
import pytz

def generate_ics_feed(user_id: str, events: list[Event]) -> str:
    cal = Calendar()
    
    # Required calendar properties
    cal.add('prodid', '-//CTF Tracker//ctftracker.io//')
    cal.add('version', '2.0')
    cal.add('calscale', 'GREGORIAN')
    cal.add('method', 'PUBLISH')
    cal.add('x-wr-calname', 'CTF & Security Events')
    cal.add('x-wr-timezone', 'UTC')
    cal.add('x-wr-caldesc', 'Personalized cybersecurity events')
    
    for event_data in events:
        event = Event()
        
        # Required fields (RFC 5545)
        event.add('uid', f"{event_data.id}@ctftracker.io")
        event.add('dtstamp', datetime.now(pytz.utc))
        event.add('dtstart', event_data.start_time)
        event.add('dtend', event_data.end_time)
        event.add('summary', event_data.title)
        
        # Optional but recommended
        event.add('description', event_data.description or '')
        event.add('location', event_data.location_city or 'Online')
        event.add('url', event_data.url)
        event.add('status', 'CONFIRMED')
        event.add('categories', event_data.categories)  # Comma-separated
        
        # Alarms (reminders)
        from icalendar import Alarm
        alarm = Alarm()
        alarm.add('action', 'DISPLAY')
        alarm.add('description', f"Reminder: {event_data.title}")
        alarm.add('trigger', timedelta(days=-7))  # 7 days before
        event.add_component(alarm)
        
        # Last-modified for update detection
        event.add('last-modified', event_data.updated_at)
        
        cal.add_component(event)
    
    return cal.to_ical().decode('utf-8')
```

**Endpoint Implementation:**
```python
@app.get("/api/calendar.ics")
async def get_calendar_feed(
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Fetch user preferences
    prefs = db.query(UserPreferences).filter_by(user_id=user_id).first()
    
    # Query matching events
    events = filter_events_by_preferences(db, prefs)
    
    # Generate ICS
    ics_data = generate_ics_feed(user_id, events)
    
    return Response(
        content=ics_data,
        media_type="text/calendar",
        headers={
            "Content-Disposition": "attachment; filename=ctf-events.ics",
            "Cache-Control": "private, max-age=3600",  # 1-hour cache
            "ETag": hashlib.md5(ics_data.encode()).hexdigest()  # For update detection
        }
    )
```

### Timezone & DST Handling

**Best Practices:**
- Store all times in UTC (PostgreSQL `TIMESTAMPTZ`)
- Convert to event's local timezone in ICS using `TZID` parameter
- Include `VTIMEZONE` component for each timezone used
- Use `pytz` library for accurate DST transitions

```python
# Example: Add VTIMEZONE for New York
from icalendar import Timezone

def add_timezone(cal, tzname: str):
    tz = pytz.timezone(tzname)
    timezone = Timezone()
    timezone.add('tzid', tzname)
    # ... add standard/daylight components (complex, use library)
    cal.add_component(timezone)
```

### Update Detection (ETag + Last-Modified)

**How calendar clients detect changes:**
1. Client sends `GET /calendar.ics` with `If-None-Match: {previous_etag}`
2. Server compares ETags; if identical → `304 Not Modified`
3. If different → `200 OK` with new ICS data

**Implementation:**
```python
@app.get("/api/calendar.ics")
async def get_calendar_feed(request: Request, user_id: str):
    ics_data = generate_ics_feed(user_id, events)
    etag = hashlib.md5(ics_data.encode()).hexdigest()
    
    # Check If-None-Match header
    if request.headers.get("If-None-Match") == etag:
        return Response(status_code=304)
    
    return Response(
        content=ics_data,
        media_type="text/calendar",
        headers={"ETag": etag}
    )
```

### Alternative: Direct Calendar API Integration (Nice-to-Have)

**Google Calendar API:**
- **Pros**: Real-time sync, bi-directional (user can edit events), notifications
- **Cons**: Requires OAuth2 flow, rate limits (1000 req/user/day), complex setup
- **Use case**: Premium feature for power users

**CalDAV:**
- **Pros**: Self-hosted calendars (Nextcloud, etc.), standardized protocol
- **Cons**: Server-side complexity, authentication challenges
- **Use case**: Enterprise deployments

**Recommendation for MVP:**
- **Start with ICS feed** (universal, simple, no API keys)
- **Add Google Calendar integration** in v2 for premium users
- **Never implement CalDAV** unless enterprise clients demand it

---

## F) NOTIFICATION + PERSONALIZATION SPEC

### User Preference Model

```python
from pydantic import BaseModel, Field

class UserPreferenceSchema(BaseModel):
    # Event filters
    categories: list[str] = Field(
        default=[],
        description="CTF categories: web, crypto, pwn, forensics, reverse, misc, osint, blockchain"
    )
    formats: list[str] = Field(
        default=["jeopardy", "attack-defense", "online", "onsite", "hybrid"],
        description="Event formats"
    )
    difficulty_levels: list[str] = Field(
        default=["beginner", "intermediate", "advanced"],
        description="Difficulty preference"
    )
    regions: list[str] = Field(
        default=[],
        description="ISO country codes: US, GB, DE, CN, etc."
    )
    event_types: list[str] = Field(
        default=["ctf", "conference"],
        description="Event types to track"
    )
    team_size_min: int = Field(default=1, ge=1, le=100)
    team_size_max: int = Field(default=10, ge=1, le=100)
    
    # Date filters
    date_range_days: int = Field(
        default=90,
        description="Look ahead window (days from today)"
    )
    
    # Notification settings
    notify_email: bool = True
    notify_telegram: bool = False
    notify_discord: bool = False
    notify_push: bool = False  # Web Push API
    
    # Timing
    notify_days_before: int = Field(default=7, ge=1, le=30)
    notify_on_registration_open: bool = True
    notify_on_schedule_published: bool = False
    notify_on_writeups_published: bool = True
    
    # Rate limiting
    max_notifications_per_day: int = Field(default=5, ge=1, le=50)
    
    # Digest mode
    digest_enabled: bool = False
    digest_frequency: str = Field(default="weekly", regex="^(daily|weekly|monthly)$")
    digest_day_of_week: int = Field(default=0, ge=0, le=6)  # 0=Monday
    digest_hour_utc: int = Field(default=9, ge=0, le=23)
```

### Event Scoring Formula

**Goal:** Rank events 0-100 based on user preference alignment

```python
def score_event(event: Event, prefs: UserPreferenceSchema) -> float:
    score = 0.0
    
    # Category match (40% weight)
    if prefs.categories:
        category_overlap = len(set(event.categories) & set(prefs.categories))
        category_score = (category_overlap / len(prefs.categories)) * 40
        score += category_score
    else:
        score += 40  # No preference = all categories match
    
    # Format match (20% weight)
    if event.format in prefs.formats:
        score += 20
    
    # Difficulty match (15% weight)
    if event.difficulty in prefs.difficulty_levels:
        score += 15
    
    # Region match (10% weight)
    if not prefs.regions or event.location_country in prefs.regions:
        score += 10
    
    # Team size match (10% weight)
    if event.team_size_min and event.team_size_max:
        if prefs.team_size_min <= event.team_size_max and prefs.team_size_max >= event.team_size_min:
            score += 10
    else:
        score += 10  # Unknown team size = assume match
    
    # Event type match (5% weight)
    if event.type in prefs.event_types:
        score += 5
    
    return min(score, 100.0)
```

### Notification Channels

#### 1. Email Notifications

**Provider:** SendGrid (free tier: 100 emails/day)

```python
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email_notification(user_email: str, event: Event):
    message = Mail(
        from_email='notifications@ctftracker.io',
        to_emails=user_email,
        subject=f'Upcoming: {event.title} in {days_until} days',
        html_content=render_template('email/event_notification.html', event=event)
    )
    
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    
    log_notification(user_id, event.id, 'email', response.status_code)
```

**Template (HTML):**
```html
<h2>{{ event.title }}</h2>
<p><strong>When:</strong> {{ event.start_time.strftime('%B %d, %Y at %H:%M UTC') }}</p>
<p><strong>Format:</strong> {{ event.format }}</p>
<p><strong>Categories:</strong> {{ ', '.join(event.categories) }}</p>
<p>{{ event.description[:200] }}...</p>
<a href="{{ event.url }}" style="background: #007bff; color: white; padding: 10px 20px;">Register Now</a>
<p style="font-size: 12px; color: #666;">
  <a href="{{ unsubscribe_url }}">Unsubscribe</a> | 
  <a href="{{ preferences_url }}">Manage Preferences</a>
</p>
```

#### 2. Telegram Bot

**Setup:**
1. Create bot via @BotFather → get bot token
2. User sends `/start` to bot → bot stores `chat_id`
3. User links Telegram in app settings

```python
import telegram

async def send_telegram_notification(chat_id: str, event: Event):
    bot = telegram.Bot(token=os.environ['TELEGRAM_BOT_TOKEN'])
    
    message = f"""
🚀 *{event.title}*

📅 {event.start_time.strftime('%B %d, %Y at %H:%M UTC')}
🏷️ {', '.join(event.categories)}
🌐 {event.format}

{event.description[:150]}...

[Register]({event.url}) | [More Info](https://ctftracker.io/events/{event.id})
    """
    
    await bot.send_message(
        chat_id=chat_id,
        text=message,
        parse_mode='Markdown',
        disable_web_page_preview=False
    )
```

#### 3. Discord Webhook

**Setup:** User creates webhook in Discord server settings → pastes URL in app

```python
from discord_webhook import DiscordWebhook, DiscordEmbed

def send_discord_notification(webhook_url: str, event: Event):
    webhook = DiscordWebhook(url=webhook_url)
    
    embed = DiscordEmbed(
        title=event.title,
        description=event.description[:200],
        color='03b2f8',
        url=f"https://ctftracker.io/events/{event.id}"
    )
    embed.add_embed_field(name="Start Time", value=event.start_time.strftime('%B %d, %Y at %H:%M UTC'))
    embed.add_embed_field(name="Format", value=event.format)
    embed.add_embed_field(name="Categories", value=', '.join(event.categories))
    embed.set_footer(text="CTF Tracker")
    embed.set_timestamp()
    
    webhook.add_embed(embed)
    response = webhook.execute()
```

#### 4. Web Push (Progressive Web App)

**Setup:** Service worker + Push API (requires HTTPS)

```javascript
// Frontend: Request permission
async function subscribeToPush() {
  const registration = await navigator.serviceWorker.ready;
  const subscription = await registration.pushManager.subscribe({
    userVisibleOnly: true,
    applicationServerKey: urlBase64ToUint8Array(VAPID_PUBLIC_KEY)
  });
  
  // Send subscription to backend
  await fetch('/api/push/subscribe', {
    method: 'POST',
    body: JSON.stringify(subscription),
    headers: {'Content-Type': 'application/json'}
  });
}
```

```python
# Backend: Send push notification
from pywebpush import webpush, WebPushException

def send_push_notification(subscription_info: dict, event: Event):
    try:
        webpush(
            subscription_info=subscription_info,
            data=json.dumps({
                'title': f'Upcoming: {event.title}',
                'body': f'Starts in {days_until} days',
                'icon': '/icon-192x192.png',
                'url': f'/events/{event.id}'
            }),
            vapid_private_key=os.environ['VAPID_PRIVATE_KEY'],
            vapid_claims={"sub": "mailto:admin@ctftracker.io"}
        )
    except WebPushException as e:
        if e.response.status_code == 410:  # Subscription expired
            delete_subscription(subscription_info)
```

### Anti-Spam Rules

**Rate Limiting:**
```python
def can_send_notification(user_id: str, event_id: str) -> bool:
    # Check daily limit
    today_count = db.query(NotificationLog).filter(
        NotificationLog.user_id == user_id,
        NotificationLog.sent_at >= datetime.now() - timedelta(days=1)
    ).count()
    
    if today_count >= user_prefs.max_notifications_per_day:
        return False
    
    # Check duplicate (same event in last 7 days)
    recent_duplicate = db.query(NotificationLog).filter(
        NotificationLog.user_id == user_id,
        NotificationLog.event_id == event_id,
        NotificationLog.sent_at >= datetime.now() - timedelta(days=7)
    ).first()
    
    if recent_duplicate:
        return False
    
    return True
```

**Priority Scoring:**
- High (90-100): Immediate notification
- Medium (70-89): Daily digest
- Low (50-69): Weekly digest
- Very Low (<50): Monthly digest or suppress

**Digest Mode:**
```python
async def send_weekly_digest(user_id: str):
    # Get events from past week above threshold (score >= 70)
    events = get_pending_notifications(user_id, min_score=70)
    
    if not events:
        return  # No digest if empty
    
    html_content = render_template('email/weekly_digest.html', events=events)
    send_email(user.email, "Your Weekly CTF Digest", html_content)
    
    # Mark as sent
    mark_notifications_sent(user_id, [e.id for e in events])
```

---

## G) SECURITY / THREAT MODEL + SECOPS CHECKLIST

### Threat Model

#### T1: Scraping Infrastructure Abuse

**Attack:** Attacker floods scraper targets with requests from our IPs, causing us to be banned/blacklisted

**Mitigations:**
- Distribute scraping across multiple IPs (proxy rotation)
- Implement per-domain rate limits (hardcoded in scraper config)
- Monitor 429/403 responses; auto-pause scraper on detection
- Allowlist our IPs with conference organizers (for high-value targets)

#### T2: SSRF (Server-Side Request Forgery)

**Attack:** User-provided URLs (event registration links, write-up URLs) point to internal services (localhost, AWS metadata, etc.)

**Mitigations:**
```python
from ipaddress import ip_address, ip_network

BLOCKED_NETWORKS = [
    ip_network('127.0.0.0/8'),      # Localhost
    ip_network('10.0.0.0/8'),       # Private
    ip_network('172.16.0.0/12'),    # Private
    ip_network('192.168.0.0/16'),   # Private
    ip_network('169.254.0.0/16'),   # Link-local
]

def is_safe_url(url: str) -> bool:
    parsed = urlparse(url)
    
    # Block non-HTTP(S) schemes
    if parsed.scheme not in ['http', 'https']:
        return False
    
    # Resolve hostname to IP
    try:
        ip = ip_address(socket.gethostbyname(parsed.hostname))
    except Exception:
        return False  # Unresolvable = unsafe
    
    # Check against blocked networks
    for network in BLOCKED_NETWORKS:
        if ip in network:
            return False
    
    return True
```

#### T3: Injection via Scraped Content

**Attack:** Malicious event organizer injects XSS/SQLi payloads in event descriptions

**Mitigations:**
- **Input sanitization:** Use `bleach` library to strip HTML tags from scraped content
- **Output encoding:** Always escape user-generated content in templates (Jinja2 auto-escapes)
- **Parameterized queries:** Use ORM (SQLAlchemy) exclusively; no raw SQL with user input
- **Content Security Policy (CSP):** Set restrictive CSP headers

```python
import bleach

ALLOWED_TAGS = ['p', 'b', 'i', 'u', 'a', 'br', 'ul', 'ol', 'li']
ALLOWED_ATTRS = {'a': ['href', 'title']}

def sanitize_html(content: str) -> str:
    return bleach.clean(
        content,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRS,
        strip=True
    )
```

#### T4: Supply Chain Risks (Dependencies)

**Attack:** Compromised PyPI package injects malware into scraper

**Mitigations:**
- Pin exact versions in `requirements.txt` (not `>=` ranges)
- Use `pip-audit` in CI/CD to detect known vulnerabilities
- Review dependency changes in PRs (especially for scraping libs)
- Consider `safety` + `Snyk` for continuous monitoring

```bash
# requirements.txt
fastapi==0.104.1
pydantic==2.5.0
playwright==1.40.0
# ... (exact versions, no ~= or >=)
```

#### T5: API Key Leaks

**Attack:** Hardcoded secrets in code → leaked via Git history

**Mitigations:**
- **Never commit secrets:** Use environment variables exclusively
- **Git hooks:** Pre-commit hook to scan for secrets (e.g., `detect-secrets`)
- **Secrets management:** Use AWS Secrets Manager / HashiCorp Vault in production
- **Rotate keys:** Quarterly rotation of SendGrid, Telegram, Discord tokens

```python
# Good: Load from environment
SENDGRID_API_KEY = os.environ['SENDGRID_API_KEY']

# Bad: Hardcoded (NEVER DO THIS)
# SENDGRID_API_KEY = 'SG.abc123...'
```

#### T6: Account Takeover

**Attack:** Weak passwords, credential stuffing, session hijacking

**Mitigations:**
- **Password hashing:** bcrypt with cost factor 12
- **Email verification:** Send confirmation link on registration
- **Rate limiting:** Max 5 login attempts per IP per 15 minutes
- **Session management:** JWT with short expiry (15 min access token, 7 day refresh token)
- **2FA (optional):** TOTP via Google Authenticator

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
```

### SecOps Checklist

#### Logging & Monitoring

```python
import structlog
from pythonjsonlogger import jsonlogger

# Structured logging (JSON format for log aggregation)
logger = structlog.get_logger()

# Log all API requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    logger.info(
        "api_request",
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        duration_ms=int(duration * 1000),
        user_agent=request.headers.get("user-agent"),
        ip=request.client.host
    )
    return response
```

**What to Log:**
- API requests (method, path, status, duration, IP, user ID)
- Scraper runs (success/failure, duration, records collected)
- Notification sends (channel, user, event, status)
- Auth events (login, logout, password reset, failures)
- Errors (exceptions with stack traces)

**Monitoring Alerts:**
- Scraper failure rate > 10% (Slack/email)
- API error rate > 5% (PagerDuty)
- Notification delivery failure > 20%
- Disk usage > 80%

#### Rate Limiting (Application Level)

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/api/auth/login")
@limiter.limit("5/minute")  # Max 5 attempts per IP per minute
async def login(request: Request, credentials: LoginSchema):
    # ... login logic
```

**Rate Limits (Recommended):**
- `/api/auth/login`: 5 req/min per IP
- `/api/events`: 60 req/min per IP (100 if authenticated)
- `/api/preferences`: 10 req/min per user
- `/api/calendar.ics`: 10 req/hour per user

#### WAF (Web Application Firewall)

**Cloudflare Free Tier:**
- DDoS protection (L3/L4/L7)
- Rate limiting (5 rules on free tier)
- Bot detection
- SSL/TLS termination

**Configuration:**
```yaml
# Cloudflare WAF rules (via Terraform)
resource "cloudflare_rate_limit" "api_login" {
  zone_id = var.zone_id
  threshold = 5
  period = 60
  action {
    mode = "challenge"  # CAPTCHA
    timeout = 3600
  }
  match {
    request {
      url_pattern = "*/api/auth/login"
    }
  }
}
```

#### Secrets Management

**Development:**
```bash
# .env file (NEVER commit)
DATABASE_URL=postgresql://user:pass@localhost/ctftracker
SENDGRID_API_KEY=SG.abc123...
JWT_SECRET=random_64_char_string
```

**Production (AWS Secrets Manager):**
```python
import boto3

def get_secret(secret_name: str) -> str:
    client = boto3.client('secretsmanager', region_name='us-east-1')
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])

# Usage
DB_CONFIG = get_secret('prod/database')
SENDGRID_KEY = get_secret('prod/sendgrid')['api_key']
```

#### Abuse Prevention

**Account Creation:**
- CAPTCHA (hCaptcha) on registration
- Email verification required before access
- Max 3 accounts per email domain per day

**Notification Spam:**
- Users can't send >50 notifications/day
- Detect rapid preference changes (rate limit: 10 updates/hour)
- Automatic suspension if abuse detected (manual review)

**API Abuse:**
- Block IPs with >100 4xx errors in 5 minutes
- JWT blacklist for compromised tokens
- Honeypot endpoints to detect scrapers

---

## H) MVP ROADMAP (Week-by-Week)

### Week 1: Foundation + CTFtime Integration

**Goals:** Core backend + CTFtime API integration

**Tasks:**
- [ ] Set up FastAPI project structure (models, routers, services)
- [ ] PostgreSQL schema creation + migrations (Alembic)
- [ ] User authentication (JWT, bcrypt, registration, login)
- [ ] CTFtime API collector (Celery task for `/api/v1/events`)
- [ ] Basic event storage + deduplication logic
- [ ] Redis setup (caching + task queue)

**Deliverable:** API can fetch & store CTFtime events; users can register/login

---

### Week 2: Frontend + Event Discovery

**Goals:** User-facing web app + search

**Tasks:**
- [ ] Next.js setup (pages, components, API routes)
- [ ] Event list page (table view with filters: category, format, date)
- [ ] Event detail page (description, registration link, countdown timer)
- [ ] Search implementation (Meilisearch integration)
- [ ] User preferences page (form to set categories, regions, etc.)
- [ ] Calendar view (FullCalendar.js integration)

**Deliverable:** Users can browse, search, and filter CTFtime events

---

### Week 3: Notifications + Conference Scraping

**Goals:** Email notifications + first conference scraper

**Tasks:**
- [ ] SendGrid integration (email templates, send function)
- [ ] Notification matching logic (score events, filter by prefs)
- [ ] Celery scheduled task: daily notification check
- [ ] ICS feed generation endpoint (`/api/calendar.ics`)
- [ ] Conference scraper prototype (Black Hat OR DEF CON)
  - [ ] robots.txt checker
  - [ ] Playwright scraper (event title, dates, location)
  - [ ] Schema validation + storage
- [ ] Rate limiting middleware (SlowAPI)

**Deliverable:** Users receive email 7 days before matching events; can subscribe to ICS feed

---

### Week 4: Archive + Polish

**Goals:** Write-up archive + MVP launch prep

**Tasks:**
- [ ] Write-up scraper (CTFtime /writeups page)
- [ ] GitHub API integration (search for "ctf-writeup" repos)
- [ ] Archive UI (searchable list of write-ups, filter by event/category)
- [ ] Admin dashboard (scraper status, error logs, user metrics)
- [ ] Security hardening:
  - [ ] SSRF protection on user-provided URLs
  - [ ] Input sanitization (bleach)
  - [ ] CSP headers
  - [ ] HTTPS enforcement (Cloudflare)
- [ ] Documentation (README, API docs via Swagger UI)
- [ ] Deployment (Docker Compose → DigitalOcean/AWS)

**Deliverable:** MVP launched with CTFtime + 1 conference + write-up archive

---

### Post-MVP (v1.1 - v1.3)

**v1.1 (Weeks 5-6):**
- Telegram bot integration
- Discord webhook support
- Add 3 more conference scrapers (RSA, BSides, OWASP)

**v1.2 (Weeks 7-8):**
- Conference materials archive (slides, videos)
- YouTube integration (Black Hat/DEF CON channels)
- User dashboard (upcoming events, past notifications)

**v1.3 (Weeks 9-10):**
- Advanced filters (prize pool, team size, difficulty)
- Event recommendations (ML-based scoring)
- Mobile app (React Native or PWA)
- Community features (user write-up submissions, event reviews)

---

## I) TECH STACK RECOMMENDATION

### Backend Stack

**Framework:** FastAPI (Python 3.11+)
- **Rationale:** Type-safe with Pydantic, async support, auto-generated OpenAPI docs, fastest Python framework
- **Alternatives:** Flask (simpler but lacks async), Django (overkill for API-only), NestJS (TypeScript, more verbose)

**Database:** PostgreSQL 15+ with JSONB
- **Rationale:** ACID compliance, excellent JSON support, full-text search, proven at scale
- **Schema:** Use Alembic for migrations
- **Connection pooling:** SQLAlchemy with asyncpg driver

**Cache & Queue:** Redis 7+
- **Use cases:** 
  - Cache: API responses (60s TTL), session storage, rate limiting counters
  - Queue: Celery task broker for scrapers and notifications
- **Configuration:** Separate Redis instances for cache (eviction) vs queue (persistent)

**Task Scheduler:** Celery + Redis
- **Tasks:** 
  - `scrape_ctftime`: Every 6 hours
  - `scrape_conferences`: Daily at 02:00 UTC
  - `send_notifications`: Hourly check
  - `cleanup_old_events`: Weekly
- **Beat scheduler:** Celery Beat for cron-like scheduling

**Search Engine:** Meilisearch
- **Rationale:** Lightweight, typo-tolerant, faceted search, <100ms latency, easier than Elasticsearch for MVP
- **Indexes:** Events, write-ups, conference materials
- **Fallback:** PostgreSQL full-text search if self-hosting isn't feasible

### Scraping Stack

**HTTP Client:** httpx (async) + requests (sync fallback)
- **Configuration:** 10s timeout, automatic retries with exponential backoff
- **User-Agent:** `CTFTrackerBot/1.0 (+https://ctftracker.io/bot)`

**HTML Parsing:** BeautifulSoup4 + lxml parser
- **Fallback:** Playwright for JavaScript-heavy sites (Black Hat, DEFCON)
- **Playwright:** Headless Chromium for dynamic content rendering

**robots.txt:** urllib.robotparser
- **Enforcement:** Check before every scrape session, cache for 24h

**Rate Limiting:** Custom decorator + Redis counters
```python
def rate_limit(calls: int, period: int):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key = f"ratelimit:{func.__name__}"
            count = await redis.incr(key)
            if count == 1:
                await redis.expire(key, period)
            if count > calls:
                raise RateLimitError(f"Max {calls} calls per {period}s")
            return await func(*args, **kwargs)
        return wrapper
    return decorator
```

### Frontend Stack

**Framework:** Next.js 14+ (App Router)
- **Rationale:** React-based, SSR for SEO, API routes, excellent DX
- **Styling:** Tailwind CSS (utility-first, fast prototyping)
- **Components:** shadcn/ui (accessible, customizable)

**State Management:** React Context + SWR (for API data fetching)
- **SWR:** Automatic revalidation, caching, optimistic updates

**Calendar UI:** FullCalendar.js
- **Features:** Month/week/day views, event click handlers, external drag-drop

**Authentication:** JWT stored in httpOnly cookies
- **Flow:** Login → server sets cookie → Next.js middleware validates on protected routes

### Infrastructure

**Hosting (MVP):**
- **Option 1 (Budget):** DigitalOcean App Platform
  - $12/mo: 1 CPU, 1GB RAM (backend)
  - $7/mo: PostgreSQL managed DB (1GB)
  - $0: Cloudflare CDN (free tier)
  - **Total:** ~$20/month
  
- **Option 2 (Scalable):** AWS
  - ECS Fargate (containerized backend)
  - RDS PostgreSQL (t3.micro)
  - ElastiCache Redis
  - S3 for static assets
  - **Total:** ~$50-80/month

**CI/CD:** GitHub Actions
```yaml
name: Deploy
on: push: branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: pytest
      - name: Build Docker image
        run: docker build -t ctftracker:latest .
      - name: Deploy to production
        run: # ... deployment script
```

**Monitoring:**
- **APM:** Sentry (error tracking, free tier: 5k events/month)
- **Logs:** Grafana Loki or CloudWatch Logs
- **Metrics:** Prometheus + Grafana (self-hosted) or DataDog (paid)

### Security Stack

**WAF:** Cloudflare (free tier)
- DDoS protection, rate limiting, bot detection
- SSL/TLS termination (automatic certificates)

**Secrets:** AWS Secrets Manager (production) / dotenv (development)

**Authentication:** OAuth2 + JWT
- **Providers:** Google, GitHub (via Authlib library)
- **Tokens:** 15-min access token (JWT), 7-day refresh token (stored in DB)

**Input Validation:** Pydantic models (backend) + Zod schemas (frontend)

**Dependencies:** Snyk + pip-audit (weekly scans in CI/CD)

---

## J) CITATIONS & REFERENCES

### CTF Data Sources

1. **CTFtime API Documentation**  
   https://ctftime.org/api/  
   (Accessed: 2026-01-19) - Official API for events, teams, ratings

2. **CTFtime Terms of Service**  
   https://ctftime.org/about/  
   "API is provided for data analysis and mobile applications only"

3. **GitHub CTF Write-ups Archive (2015-2018)**  
   https://github.com/ctfs/write-ups-2015  
   https://github.com/ctfs/write-ups-2016  
   https://github.com/ctfs/write-ups-2017  
   https://github.com/ctfs/write-ups-2018  
   Community-maintained historical archives

### Conference Sources

4. **Black Hat Official Site**  
   https://www.blackhat.com/  
   Conference schedules, CFP, speaker info

5. **Black Hat Archives**  
   https://www.blackhat.com/html/archives.html  
   Historical presentations (1997-present)

6. **DEF CON Media Server**  
   https://media.defcon.org/  
   Talks, slides, village materials

7. **RSA Conference**  
   https://www.rsaconference.com/  
   Major enterprise security conference

8. **OWASP Events Calendar**  
   https://owasp.org/events/  
   Global application security events

9. **BSides Security**  
   http://www.securitybsides.com/  
   Community-driven local security conferences

10. **Chaos Computer Club (CCC)**  
    https://www.ccc.de/  
    Annual Congress (Dec 27-30)

11. **InfoCon Archive**  
    https://infocon.org/  
    Multi-conference video/document archive

### Technical Standards

12. **RFC 5545 - Internet Calendaring and Scheduling Core Object Specification (iCalendar)**  
    https://datatracker.ietf.org/doc/html/rfc5545  
    iCal format specification for calendar feeds

13. **robots.txt Specification**  
    https://www.robotstxt.org/  
    Standard for web crawler exclusion

14. **Web Scraping Best Practices (ScrapingBee)**  
    https://www.scrapingbee.com/blog/web-scraping-best-practices/  
    Ethical scraping, rate limiting, robots.txt compliance

### Security References

15. **OWASP SSRF Prevention Cheat Sheet**  
    https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html  
    Preventing SSRF attacks in scraping infrastructure

16. **OWASP Input Validation Cheat Sheet**  
    https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html  
    Sanitizing scraped content, XSS prevention

17. **bcrypt Password Hashing**  
    https://github.com/pyca/bcrypt  
    Secure password hashing library

### API Documentation

18. **SendGrid Email API**  
    https://docs.sendgrid.com/  
    Transactional email service (100 emails/day free)

19. **Telegram Bot API**  
    https://core.telegram.org/bots/api  
    Bot creation, message sending

20. **Discord Webhooks**  
    https://discord.com/developers/docs/resources/webhook  
    Sending messages to Discord channels

21. **Google Calendar API**  
    https://developers.google.com/calendar/api  
    Calendar event management (for v2 integration)

22. **YouTube Data API v3**  
    https://developers.google.com/youtube/v3  
    Fetching conference videos

### Libraries & Frameworks

23. **FastAPI Documentation**  
    https://fastapi.tiangolo.com/  
    Modern Python web framework

24. **Celery Documentation**  
    https://docs.celeryq.dev/  
    Distributed task queue

25. **Playwright Python**  
    https://playwright.dev/python/  
    Browser automation for scraping

26. **Meilisearch Documentation**  
    https://www.meilisearch.com/docs  
    Lightweight search engine

27. **Next.js Documentation**  
    https://nextjs.org/docs  
    React framework for production

28. **icalendar Library (Python)**  
    https://icalendar.readthedocs.io/  
    iCal feed generation

29. **Pydantic Documentation**  
    https://docs.pydantic.dev/  
    Data validation with Python type hints

30. **SQLAlchemy ORM**  
    https://docs.sqlalchemy.org/  
    PostgreSQL ORM with async support

### Community Resources

31. **APAC Security Conferences (GitHub)**  
    https://github.com/Infosec-Community/APAC-Conferences  
    Community-curated conference list

32. **Base Cyber Security Calendar**  
    https://basecybersecurity.com/cyber-security-events-2025/  
    Aggregated European security events

---

## K) ADDITIONAL RECOMMENDATIONS

### Data Quality & Validation

**Event Verification System:**
- Flag events as `verified=true` after manual review or high confidence (official source)
- Display trust indicator to users (verified badge)
- Allow community reporting of incorrect data (report button → admin queue)

**Conflict Resolution:**
- If multiple sources report same event with conflicting data, prefer:
  1. Official event website
  2. CTFtime (for CTFs)
  3. Community aggregators (last resort)

### Performance Optimization

**Database Indexing:**
```sql
-- Composite indexes for common queries
CREATE INDEX idx_events_upcoming ON events(start_time) WHERE start_time > NOW();
CREATE INDEX idx_events_category_date ON events USING GIN(categories) WHERE start_time > NOW();
```

**Caching Strategy:**
- Event list page: 5-minute cache (Redis)
- Event detail page: 1-hour cache, invalidate on update
- Search results: 10-minute cache with cache keys per query

**Pagination:**
- Event list: 50 events per page (cursor-based pagination)
- Write-ups: 100 per page (offset pagination acceptable for archive)

### Accessibility

**WCAG 2.1 AA Compliance:**
- Semantic HTML (proper heading hierarchy)
- ARIA labels for interactive elements
- Keyboard navigation (tab order, focus indicators)
- Color contrast ratio ≥ 4.5:1
- Alt text for images (event logos, speaker photos)

### Legal Compliance

**GDPR (EU users):**
- Cookie consent banner (analytics, preferences)
- Data export feature (user can download all their data as JSON)
- Right to deletion (account deletion → cascade delete all user data)
- Privacy policy (what data is collected, how it's used, retention period)

**Copyright Compliance:**
- Write-ups: Link to original sources, never copy full content
- Conference materials: Mirror only if license permits, otherwise hotlink
- Event descriptions: Respect copyright, paraphrase when necessary
- Disclaimer: "All event data provided as-is; verify with official sources"

### Community Features (Post-MVP)

**User Contributions:**
- Submit missing events (admin approval queue)
- Upload write-ups (with credit + link to original)
- Rate events (1-5 stars) + review system
- Team formation (find teammates for CTFs)

**Social Features:**
- Follow other users (see their event calendar)
- Event discussion threads (comments on event pages)
- Share event to Twitter/LinkedIn (Open Graph meta tags)

### Metrics & Analytics

**Track for Product Decisions:**
- Event view counts (identify popular categories)
- Notification click-through rate (email → event page)
- User retention (weekly active users)
- Scraper success rate (by source)
- Search query analysis (improve tagging)

**Privacy-Respecting Analytics:**
- Use Plausible.io or Umami (GDPR-compliant, no cookies)
- Aggregate metrics only (no individual user tracking)

---

## SUMMARY: MVP Success Criteria

**Technical Milestones:**
- [ ] 100+ CTF events indexed from CTFtime
- [ ] 20+ conferences from 3+ sources
- [ ] <200ms average API response time
- [ ] 99% uptime (Cloudflare + health checks)
- [ ] Zero critical security vulnerabilities

**User Metrics (Month 1):**
- [ ] 100 registered users
- [ ] 50 active users (logged in weekly)
- [ ] 1000+ notification emails sent
- [ ] 20+ calendar feed subscriptions
- [ ] <5% notification unsubscribe rate

**Product Quality:**
- [ ] Mobile-responsive UI (tested on iOS + Android)
- [ ] Accessibility score ≥90 (Lighthouse)
- [ ] Search returns relevant results in <100ms
- [ ] No data staleness >24 hours for CTFtime events

**Launch Checklist:**
- [ ] Privacy policy + Terms of Service published
- [ ] HTTPS enforced (Cloudflare SSL)
- [ ] Error monitoring (Sentry configured)
- [ ] Backup strategy (daily DB snapshots)
- [ ] Support channel (email or Discord)

---

**END OF DOCUMENT**

This research document provides a comprehensive blueprint for building a CTF & Conference Tracker platform with ethical scraping, robust data pipelines, personalized notifications, and production-ready security practices. All recommendations prioritize official APIs where available, respect legal constraints (ToS, robots.txt), and follow industry best practices for web scraping and SecOps.

**Estimated development time:** 4 weeks MVP, 6-8 weeks for v1.3 with full feature set.