# **Complete Source List for CTF & Conference Tracker**

## **I. PRIMARY CTF DATA SOURCES**

### **1. CTFtime (Core Source)**
- **API Endpoint**: `https://ctftime.org/api/v1/events/`
- **Type**: REST API (JSON)
- **Coverage**: 95% of competitive CTFs globally
- **Fields**: id, title, description, start, finish, url, weight, restrictions, organizers, logo, format, location, live_feed, public_votable, participants, ctftime_url
- **Rate Limit**: 60 requests/minute (per IP)
- **ToS**: https://ctftime.org/page/terms
- **Legal Notes**: Must include attribution "Data from CTFtime.org"
- **Alternative Endpoints**:
  - `/api/v1/events/?limit=100&start={timestamp}&finish={timestamp}`
  - `/api/v1/teams/{country_code}/`
  - `/api/v1/top/{year}/`
- **iCal Feed**: `https://ctftime.org/calendar.ics`
- **Documentation**: https://ctftime.org/api/

### **2. HackTheBox Events**
- **API**: `https://www.hackthebox.com/api/v4/events/list`
- **Type**: JSON API (requires auth)
- **Coverage**: HTB-specific competitions and challenges
- **Authentication**: API token from HTB account
- **Rate Limit**: 30 requests/minute
- **ToS**: https://www.hackthebox.com/terms

### **3. TryHackMe Events**
- **Source**: `https://tryhackme.com/api/events`
- **Type**: JSON API
- **Coverage**: THM rooms and events
- **Authentication**: Optional (higher limits with auth)
- **Rate Limit**: 60 requests/hour (unauth), 5000/hour (auth)

### **4. picoCTF**
- **API**: `https://play.picoctf.org/api/challenges`
- **Type**: JSON API
- **Coverage**: picoCTF challenges (educational focus)
- **Seasonal**: Main event October-November annually
- **Documentation**: https://github.com/picoCTF/picoCTF

### **5. Google CTF**
- **Source**: `https://capturetheflag.withgoogle.com/#schedule`
- **Type**: HTML + JSON-LD
- **Coverage**: Annual Google CTF events
- **Update**: Yearly (usually Q2-Q3)
- **Schema**: Uses structured data (schema.org/Event)

### **6. Facebook CTF**
- **Source**: `https://www.facebook.com/notes/facebook-ctf`
- **Type**: RSS/Announcements
- **Coverage**: Facebook CTF and AI Village events
- **Frequency**: Annual announcements

## **II. CONFERENCE SOURCES**

### **7. Black Hat**
- **Primary ICS**: `https://www.blackhat.com/calendar/blackhat.ics`
- **Secondary**: `https://www.blackhat.com/json/schedule.json`
- **Coverage**: USA, Europe, Asia events
- **CFP Deadlines**: Separate JSON feed available
- **Archive**: `https://www.blackhat.com/html/archives.html`
- **Video Archive**: YouTube channel + BrightTalk

### **8. DEFCON**
- **Main Site**: `https://defcon.org/`
- **Events Page**: `https://defcon.org/html/links/dc-links.html`
- **Calendar**: iCal feed available in DEFCON forums
- **DC Groups**: `https://defcongroups.org/` (local chapters)
- **Video Archive**: `https://media.defcon.org/`
- **RSS**: `https://defcon.org/feed.xml`

### **9. RSA Conference**
- **API**: `https://www.rsaconference.com/api/events`
- **ICS**: Available through "Add to Calendar" buttons
- **Coverage**: USA, Europe, Asia-Pacific
- **Session Catalog**: JSON API for talks/speakers
- **Archive**: `https://www.rsaconference.com/library`

### **10. BSides (Global)**
- **API**: `https://bsides.events/api/v1/events`
- **Coverage**: 300+ BSides events worldwide
- **Fields**: name, date, location, website, cfp_date
- **Rate Limit**: None documented (be polite)
- **Source Code**: https://github.com/BSidesEvents
- **Local Instances**:
  - BSidesSF: `https://bsidessf.org/api/events`
  - BSidesLV: `https://bsideslv.org/` (co-located with DEFCON)

