import httpx
import logging
import defusedxml.ElementTree as ET
from datetime import datetime, timezone

# Actually, better to inherit BaseScraper and reuse a similar save logic or abstract it.
from src.app.workers.scrapers import BaseScraper
from src.app.db.models import Event
from src.app.db.session import AsyncSessionLocal
from sqlalchemy.future import select

logger = logging.getLogger(__name__)


class RSSScraper(BaseScraper):
    # Example Feeds (Security Conferences / News)
    FEEDS = [
        "https://www.usenix.org/rss.xml",  # USENIX Conferences
        # Add more here
    ]

    async def fetch_feed(self, url: str):
        logger.info(f"Fetching RSS feed: {url}")
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.text

    def parse_feed(self, xml_content: str, source_label: str):
        events = []
        try:
            root = ET.fromstring(xml_content)
            # Handle standard RSS 2.0
            channel = root.find("channel")
            if channel is None:
                # Try Atom? For now assume RSS
                return []

            for item in channel.findall("item"):
                title = (
                    item.find("title").text
                    if item.find("title") is not None
                    else "No Title"
                )
                link = item.find("link").text if item.find("link") is not None else ""
                desc = (
                    item.find("description").text
                    if item.find("description") is not None
                    else ""
                )

                # Basic normalization
                events.append(
                    {
                        "id": link,  # Use link as unique ID
                        "title": title,
                        "url": link,
                        "description": desc,
                        "start": datetime.now(
                            timezone.utc
                        ).isoformat(),  # RSS items often lack future event dates, using now as placeholder for "News"
                        "finish": datetime.now(timezone.utc).isoformat(),
                        "source": source_label,
                    }
                )
        except Exception as e:
            logger.error(f"Error parsing XML: {e}")

        return events

    async def normalize_and_save(self, items: list):
        """Similar to CTFtime, but adapted for RSS items."""
        count = 0
        new_events = []
        async with AsyncSessionLocal() as session:
            for item in items:
                source_id = f"rss_{hash(item['id'])}"

                query = select(Event).where(Event.source_id == source_id)
                result = await session.execute(query)
                if result.scalar_one_or_none():
                    continue

                new_event = Event(
                    source_id=source_id,
                    title=item["title"],
                    description=item["description"][:500] + "...",  # Truncate check
                    url=item["url"],
                    type="conference",  # Assume RSS feeds track confs/news
                    start_time=datetime.fromisoformat(item["start"]),
                    end_time=datetime.fromisoformat(item["finish"]),
                    meta={"source": item["source"]},
                )
                session.add(new_event)
                new_events.append(new_event)
                count += 1

            await session.commit()
            return new_events


async def ingest_rss_feeds(ctx):
    from src.app.services.notifications import NotificationService

    logger.info("Starting RSS Ingest Job")
    scraper = RSSScraper()
    total_new = 0

    for feed_url in scraper.FEEDS:
        try:
            xml = await scraper.fetch_feed(feed_url)
            items = scraper.parse_feed(xml, source_label=feed_url)
            new_events = await scraper.normalize_and_save(items)

            if new_events:
                await NotificationService.notify_new_events(new_events)
                total_new += len(new_events)

        except Exception as e:
            logger.error(f"Failed to process feed {feed_url}: {e}")

    return f"RSS Ingest Complete. New items: {total_new}"
