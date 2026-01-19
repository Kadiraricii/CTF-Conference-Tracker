# **CTF & Conference Tracker \- Project Plan**

## **1\. Data Sources Strategy**

The platform relies on a "Tiered Trust" model for data ingestion.

| Tier | Source | Use Case | Reliability |
| :---- | :---- | :---- | :---- |
| **Tier 1** | **CTFtime API** | CTF events, dates, weights, format. | High |
| **Tier 1** | **InfoSec Conf (GitHub)** | Conference dates, CFPs. | High |
| **Tier 2** | **Official RSS Feeds** | Aggregators like CCC or DEFCON news. | Medium |
| **Tier 3** | **Scraping** | Specific event pages (Last resort). | Low (Fragile) |

## **2\. Technical Architecture**

### **Tech Stack (Recommended)**

* **Language:** Python 3.11+  
* **Framework:** FastAPI (Async is great for scraper I/O)  
* **Database:** PostgreSQL (Relation data) \+ Redis (Cache/Queue)  
* **Task Queue:** Celery or Arq  
* **Frontend:** Next.js (Static Site Generation \+ API hydration)

### **Service Diagram**

User \--\> \[Next.js UI\]  
|  
v  
User \--\> \[FastAPI\] \--\> \[Postgres\]  
^  
|  
\[Celery Worker\]  
/ |  
\[CTFtime\] \[GitHub\] \[RSS\]

## **3\. Data Model (SQL)**

CREATE TABLE events (  
    id UUID PRIMARY KEY,  
    title VARCHAR(255) NOT NULL,  
    start\_time TIMESTAMPTZ NOT NULL,  
    end\_time TIMESTAMPTZ NOT NULL,  
    type VARCHAR(50) CHECK (type IN ('CTF', 'Conference')),  
    format VARCHAR(50), \-- Online, Onsite  
    url TEXT,  
    description TEXT,  
    weight FLOAT DEFAULT 0, \-- Importance score  
    raw\_source JSONB \-- Store original data for debugging  
);

CREATE TABLE subscriptions (  
    user\_id UUID,  
    webhook\_url TEXT,  
    filter\_tags TEXT\[\],  
    PRIMARY KEY (user\_id)  
);

## **4\. Automation & Notifications**

* **Discord Integration:** Send POST requests to user-provided Webhook URLs.  
* **Payload Format:**  
  {  
    "content": "🚨 \*\*New CTF Alert:\*\* DEFCON Quals",  
    "embeds": \[{  
      "title": "DEFCON CTF Qualifiers",  
      "description": "Format: Jeopardy | Weight: 100",  
      "url": "\[https://ctftime.org/event/\](https://ctftime.org/event/)...",  
      "color": 15158332  
    }\]  
  }

## **5\. Security Controls**

1. **Input Validation:** Use Pydantic models for all incoming data.  
2. **Outbound Traffic:** Firewall the scraping worker to only allow connections to specific ports (80, 443).  
3. **Database:** Use read-only replicas for the public API if scaling.