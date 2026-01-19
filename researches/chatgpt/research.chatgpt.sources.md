## Complete source list (for your “CTF & Conference Tracker” deep research)

### CTF event data (primary)

* CTFtime — Official API docs + usage/ToS note (incl. “no CTFtime clones” guidance). ([ctftime.org][1])
* CTFtime — Main site navigation (events/upcoming/archive/calendar). ([ctftime.org][2])
* CTFtime — Organizer submission guidance (how events get added). ([ctftime.org][3])
* CTFtime — Writeups directory (community write-ups archive). ([ctftime.org][4])
* Example reference for CTFtime Events endpoint URL pattern (community code reference). ([GitHub][5])

### Conference / community event sources (primary)

* BSides — Official events listing with iCalendar/ICS export & subscription links. ([BSides][6])
* Black Hat — Archives policy notes (materials + video availability timelines). ([Black Hat][7])
* Black Hat — Briefings materials availability statement. ([Black Hat][8])
* Black Hat — Official YouTube channel (talk recordings). ([YouTube][9])
* OWASP — Global & regional events index (incl. Global AppSec listings). ([OWASP][10])
* OWASP Global AppSec EU 2026 — Official event page (dates + structure). ([Glue Up][11])
* OWASP (Sessionize) — Call-for-Trainers / program submission pages. ([Sessionize][12])
* DEF CON — Official Media Server (talks + CTF-related archives). ([Defcon Media][13])
* CCC / Congress schedules — Fahrplan “schedule.xml” references (how schedules are distributed). ([c3voc.de][14])
* CCC media — media.ccc.de downloadability + metadata. ([media.ccc.de][15])
* CCC media stack — Voctoweb Public JSON API (api.media.ccc.de). ([GitHub][16])
* Conference aggregator dataset — infosec-conferences.com (broad, auto-updated directory). ([infosec-conferences.com][17])

### Archive sources (write-ups / slides / videos)

* GitHub — “Conference presentation slides” mega-repo (community mirrors). ([GitHub][18])
* GitHub — CTF Archives (challenge packs / historical collections). ([GitHub][19])
* GitHub — CTF technical writeups collection. ([GitHub][20])

### Calendar standards + integration references (ICS / CalDAV / Google)

* iCalendar core spec (RFC 5545). ([datatracker.ietf.org][21])
* iCalendar extensions: REFRESH-INTERVAL + SOURCE (RFC 7986). ([datatracker.ietf.org][22])
* CalDAV spec (RFC 4791). ([datatracker.ietf.org][23])
* CalDAV time zone handling details (RFC 7809). ([datatracker.ietf.org][24])
* Google Calendar API overview + event creation (“events.insert”). ([Google for Developers][25])
* Practical refresh behavior notes (Google/clients): Google feed update delay anecdote. ([Web Applications Stack Exchange][26])
* REFRESH hint behavior in the wild: X-PUBLISHED-TTL discussion (client refresh hint). ([GitHub][27])
* ICS refresh interval discussion (community Q&A). ([Stack Overflow][28])
* Google Calendar community thread: “ICS changes not updating” (real-world behavior). ([Google Yardım][29])
* ICS limitations vs real-time sync (one-way + delay framing). ([CalendarBridge][30])

### Scraping ethics + robustness + data QA