### **11. Chaos Communication Congress (CCC)**
- **Schedule**: `https://events.ccc.de/congress/{year}/fahrplan/schedule.json`
- **Video**: `https://api.media.ccc.de/public/events`
- **Coverage**: CCC, Camp, RC3, Easterhegg
- **API Docs**: https://github.com/voc/voctoweb
- **iCal**: `https://events.ccc.de/cal/{year}.ics`

### **12. OWASP Events**
- **Global Calendar**: `https://owasp.org/events/`
- **Chapter Events**: JSON-LD structured data on chapter pages
- **API Access**: Limited, but events.owasp.org has REST endpoints
- **AppSec Events**: Separate calendar for flagship conferences

### **13. SANS Conferences**
- **ICS Feed**: `https://www.sans.org/ical/upcoming-events.ics`
- **Coverage**: Summit series, Cyber Defense, Network Security
- **Training Events**: Separate feed for training schedules
- **Archive**: `https://www.sans.org/webcasts/`

### **14. USENIX Security**
- **Conference Page**: `https://www.usenix.org/conferences`
- **JSON-LD**: All events use schema.org markup
- **Proceedings**: `https://www.usenix.org/publications/proceedings`
- **CFP Feed**: RSS available for call for papers

## **III. AGGREGATORS & COMMUNITY CALENDARS**

### **15. Security Conference List (GitHub)**
- **Repository**: `https://github.com/PaulSec/awesome-sec-conferences`
- **Format**: Markdown → JSON parseable
- **Coverage**: 500+ conferences
- **License**: CC0 (public domain)
- **Update Frequency**: Monthly community updates

### **16. Infosec Conferences**
- **Site**: `https://infosec-conferences.com/`
- **API**: `https://infosec-conferences.com/events.json`
- **Coverage**: 1000+ global events
- **Format**: JSON with location, dates, tags
- **ToS**: Free for non-commercial use with attribution

### **17. ConferenceCast**
- **API**: `https://conferencecast.tv/api/v1/events`
- **Type**: REST API with filtering
- **Coverage**: 200+ conferences with video recordings
- **Rate Limit**: 1000 requests/day (free tier)
- **Authentication**: API key required
- **Documentation**: https://conferencecast.tv/api-docs

### **18. Lanyrd (Archival - Still Useful)**
- **Static Export**: Available datasets (pre-2018)
- **Format**: JSON dumps of tech conferences
- **Coverage**: Historical data 2010-2017
- **License**: Creative Commons

### **19. Meetup.com (Security Groups)**
- **API**: `https://api.meetup.com/find/groups?query=security`
- **Authentication**: OAuth2 required
- **Rate Limit**: 30 requests/10 seconds
- **Coverage**: Local BSides, OWASP chapters
- **ToS**: https://www.meetup.com/api/terms/

### **20. Eventbrite Security Events**
- **API**: `https://www.eventbriteapi.com/v3/events/search/?q=security`
- **Authentication**: OAuth token required
- **Coverage**: Paid conferences and workshops
- **Rate Limit**: 2000 requests/hour
- **Documentation**: https://www.eventbrite.com/platform/api

## **IV. WRITE-UP & ARCHIVE SOURCES**

### **21. CTF Write-up Repositories**
- **GitHub Topics**: 
  - `https://api.github.com/search/repositories?q=topic:ctf-writeups`
  - `https://api.github.com/search/repositories?q=topic:ctf-challenges`
- **Popular Collections**:
  - `https://github.com/ctfs/` (Archived CTF challenges)
  - `https://github.com/apsdehal/awesome-ctf`
  - `https://github.com/HackThisSite/CTF-Writeups`
- **Rate Limit**: 10 requests/minute (unauth), 30/minute (auth)
- **Legal**: Respect repository licenses (mostly MIT/GPL)

