#!/usr/bin/env python3
import click
import asyncio
from src.app.db.session import engine, Base

@click.group()
def cli():
    pass

@cli.command()
def init_db():
    """Create database tables."""
    async def _init():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("Database tables created.")
    
    asyncio.run(_init())


@cli.command()
def run_worker():
    """Run the user-facing worker (wrapper around arq)."""
    import subprocess
    subprocess.run(["arq", "src.app.workers.tasks.WorkerSettings"])

@cli.command()
def trigger_ingest():
    """Trigger the CTFtime ingestion task via Redis."""
    from arq import create_pool
    from arq.connections import RedisSettings
    from src.app.core.config import settings

    async def _trigger():
        redis = await create_pool(
            RedisSettings(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
        )
        job = await redis.enqueue_job("ingest_ctftime_events", 50)
        print("Enqueued job:", job.job_id)
        await redis.close()

    asyncio.run(_trigger())


if __name__ == "__main__":
    cli()
