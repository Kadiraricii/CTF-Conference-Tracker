from fastapi import APIRouter, Depends, Response
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.db.session import get_db
from src.app.db.models import Event
from ics import Calendar, Event as IcsEvent
from datetime import datetime

router = APIRouter()


@router.get("/ctf.ics", response_class=Response)
async def get_cal_feed(db: AsyncSession = Depends(get_db)):
    """
    Generate an ICS feed for all upcoming CTFs.
    """
    # Fetch upcoming events
    query = (
        select(Event)
        .where(Event.start_time > datetime.now())
        .order_by(Event.start_time.asc())
    )
    result = await db.execute(query)
    db_events = result.scalars().all()

    cal = Calendar()
    cal.creator = "CTF Tracker MVP"

    for e in db_events:
        c = IcsEvent()
        c.name = f"[{e.type.upper()}] {e.title}"
        c.begin = e.start_time
        c.end = e.end_time
        c.description = (
            f"{e.description}\n\nFormat: {e.format}\nWeight: {e.weight}\n\nURL: {e.url}"
        )
        c.url = e.url
        c.location = e.format if e.format else "Online"

        cal.events.add(c)

    return Response(content=str(cal), media_type="text/calendar")