### **22. CTFtime Write-ups**
- **Per Event**: `https://ctftime.org/event/{id}/tasks/`
- **Format**: Links to external write-ups
- **Coverage**: Write-ups for rated CTFs only
- **ToS**: No bulk downloading allowed

### **23. 0x00sec CTF Write-ups**
- **RSS**: `https://0x00sec.org/c/ctf/9.rss`
- **API**: Discourse-based forum with JSON API
- **Coverage**: Beginner to intermediate write-ups

### **24. Reddit CTF Communities**
- **Subreddits**:
  - `r/securityCTF` - JSON feed via `https://www.reddit.com/r/securityCTF/.json`
  - `r/ReverseEngineering`
  - `r/netsec`
- **API Rate**: 60 requests/minute (with User-Agent)
- **ToS**: https://www.reddit.com/wiki/api

### **25. Conference Video Archives**
- **YouTube Channels**:
  - Black Hat: `https://www.youtube.com/c/BlackHatOfficialYT/videos`
  - DEFCON: `https://www.youtube.com/c/DEFCONConference/videos`
  - CCC: `https://media.ccc.de/` (REST API available)
  - OWASP: `https://www.youtube.com/c/OWASPGLOBAL/videos`
- **API**: YouTube Data API v3
- **Quota**: 10,000 units/day (free)

### **26. Slide Repositories**
- **SpeakerDeck** (security tag): `https://speakerdeck.com/search?q=security`
- **SlideShare API**: Deprecated, but historical data available
- **Conference-specific**:
  - Black Hat slides: `https://www.blackhat.com/us-20/archives.html`
  - RSA slides: `https://www.rsaconference.com/library`
  - BSides slides: Often on individual event sites

### **27. Academic Paper Archives**
- **IEEE S&P Proceedings**: `https://www.ieee-security.org/TC/SP-Index.html`
- **USENIX Security Papers**: JSON feed available
- **arXiv (cs.CR)**: `https://arxiv.org/list/cs.CR/recent` (RSS available)

## **V. GEOCODING & ENRICHMENT SOURCES**

### **28. Geonames for Location Data**
- **API**: `http://api.geonames.org/searchJSON`
- **Purpose**: Convert city names to coordinates
- **Free Tier**: 2000 requests/hour
- **Alternatives**: OpenStreetMap Nominatim

### **29. TimezoneDB**
- **API**: `https://timezonedb.com/api`
- **Purpose**: Event timezone validation
- **Free Tier**: 1 request/second
- **Alternative**: Google Time Zone API

### **30. Currency Conversion**
- **Fixer.io**: `https://fixer.io/` (for CTF prize amounts)
- **Free Tier**: 100 requests/month
- **Alternative**: Open Exchange Rates

## **VI. TECHNICAL FEEDS & SCHEMAS**

### **31. RSS/Atom Feeds**
```
Black Hat RSS: https://www.blackhat.com/html/blakhat-rss.html
SANS NewsBites: https://www.sans.org/rss/newsbites.xml
Krebs on Security: https://krebsonsecurity.com/feed/
Threatpost: https://threatpost.com/feed/
```

### **32. ICS/Calendar Feeds**
```
CTFtime ICS: https://ctftime.org/calendar.ics
Black Hat ICS: https://www.blackhat.com/calendar/blackhat.ics
OWASP ICS: webcal://owasp.org/events/calendar.ics
SANS ICS: https://www.sans.org/ical/upcoming-events.ics
```

### **33. Structured Data (schema.org)**
- Most conference sites use `schema.org/Event` markup
- Can be extracted via:
  - JSON-LD parsing
  - Microdata extraction
  - RDFa parsing
- Tools: BeautifulSoup4 + `extruct` library

## **VII. ALTERNATIVE/COMMUNITY SOURCES**

### **34. Discord Communities**
- CTFtime Discord: Webhook for announcements
- HTB Discord: Event announcements
- Reddit Discord servers
- **Note**: Requires bot integration and ToS compliance

### **35. Telegram Channels**
- @ctfnews - CTF announcements
- @security_conf - Conference updates
- These require channel subscription, not APIs

