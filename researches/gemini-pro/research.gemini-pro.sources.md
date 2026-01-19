Based on the deep research performed to generate the technical design report, here is the complete categorized list of sources used.

### 1. Primary Data Sources (APIs & Event Data)

* **CTFtime API:** The official API documentation for the primary CTF data source, including strict usage policies regarding "clones" and data moderation.
* *Source:*([https://ctftime.org/api/](https://ctftime.org/api/)) `[1]`, `[1]`


* **Sched.com API:** Documentation for the session management platform used by many InfoSec conferences (BSides, etc.), detailing endpoints for session retrieval.
* *Source:*([https://sched.com/api](https://sched.com/api)) `[2]`


* **media.ccc.de API:** Public JSON/GraphQL API documentation for the Chaos Computer Club's media archive, a primary source for conference talks and slides.
* *Source:*([https://github.com/voc/voctoweb](https://github.com/voc/voctoweb)) `[3]`, `[4]`


* **DEFCON Data:** Community-maintained JSON feeds and the "The One" aggregator, which are often more parseable than the official static HTML.
* *Source:*([https://defcon.outel.org/defcon31/dc31-consolidated_page.html](https://defcon.outel.org/defcon31/dc31-consolidated_page.html)) `[5]`, `[6]`


* **GitHub API:** Documentation on rate limits and code search endpoints, essential for the "Archive Crawler" strategy.
* *Source:*([https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api)) `[7]`
* *Source:*([https://github.com/orgs/community/discussions/64618](https://github.com/orgs/community/discussions/64618)) `[8]`



### 2. Technical Standards & Protocols

* **iCalendar (ICS) & Webcal:** Libraries and protocol constraints for calendar subscription feeds.
* *Source:*([https://pypi.org/project/ics/](https://pypi.org/project/ics/)) `[9]`
* *Source:*([https://issuetracker.google.com/issues/465755643](https://issuetracker.google.com/issues/465755643)) `[10]`
* *Source:*([https://developers.google.com/workspace/calendar/caldav/v2/guide](https://developers.google.com/workspace/calendar/caldav/v2/guide)) `[11]`


* **Robots.txt & Crawling Ethics:** Standards for polite crawling and exclusion protocols.
* *Source:*([https://www.robotstxt.org/robotstxt.html](https://www.robotstxt.org/robotstxt.html)) `[12]`
* *Source:*([https://www.cloudflare.com/learning/bots/what-is-robots-txt/](https://www.cloudflare.com/learning/bots/what-is-robots-txt/)) `[13]`



### 3. Architecture & Infrastructure

* **Backend Frameworks (FastAPI vs NestJS):** Performance benchmarks and architectural comparisons justifying the Python/FastAPI choice for this specific domain.
* *Source:*([https://medium.com/@rodrigoarancibiapla/comparing-performances-nestjs-django-and-fastapi-88a464143efb](https://medium.com/@rodrigoarancibiapla/comparing-performances-nestjs-django-and-fastapi-88a464143efb)) `[14]`
* *Source:*([https://www.reddit.com/r/Backend/comments/1nz2ofu/fastapi_vs_spring_boot_nestjs_for_scalable/](https://www.reddit.com/r/Backend/comments/1nz2ofu/fastapi_vs_spring_boot_nestjs_for_scalable/)) `[15]`


* **Task Queues (ARQ vs Celery):** Research into lightweight async queues suitable for the proposed architecture.
* *Source:*([https://davidmuraya.com/blog/fastapi-background-tasks-arq-vs-built-in/](https://davidmuraya.com/blog/fastapi-background-tasks-arq-vs-built-in/)) `[16]`
* *Source:*([https://leapcell.io/blog/celery-versus-arq-choosing-the-right-task-queue-for-python-applications](https://leapcell.io/blog/celery-versus-arq-choosing-the-right-task-queue-for-python-applications)) `[17]`


* **Redis Patterns:** Usage of Redis for caching, rate limiting, and pub/sub in this architecture.
* *Source:*([https://www.geeksforgeeks.org/system-design/redis-and-its-role-in-system-design/](https://www.geeksforgeeks.org/system-design/redis-and-its-role-in-system-design/)) `[18]`



### 4. Notifications & Limits

* **Discord Webhooks:** Rate limits and payload constraints (2000 chars) for the notification dispatcher.
* *Source:*([https://support-dev.discord.com/hc/en-us/articles/6223003921559-My-Bot-is-Being-Rate-Limited](https://support-dev.discord.com/hc/en-us/articles/6223003921559-My-Bot-is-Being-Rate-Limited)) `[19]`
* *Source:*([https://birdie0.github.io/discord-webhooks-guide/other/field_limits.html](https://birdie0.github.io/discord-webhooks-guide/other/field_limits.html)) `[20]`


* **Telegram Bot API:** Message length limits (4096 chars) and broadcasting constraints.
* *Source:*([https://limits.tginfo.me/](https://limits.tginfo.me/)) `[21]`
* *Source:*([https://core.telegram.org/bots/faq](https://core.telegram.org/bots/faq)) `[22]`



### 5. Security & Threat Modeling

* **Automated Threats:** OWASP definitions used to build the threat model regarding scraping and abuse.
* *Source:*([https://owasp.org/www-project-automated-threats-to-web-applications/](https://owasp.org/www-project-automated-threats-to-web-applications/)) `[23]`
* *Source:*([https://owasp.org/www-project-automated-threats-to-web-applications/assets/oats/EN/OAT-011_Scraping](https://owasp.org/www-project-automated-threats-to-web-applications/assets/oats/EN/OAT-011_Scraping)) `[24]`



### 6. Archive & Community Repositories

* **Write-up Archives:** Key GitHub topics and repositories identified for the archive scraper.
* *Source:*([https://github.com/topics/ctf-writeup](https://www.google.com/search?q=https://github.com/topics/ctf-writeup)) `[25]`
* *Source:*([https://github.com/collections/ctf-cybersec-resources](https://github.com/collections/ctf-cybersec-resources)) `[26]`
* *Source:*([https://github.com/devploit/awesome-ctf-resources](https://github.com/devploit/awesome-ctf-resources)) `[27]`