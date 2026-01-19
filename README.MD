# CTF & Conference Tracker

A centralized intelligence platform for tracking global cybersecurity events (CTFs and Conferences).
Built with **FastAPI**, **PostgreSQL**, **Redis/ARQ**, and **Telegram Notifications**.

> **Project Status**: Phase 3 (Automation & Standards Implemented).

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

## 🛠 Management CLI
The project includes a `manage.py` script for automation and maintenance.

**Inside Container:**
```bash
docker exec -it deploy-backend-1 python scripts/manage.py [COMMAND]
```

**Commands:**
- `self-check`: Verify connections to DB, Redis, and API.
- `test`: Run the automated Pytest suite.
- `init-db`: Initialize database tables manually.
- `trigger-ingest`: Manually trigger the CTFtime scraper job.
- `run-worker`: Start the ARQ worker process.

## 🏗 Architecture

- **Backend**: Python 3.11 + FastAPI
- **Database**: PostgreSQL (Async SQLAlchemy)
- **Queue**: ARQ (Async Redis Queue) for scrapers
- **Notifications**: Telegram Bot API
- **Automation**: Self-healing checks and regression tests.

## 📂 Repository Structure

```text
├── deploy/           # Docker configs
├── docs/             # Project documentation
├── researches/       # Deep dive analysis artifacts
├── scripts/          # Automation (setup.sh, manage.py)
├── src/
│   ├── app/
│   │   ├── api/      # REST Endpoints
│   │   ├── core/     # Config & Settings
│   │   ├── db/       # Models & Session
│   │   └── workers/  # ARQ Tasks & Scrapers
│   └── main.py       # Entrypoint
├── project_info.json # Project metadata
```

## 🤝 Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for style guides and scraper development instructions.
