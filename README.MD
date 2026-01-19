# CTF & Conference Tracker (MVP)

A centralized intelligence platform for tracking global cybersecurity events (CTFs and Conferences).
Built with **FastAPI**, **PostgreSQL**, **Redis/ARQ**, and **Telegram Notifications**.

> **Project Status**: Phase 1 MVP (API + CLI Only).

## 🚀 Quick Start

### Option A: Docker Compose (Preferred)
The easiest way to run the full stack (API + Worker + DB + Redis).

```bash
# 1. Setup Environment
./scripts/setup.sh    # Creates .env from example

# 2. Build & Run
docker-compose -f deploy/docker-compose.yml up --build -d

# 3. Access
# API Docs: http://localhost:8000/docs
```

### Option B: Local Development (Virtualenv)
If you want to run services locally (requires Postgres/Redis installed).

```bash
# 1. Setup Environment
./scripts/setup.sh    # Answer 'y' to create venv

# 2. Activate
source venv/bin/activate

# 3. Run API
uvicorn src.main:app --reload

# 4. Run Worker (in another terminal)
arq src.app.workers.tasks.WorkerSettings
```

## 🏗 Architecture

- **Backend**: Python 3.11 + FastAPI
- **Database**: PostgreSQL (Async SQLAlchemy)
- **Queue**: ARQ (Async Redis Queue) for scrapers
- **Notifications**: Telegram Bot API

## 📂 Repository Structure

```text
├── deploy/           # Docker configs
├── scripts/          # Automation scripts
├── src/
│   ├── app/
│   │   ├── api/      # REST Endpoints
│   │   ├── core/     # Config & Settings
│   │   ├── db/       # Models & Session
│   │   └── workers/  # ARQ Tasks & Scrapers
│   └── main.py       # Entrypoint
```

## 🤝 Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for style guides and scraper development instructions.
