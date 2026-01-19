# Contributing to CTF & Conference Tracker

## Development Setup

1. **Prerequisites**:
   - Docker & Docker Compose
   - Python 3.11+ (if running locally)

2. **Quick Start**:
   ```bash
   ./scripts/setup.sh
   ```

3. **Running the Stack**:
   ```bash
   docker-compose -f deploy/docker-compose.yml up --build
   ```

## Workflow

1. **Branching**:
   - `main`: Stable production code.
   - `dev`: Integration branch.
   - `feature/xxx`: Your new features.

2. **Commits**:
   - Use Conventional Commits (e.g., `feat: add scraper`, `fix: scraper timeout`).

3. **Testing**:
   - Run tests before PR: `pytest`

## Code Style
- We use `black` and `isort`.
- Run formatting: `black src && isort src`

## Adding a New Scraper
1. Create a new file in `src/app/workers/scrapers/`.
2. Inherit from `BaseScraper`.
3. Register the task in `src/app/workers/tasks.py`.
