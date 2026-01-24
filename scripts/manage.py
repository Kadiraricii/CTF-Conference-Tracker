#!/usr/bin/env python3
import click
import asyncio
from src.app.db.session import engine, Base


@click.group()
def cli():
    pass


@cli.command(name="init_db")
def init_db():
    """Create database tables."""

    async def _init():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("Database tables created.")

    asyncio.run(_init())


@cli.command(name="run_worker")
def run_worker():
    """Run the user-facing worker (wrapper around arq)."""
    import subprocess

    subprocess.run(["arq", "src.app.workers.tasks.WorkerSettings"])


@cli.command(name="trigger_ingest")
def trigger_ingest():
    """Trigger the CTFtime ingestion task via Redis."""
    from arq import create_pool
    from arq.connections import RedisSettings
    from src.app.core.config import settings

    async def _trigger():
        redis = await create_pool(
            RedisSettings(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
        )
        await redis.enqueue_job("ingest_ctftime_events", limit=50)
        print("Job 'ingest_ctftime_events' enqueued successfully.")
        await redis.aclose()

    asyncio.run(_trigger())


@cli.command(name="self_check")
def self_check():
    """Perform a system-wide self check and exit with status code."""
    from src.app.services.health import check_health_status
    import sys
    import json

    async def _check():
        print("Running Self-Check...")
        result = await check_health_status()
        print(json.dumps(result, indent=2))

        if result["overall"] != "PASS":
            sys.exit(1)
        else:
            sys.exit(0)

    asyncio.run(_check())


@cli.command()
def test():
    """Run automated tests using pytest."""
    import subprocess
    import sys

    print("Running Auto-Tests...")
    # Run pytest with logical flags
    # -v: verbose
    # -p no:warnings: suppress deprecation warnings for cleaner output
    result = subprocess.run(["pytest", "-v", "-p", "no:warnings"], cwd=".")
    if result.returncode != 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    cli()