* AWS Prescriptive Guidance — ethical crawler best practices (robots.txt, rate limiting, user-agent transparency, error handling). ([AWS Dokümantasyonu][31])
* Zyte — Schema/JSON Schema validation approach for scraped data QA. ([Zyte  #1 Web Scraping Service][32])

### Notifications + anti-spam + security hygiene

* OneSignal — Frequency capping documentation (limits per time window). ([documentation.onesignal.com][33])
* OneSignal — Over-messaging mitigation (frequency cap patterns). ([OneSignal][34])
* Push notification best-practice guidance (frequency moderation + personalization). ([upshot.ai][35])
* Secrets management baseline (“never hardcode secrets”). ([StackHawk, Inc.][36])
* OWASP Secure Coding Practices checklist (general appsec checklist baseline). ([GitHub][37])

If you want, I can also output this same list as a clean “Sources Appendix” you can paste directly into your report (with short annotations per source).

[1]: https://ctftime.org/api/?utm_source=chatgpt.com "CTFtime.org / API"
[2]: https://ctftime.org/?utm_source=chatgpt.com "CTFtime.org / All about CTF (Capture The Flag)"
[3]: https://ctftime.org/for-organizers/?utm_source=chatgpt.com "Information for CTF organizers"
[4]: https://ctftime.org/writeups?utm_source=chatgpt.com "CTFtime.org / Writeups"
[5]: https://github.com/Mayfly277/ctftime_events_info?utm_source=chatgpt.com "CTF time event api checker"
[6]: https://bsides.org/events/?utm_source=chatgpt.com "Events from January 2, 2025"
[7]: https://blackhat.com/html/archives.html?utm_source=chatgpt.com "Archives"
[8]: https://blackhat.com/briefings/?utm_source=chatgpt.com "Briefings"
[9]: https://www.youtube.com/%40BlackHatOfficialYT?utm_source=chatgpt.com "Black Hat"
[10]: https://owasp.org/events/?utm_source=chatgpt.com "OWASP Global & Regional Events"
[11]: https://owasp.glueup.com/en/event/owasp-global-appsec-eu-2026-vienna-austria-162243/?utm_source=chatgpt.com "OWASP Global AppSec EU 2026 (Vienna, Austria)"
[12]: https://sessionize.com/owasp-global-appsec-2026EU/?utm_source=chatgpt.com "OWASP Global AppSec EU (Vienna) 2026 - CFT"
[13]: https://media.defcon.org/?utm_source=chatgpt.com "The DEF CON® Media Server - Archives of the conferences"
[14]: https://c3voc.de/wiki/schedule?utm_source=chatgpt.com "Schedule"
[15]: https://media.ccc.de/?utm_source=chatgpt.com "home - media.ccc.de"
[16]: https://github.com/voc/voctoweb?utm_source=chatgpt.com "voctoweb – the frontend and backend software behind ..."
[17]: https://infosec-conferences.com/?utm_source=chatgpt.com "Cybersecurity Conferences 2026 - 2027 | Over 3.4K Events ..."
[18]: https://github.com/onhexgroup/Conferences?utm_source=chatgpt.com "onhexgroup/Conferences: Conference presentation slides"
[19]: https://github.com/sajjadium/ctf-archives?utm_source=chatgpt.com "CTF Archives: Collection of CTF Challenges."
[20]: https://github.com/sajjadium/ctf-writeups?utm_source=chatgpt.com "Collection of CTF \"technical\" writeups by PersianCats."
[21]: https://datatracker.ietf.org/doc/html/rfc5545?utm_source=chatgpt.com "RFC 5545 - Internet Calendaring and Scheduling Core Object ..."
[22]: https://datatracker.ietf.org/doc/html/rfc7986?utm_source=chatgpt.com "RFC 7986 - New Properties for iCalendar - Datatracker - IETF"
[23]: https://datatracker.ietf.org/doc/html/rfc4791?utm_source=chatgpt.com "RFC 4791 - Calendaring Extensions to WebDAV (CalDAV)"
[24]: https://datatracker.ietf.org/doc/html/rfc7809?utm_source=chatgpt.com "RFC 7809 - Calendaring Extensions to WebDAV (CalDAV)"
[25]: https://developers.google.com/workspace/calendar/api/guides/overview?utm_source=chatgpt.com "Google Calendar API overview"
[26]: https://webapps.stackexchange.com/questions/6313/how-often-does-google-calendar-update-its-other-calendar-feeds?utm_source=chatgpt.com "How often does Google Calendar update its \"Other ..."
[27]: https://github.com/Sonarr/Sonarr/issues/6065?utm_source=chatgpt.com "Signal automatic calendar updates with iCal · Issue #6065"
[28]: https://stackoverflow.com/questions/17152251/specifying-name-description-and-refresh-interval-in-ical-ics-format?utm_source=chatgpt.com "Specifying name, description and refresh interval in iCal ..."
[29]: https://support.google.com/calendar/thread/178132462/calendar-events-not-updating-on-changes-in-ics-file?hl=en&utm_source=chatgpt.com "Calendar events not updating on changes in ics-file"
[30]: https://calendarbridge.com/blog/ics-icalendar-feeds-vs-real-time-sync-whats-the-difference/?utm_source=chatgpt.com "ICS iCalendar Feeds vs Real Time Sync"
[31]: https://docs.aws.amazon.com/prescriptive-guidance/latest/web-crawling-system-esg-data/best-practices.html?utm_source=chatgpt.com "Best practices for ethical web crawlers"
[32]: https://www.zyte.com/blog/guide-to-web-data-extraction-qa-validation-techniques/?utm_source=chatgpt.com "A practical guide to web data QA part I: Validation techniques"
[33]: https://documentation.onesignal.com/docs/en/frequency-capping?utm_source=chatgpt.com "Push frequency capping"
[34]: https://onesignal.com/blog/7-easy-solutions-to-mitigate-the-risks-of-over-messaging/?utm_source=chatgpt.com "7 Easy Solutions to Mitigate the Risks of Over-Messaging"
[35]: https://www.upshot.ai/blog/push-notifications-best-practices?utm_source=chatgpt.com "Push Notifications Best Practices for 2025: Do's and Don'ts"
[36]: https://www.stackhawk.com/blog/web-application-security-checklist-10-improvements/?utm_source=chatgpt.com "Web Application Security Checklist: 10 Best Practices"
[37]: https://github.com/OWASP/www-project-secure-coding-practices-quick-reference-guide/blob/main/stable-en/02-checklist/05-checklist.md?utm_source=chatgpt.com "Secure Coding Practices Checklist"
