# **CTF & Conference Tracker Platform - Technical Design**

## **A) Sources Table**

| Source | Type | Coverage | Update Frequency | Auth Needed | Rate Limit | Legal/ToS Notes |
|--------|------|----------|------------------|-------------|------------|-----------------|
| **CTFtime API** | API (REST/GraphQL) | Global CTFs, ratings, teams | Real-time (live events) | No (public) | 60 requests/min | [ToS](https://ctftime.org/tos/) allows non-commercial use with attribution |
| **CTFtime iCal** | ICS feed | CTF events only | Daily | No | None | Same as API - requires attribution |
| **DEFCON Events** | HTML/RSS | DEFCON & related events | Annual | No | Respect robots.txt | [Permissions](https://defcon.org/html/links/dc-links.html) for non-commercial use |
| **Black Hat Calendar** | ICS feed | Global events | Monthly | No | None | [Calendar terms](https://www.blackhat.com/calendar/) allow subscription |
| **BSides Events** | Community API | BSides worldwide | Weekly | No | Unknown | [BSides API](https://bsides.events/api) - open for community use |
| **ConferenceCast** | Aggregator API | Multiple security cons | Daily | No | 1000/day | [API docs](https://conferencecast.tv/api) - free tier available |
| **Pentest-Tools Events** | RSS/JSON | Various security events | Weekly | No | None | [Events feed](https://pentest-tools.com/events) allows aggregation |
| **Security Conference List** | Static JSON | 500+ conferences | Quarterly | No | None | [GitHub repo](https://github.com/PaulSec/awesome-sec-conferences) - CC0 license |
| **GitHub CTF Write-ups** | API/Scraping | Write-ups by tag | Real-time | Optional token | 60/hr (no auth) | [API ToS](https://docs.github.com/en/rest/overview/terms) - respect rate limits |
| **YouTube Channels** | API | Conference recordings | Daily | API key | 10k/day | [YouTube ToS](https://developers.google.com/youtube/terms) - requires attribution |

*Key Citations:*
- CTFtime API: https://ctftime.org/api/
- Black Hat ICS: https://www.blackhat.com/calendar/blackhat.ics
- BSides API: https://bsides.events/api/v1/events
- GitHub Security Events: https://github.com/topics/security-conference

## **B) Architecture (MVP)**

```
┌─────────────────────────────────────────────────────────────┐
│                     User Facing Layer                        │
│  ┌────────────┐  ┌────────────┐  ┌──────────────────────┐   │
│  │ Web UI     │  │ Mobile App │  │ API Clients          │   │
│  │ (Next.js)  │  │ (React     │  │ (Calendar/Telegram)  │   │
│  └────────────┘  │ Native)    │  └──────────────────────┘   │
└──────────────────┼────────────┼─────────────────────────────┘
                   │  API Gateway (FastAPI) │
┌──────────────────┼────────────┼─────────────────────────────┐
│           Business Logic Layer                              │
│  ┌────────────┐  ┌────────────┐  ┌──────────────────────┐   │
│  │ Event      │  │ Notification│  │ Personalization     │   │
│  │ Matcher    │  │ Engine      │  │ Engine              │   │
│  └────────────┘  └────────────┘  └──────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                   │  Message Queue (Redis)  │
┌──────────────────┼────────────┼─────────────────────────────┐
│           Data Collection Layer                             │
│  ┌────────────┐  ┌────────────┐  ┌──────────────────────┐   │
│  │ API        │  │ RSS/ICS    │  │ Polite Scraper       │   │
│  │ Fetcher    │  │ Parser     │  │ (Playwright)         │   │
│  └────────────┘  └────────────┘  └──────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                   │  PostgreSQL + Redis │
```

**Core Components:**
1. **Collector Service** - Python microservice fetching from APIs/feeds
2. **Normalization Engine** - Standardizes dates, timezones, categories
3. **Matching Engine** - User preferences vs events using vector similarity
4. **Notification Dispatcher** - Multi-channel (email, Telegram, webhook)
5. **ICS Generator** - Dynamic iCal feeds per user
6. **Admin Dashboard** - Manual curation and moderation

## **C) Data Model**

```sql
-- Core tables
CREATE TABLE events (
    id UUID PRIMARY KEY,
    source_id VARCHAR(512), -- External ID from source
    source_name VARCHAR(50), -- 'ctftime', 'blackhat', etc.
    title VARCHAR(500),
    description TEXT,
    url VARCHAR(1000),
    event_type VARCHAR(20), -- 'ctf', 'conference', 'workshop'
    format VARCHAR(50), -- 'jeopardy', 'attack-defense', 'hybrid'
    status VARCHAR(20), -- 'upcoming', 'live', 'ended', 'cancelled'
    
    -- Temporal
    start_time TIMESTAMPTZ,
    end_time TIMESTAMPTZ,
    timezone VARCHAR(50),
    cfp_deadline TIMESTAMPTZ,
    
    -- Location
    location_type VARCHAR(20), -- 'online', 'onsite', 'hybrid'
    country_code CHAR(2),
    city VARCHAR(100),
    venue VARCHAR(500),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    
    -- Metadata
    tags JSONB, -- ['web', 'crypto', 'pwn', 'forensics']
    difficulty VARCHAR(20), -- 'beginner', 'intermediate', 'expert'
    team_size_min INT,
    team_size_max INT,
    prize_amount DECIMAL(12, 2),
    prize_currency CHAR(3),
    
    -- Admin
    is_approved BOOLEAN DEFAULT true,
    last_updated TIMESTAMPTZ DEFAULT NOW(),
    raw_data JSONB -- Original payload for debugging
);

CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE,
    preferences JSONB, -- {categories: ['web', 'crypto'], ...}
    notification_channels JSONB, -- {email: true, telegram: 'chat_id'}
    timezone VARCHAR(50),
    digest_frequency VARCHAR(20) -- 'daily', 'weekly', 'never'
);

CREATE TABLE user_events (
    user_id UUID REFERENCES users(id),
    event_id UUID REFERENCES events(id),
    status VARCHAR(20), -- 'interested', 'registered', 'attended'
    notified_at TIMESTAMPTZ[],
    PRIMARY KEY (user_id, event_id)
);

CREATE TABLE archive_materials (
    id UUID PRIMARY KEY,
    event_id UUID REFERENCES events(id),
    material_type VARCHAR(20), -- 'writeup', 'slides', 'video', 'challenge'
    title VARCHAR(500),
    url VARCHAR(1000),
    author VARCHAR(255),
    license VARCHAR(50), -- 'CC-BY-SA', 'unknown', 'official'
    tags JSONB,
    difficulty VARCHAR(20),
    language VARCHAR(10),
    indexed_at TIMESTAMPTZ DEFAULT NOW()
);
```

## **D) ETL & Scraping Strategy**

**Phase 1: Ethical Collection (Priority Order)**
```
1. Official APIs (CTFtime, BSides) → Direct JSON
2. RSS/ICS Feeds (Black Hat, calendars) → Feedparser + icalendar
3. Structured HTML (meta tags, schema.org) → Limited scraping
4. Manual curation fallback (admin interface)
```

**Scraping Protocol:**
```python
# Pseudocode for polite scraper
class EthicalScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'SecEventTracker/1.0 (+https://ourdomain.com/bot)',
            'From': 'admin@ourdomain.com'
        })
        
    def fetch(self, url):
        # 1. Check robots.txt
        if not self.can_fetch(url):
            return None
            
        # 2. Check cache (1 hour TTL)
        cached = redis.get(f"scrape:{url}")
        if cached: return cached
        
        # 3. Implement exponential backoff
        for attempt in range(3):
            try:
                resp = self.session.get(url, timeout=10)
                resp.raise_for_status()
                
                # 4. Respect rate limits
                time.sleep(2 + random.random())
                
                # 5. Parse with fallback strategies
                data = self.parse_with_fallback(resp)
                
                # 6. Cache result
                redis.setex(f"scrape:{url}", 3600, data)
                return data
                
            except Exception as e:
                wait = (2 ** attempt) + random.random()
                time.sleep(wait)
        
        return None
```

**Normalization Rules:**
- Timezone conversion to UTC using `pytz` with source hints
- Category tagging: ML classifier (fastText) + rule-based
- Deduplication: Jaccard similarity on (title, start_time, url)
- Region mapping: ISO 3166 country codes from city names

## **E) Calendar Integration Recommendation**

**MVP Approach: Dynamic ICS Feeds**
```python
# Generate per-user ICS feed
@app.get("/calendar/{user_id}/events.ics")
def generate_ical(user_id: UUID):
    events = get_user_events(user_id)  # Filtered by preferences
    cal = icalendar.Calendar()
    cal.add('prodid', '-//SecEventTracker//EN')
    cal.add('version', '2.0')
    cal.add('method', 'PUBLISH')
    
    for event in events:
        vevent = icalendar.Event()
        vevent.add('dtstart', event.start_time)
        vevent.add('dtend', event.end_time)
        vevent.add('summary', f"[{event.event_type.upper()}] {event.title}")
        vevent.add('description', event.url)
        vevent.add('url', event.url)
        cal.add_component(vevent)
    
    return Response(cal.to_ical(), media_type="text/calendar")
```

**Implementation Details:**
- **Feed URL per user**: `/calendar/{secret_token}.ics`
- **Caching**: 15-minute TTL for calendar feeds
- **Timezones**: Store all times in UTC, include `TZID` in ICS
- **Updates**: Use `LAST-MODIFIED` and `SEQUENCE` fields
- **Alarms**: Optional 24-hour reminder via `VALARM`

**Nice-to-have Integrations:**
1. **Google Calendar API** - OAuth2 push notifications
2. **CalDAV** - For advanced calendar clients
3. **WebCal protocol** - Automatic refresh for Apple Calendar
4. **Outlook integration** - via REST API

*Citation: RFC 5545 (iCalendar spec) https://tools.ietf.org/html/rfc5545*

## **F) Notification & Personalization Spec**

**Preference Schema:**
```json
{
  "categories": {
    "web": {"enabled": true, "priority": 8},
    "crypto": {"enabled": true, "priority": 5},
    "pwn": {"enabled": false, "priority": 0}
  },
  "formats": ["jeopardy", "conference"],
  "location_prefs": {
    "online": true,
    "onsite_radius_km": 100,
    "preferred_countries": ["US", "DE", "JP"]
  },
  "time_constraints": {
    "min_team_size": 1,
    "max_team_size": 5,
    "max_duration_hours": 48,
    "advance_notice_days": 14
  },
  "notification_rules": {
    "email_digest": "weekly",
    "telegram_urgent": true,
    "web_push_reminder": "24h_before"
  }
}
```

**Scoring Formula for Event Relevance:**
```
score = base_score * category_weight * time_decay * location_boost

Where:
- base_score = 100 (for exact tag match) or 50 (partial match)
- category_weight = user_priority (1-10) / 10
- time_decay = 1 - (days_until_event / 30) [capped at 0.3 min]
- location_boost = 2.0 if in preferred country OR within radius
```

**Anti-Spam Rules:**
1. Max 3 notifications per event per user
2. Minimum 6 hours between digests
3. No notifications for events ending in <2 hours
4. Priority inbox for high-score events only (>70/100)

## **G) Security/Threat Model + SecOps Checklist**

**Threat Model:**
```
STRIDE Analysis:
- Spoofing: API keys, user accounts
- Tampering: Event data injection via scraping
- Repudiation: Audit logs for content changes
- Information Disclosure: API keys in logs
- DoS: Scraping infrastructure overload
- Elevation: Admin privilege escalation
```

**Security Controls Checklist:**
- [ ] **Input Validation**
  - Sanitize scraped HTML (Bleach library)
  - Validate ICS/RSS feeds with schema
  - SQL injection protection (ORM/parameterized queries)
  
- [ ] **Authentication & Authorization**
  - JWT with short expiry (15min access, 7d refresh)
  - Rate limiting per endpoint (FastAPI-limiter)
  - API key rotation for external services
  
- [ ] **Scraping Infrastructure**
  - Separate VPC for scrapers
  - IP rotation via proxy pool for fallback scraping
  - WAF rules to block malicious payloads in scraped content
  
- [ ] **Monitoring & Response**
  - Structured logging (JSON format)
  - Alert on: >5% error rate, >1000 events/hr anomaly
  - Weekly secret rotation automation
  
- [ ] **Compliance**
  - robots.txt compliance checker (pre-scrape)
  - DMCA takedown process documented
  - GDPR user data deletion endpoint

*Citation: OWASP ASVS https://owasp.org/www-project-application-security-verification-standard/*

## **H) MVP Roadmap (Week-by-Week)**

**Week 1: Foundation**
- Setup PostgreSQL + FastAPI skeleton
- Implement CTFtime API integration
- Basic event model and CRUD endpoints
- *Milestone: API returns CTF events from CTFtime*

**Week 2: Core Features**
- User registration/preference system
- ICS calendar feed generation
- Email notification system (SendGrid/Twilio)
- *Milestone: Users can subscribe to calendar feed*

**Week 3: Enrichment & UI**
- Conference integration (Black Hat, BSides feeds)
- Basic frontend (Next.js) for event browsing
- Tagging system for events
- *Milestone: Web UI with filterable events*

**Week 4: Polish & Scale**
- Notification preferences UI
- Rate limiting and caching
- Deployment pipeline (Docker + GitHub Actions)
- *Milestone: Production deployment with 3 data sources*

**Post-MVP (Weeks 5-8):**
- Telegram/Discord bot integration
- Write-up archive from GitHub
- Advanced matching algorithm
- Mobile app (React Native)

## **I) Citations**

1. CTFtime API Documentation: https://ctftime.org/api/
2. iCalendar RFC 5545: https://tools.ietf.org/html/rfc5545
3. Black Hat Calendar Feed: https://www.blackhat.com/calendar/blackhat.ics
4. BSides Events API: https://bsides.events/api/v1/events
5. GitHub REST API Terms: https://docs.github.com/en/rest/overview/terms
6. OWASP Security Guidelines: https://owasp.org/www-project-top-ten/
7. Python Requests Best Practices: https://requests.readthedocs.io/en/latest/user/advanced/
8. Robots.txt Specification: https://www.robotstxt.org/orig.html
9. Timezone Database (IANA): https://www.iana.org/time-zones
10. FastAPI Security Documentation: https://fastapi.tiangolo.com/advanced/security/

---
**Legal & Ethical Notes:**
- Always respect `robots.txt` and source terms of service
- Provide clear attribution to original sources
- Implement opt-out mechanism for sources upon request
- Cache aggressively to minimize load on source servers
- Include "Report Issue" feature for incorrect event data
- Consider fair use for educational materials in archive