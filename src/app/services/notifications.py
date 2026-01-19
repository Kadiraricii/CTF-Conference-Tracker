import httpx
import logging
from typing import List
from src.app.core.config import settings
from src.app.db.models import Event

logger = logging.getLogger(__name__)

class NotificationService:
    TELEGRAM_API_URL = "https://api.telegram.org/bot"

    @classmethod
    async def send_telegram_message(cls, chat_id: str, message: str):
        """Send a raw message to a specific chat."""
        if not settings.TELEGRAM_BOT_TOKEN:
            logger.warning("TELEGRAM_BOT_TOKEN not set. Skipping notification.")
            return

        url = f"{cls.TELEGRAM_API_URL}{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=payload, timeout=10.0)
                if response.status_code != 200:
                    logger.error(f"Failed to send Telegram msg: {response.text}")
            except Exception as e:
                logger.error(f"Error sending Telegram msg: {e}")

    @classmethod
    async def notify_new_events(cls, events: List[Event]):
        """Send a summary of new events to admins."""
        if not events:
            return

        if not settings.TELEGRAM_ADMIN_IDS:
            logger.warning("No TELEGRAM_ADMIN_IDS configured. Skipping notification.")
            return

        # Prepare Message
        # Telegram has a limit (4096 chars), so keep it brief or split.
        # For now, we assume batch size isn't huge (50 items) but we should be careful.
        
        header = f"🚨 <b>{len(events)} New CTF Events Found!</b>\n\n"
        body = ""
        for event in events[:10]: # Limit to top 10 to avoid spamming/limit issues
            start = event.start_time.strftime("%Y-%m-%d")
            body += f"🔹 <a href='{event.url}'>{event.title}</a> ({start})\n"
        
        if len(events) > 10:
            body += f"\n<i>...and {len(events) - 10} more.</i>"

        full_message = header + body

        # Send to all admins
        for admin_id in settings.TELEGRAM_ADMIN_IDS:
            await cls.send_telegram_message(str(admin_id), full_message)
