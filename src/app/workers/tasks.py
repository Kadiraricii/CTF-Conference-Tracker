from arq.connections import RedisSettings
from datetime import timedelta
from src.app.core.config import settings

from src.app.workers.scrapers.ctftime import ingest_ctftime_events
from src.app.workers.scrapers.rss import ingest_rss_feeds

async def startup(ctx):
    print("ARQ Worker Starting...")

async def shutdown(ctx):
    print("ARQ Worker Shutting down...")

async def sample_task(ctx, word: str):
    print(f"Processing task: {word}")
    return f"Hello {word}"

class WorkerSettings:
    functions = [sample_task, ingest_ctftime_events, ingest_rss_feeds]
    redis_settings = RedisSettings(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT
    )
    on_startup = startup
    on_shutdown = shutdown
    job_timeout = timedelta(minutes=10)
