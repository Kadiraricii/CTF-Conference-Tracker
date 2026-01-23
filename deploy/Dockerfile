FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry (or just use pip for simplicity in MVP, but pyproject.toml implies poetry)
# For MVP simplicity with Docker, we'll just pip install .
COPY pyproject.toml .
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

# Copy Application
COPY src/ src/
COPY scripts/ scripts/
COPY alembic.ini .
COPY alembic/ alembic/
COPY tests/ tests/

ENV PYTHONPATH=/app

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

