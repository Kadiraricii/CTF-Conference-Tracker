from datetime import datetime, timezone
import httpx
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.db.session import AsyncSessionLocal
from src.app.db.models import Event
from src.app.workers.scrapers import BaseScraper
import logging

logger = logging.getLogger(__name__)

class CTFTimeScraper(BaseScraper):
    BASE_URL = "https://ctftime.org/api/v1/events/"
    
    async def fetch_events(self, limit: int = 100):
        """Fetch upcoming events from CTFtime API."""
        params = {
            "limit": limit,
            "start": int(datetime.now().timestamp()),
            "finish": int(datetime.now().timestamp()) + 31536000 # +1 Year
        }
        headers = {
            "User-Agent": "CTFTracker/1.0 (Student Project; Contact: admin@example.com)"
        }
        
        logger.info(f"Fetching events from {self.BASE_URL} with params {params}")
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(self.BASE_URL, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            logger.info(f"Fetched {len(data)} events from API.")
            return data

    async def normalize_and_save(self, events_data: list):
        """Normalize CTF/Conf data and upsert into DB."""
        count = 0
        async with AsyncSessionLocal() as session:
            for item in events_data:
                source_id = f"ctftime_{item['id']}"
                
                # Check for updates (idempotency)
                query = select(Event).where(Event.source_id == source_id)
                result = await session.execute(query)
                existing_event = result.scalar_one_or_none()

                # Robust datetime parsing
                try:
                    start = datetime.fromisoformat(item['start'].replace('Z', '+00:00'))
                    end = datetime.fromisoformat(item['finish'].replace('Z', '+00:00'))
                except ValueError:
                    logger.error(f"Failed to parse dates for event {item.get('title')}: {item.get('start')}/{item.get('finish')}")
                    continue

                event_data = {
                    "source_id": source_id,
                    "title": item['title'],
                    "description": item.get('description', ''),
                    "url": item.get('url', '') or item.get('ctftime_url', ''),
                    "logo_url": item.get('logo', ''),
                    "type": "ctf", # CTFtime mostly lists CTFs
                    "format": item.get('format', 'Jeopardy'),
                    "start_time": start,
                    "end_time": end,
                    "weight": float(item.get('weight', 0)),
                    "meta": item # Store raw payload
                }
                
                if existing_event:
                    # Update fields
                    for key, value in event_data.items():
                        setattr(existing_event, key, value)
                else:
                    # Create new
                    new_event = Event(**event_data)
                    session.add(new_event)
                count += 1
            
            await session.commit()
            logger.info(f"Synced {count} events from CTFtime.")
            return count

# ARQ Job Function
async def ingest_ctftime_events(ctx, limit: int = 100):
    logger.info("Starting CTFtime Ingest Job")
    scraper = CTFTimeScraper()
    try:
        data = await scraper.fetch_events(limit=limit)
        count = await scraper.normalize_and_save(data)
        return f"Successfully ingested {count} events"
    except Exception as e:
        logger.error(f"Error during ingestion: {e}")
        raise e
