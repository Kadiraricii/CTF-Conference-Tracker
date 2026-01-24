import logging
from sqlalchemy import text
from src.app.db.session import AsyncSessionLocal
from src.app.core.config import settings
from redis import asyncio as aioredis  # Use async redis

logger = logging.getLogger(__name__)


async def check_health_status() -> dict:
    """
    Perform self-check on all components.
    Returns a dict with status of each component.
    """
    status = {
        "api": "PASS",
        "database": "FAIL",
        "redis": "FAIL",
        "data": "FAIL",
        "overall": "FAIL",
    }

    # 1. Database Check
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
            # Check Data Count
            result = await session.execute(text("SELECT count(*) FROM events"))
            count = result.scalar()
            status["database"] = "PASS"
            status["data"] = "PASS" if count > 0 else "WARN (0 events)"
    except Exception as e:
        logger.error(f"DB Health Check Failed: {e}")
        status["database"] = f"FAIL: {str(e)}"

    # 2. Redis Check
    try:
        redis = aioredis.from_url(
            f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}"
        )
        await redis.ping()
        await redis.close()
        status["redis"] = "PASS"
    except Exception as e:
        logger.error(f"Redis Health Check Failed: {e}")
        status["redis"] = f"FAIL: {str(e)}"

    # Overall Logic
    if status["database"].startswith("PASS") and status["redis"].startswith("PASS"):
        status["overall"] = "PASS"

    return status