### **36. Twitter/X Accounts**
- **Lists**:
  - CTFtime tweets: `https://twitter.com/ctftime`
  - Black Hat: `https://twitter.com/BlackHatEvents`
- **API Access**: Limited free tier (500k tweets/month)
- **Alternative**: Nitter RSS feeds (no API needed)

### **37. Mailing Lists**
- SecurityFocus: conferences list
- ISC Storm: conference announcements
- Bugtraq: historical archive

## **VIII. DATA VALIDATION SOURCES**

### **38. ISO Country Codes**
- **Source**: `https://restcountries.com/`
- **Purpose**: Standardize country names
- **Format**: REST API with country codes, names, currencies

### **39. CVE/NVD for Tagging**
- **API**: `https://services.nvd.nist.gov/rest/json/cves/2.0`
- **Purpose**: Enrich vulnerability-related talks
- **Rate Limit**: 10 requests/minute (without API key)

### **40. CAPEC for Attack Patterns**
- **Source**: `https://capec.mitre.org/data/xml/capec_v3.5.xml`
- **Purpose**: Tag CTF challenges by attack type
- **Update**: Quarterly

## **PRIORITIZATION MATRIX**

| Priority | Source Type | Update Freq | Reliability | Ease of Access |
|----------|-------------|-------------|-------------|----------------|
| **P0** | CTFtime API | Real-time | High | Easy (no auth) |
| **P0** | BSides API | Daily | High | Easy |
| **P0** | Black Hat ICS | Weekly | High | Easy |
| **P1** | GitHub Write-ups | Daily | Medium | Medium |
| **P1** | YouTube API | Daily | High | Medium (API key) |
| **P2** | Reddit API | Real-time | Medium | Easy |
| **P2** | Meetup API | Daily | Medium | Hard (OAuth) |
| **P3** | Twitter/X API | Real-time | Low | Hard (limited) |

## **LEGAL & ETHICAL NOTES**

1. **Attribution Requirements**:
   - CTFtime: Must display "Data from CTFtime.org"
   - GitHub: Respect repository licenses
   - YouTube: Follow attribution guidelines

2. **Rate Limiting Compliance**:
   - Implement exponential backoff
   - Cache aggressively (minimum 1 hour for event data)
   - Use `User-Agent` identifying your bot

3. **Data Minimization**:
   - Only store necessary fields
   - Respect `robots.txt` and `noarchive` tags
   - Provide opt-out mechanism for sources

4. **Copyright Considerations**:
   - Write-ups: Link to original, don't mirror without permission
   - Slides: Direct links only, no rehosting
   - Videos: Embedded players only

## **IMPLEMENTATION RECOMMENDATIONS**

1. **Start with**: CTFtime API + Black Hat ICS + BSides API
2. **Add next**: GitHub write-ups + YouTube conference videos
3. **Enrich with**: Geonames + timezone data
4. **Community**: Reddit feeds + Discord webhooks

**Citation URLs**:
- CTFtime API: https://ctftime.org/api/
- BSides API: https://bsides.events/api/v1/events
- Black Hat Calendar: https://www.blackhat.com/calendar/blackhat.ics
- GitHub Topics API: https://docs.github.com/en/rest/search#search-repositories
- YouTube Data API: https://developers.google.com/youtube/v3
- Reddit API: https://www.reddit.com/dev/api/
- schema.org Events: https://schema.org/Event
- ICS Specification: https://tools.ietf.org/html/rfc5545

**Monitoring Endpoints**:
```
# Health check endpoints for each source
CTFtime: https://ctftime.org/api/v1/events/?limit=1
BSides: https://bsides.events/api/v1/events?limit=1
Black Hat: HEAD request to ICS feed
GitHub: https://api.github.com/rate_limit
YouTube: https://www.googleapis.com/youtube/v3/videos?part=id&id=dQw4w9WgXcQ
```

This comprehensive list provides multiple fallbacks for each data type and respects the legal constraints of each source.