from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.db.session import get_db
from src.app.db.models import Event
from datetime import datetime

router = APIRouter()

@router.get("/", response_model=List[dict])
async def list_events(
    db: AsyncSession = Depends(get_db),
    type: Optional[str] = Query(None, description="Filter by type (ctf, conference)"),
    status: Optional[str] = Query(None, description="upcoming, past"),
    limit: int = 100
):
    """
    List events with optional filtering.
    """
    query = select(Event)
    
    if type:
        query = query.where(Event.type == type)
    
    if status == "upcoming":
        query = query.where(Event.start_time > datetime.now())
    elif status == "past":
        query = query.where(Event.end_time < datetime.now())
        
    query = query.order_by(Event.start_time.asc()).limit(limit)
    
    result = await db.execute(query)
    events = result.scalars().all()
    
    # Simple manual serialization for MVP (Pydantic models later)
    return [{
        "id": e.id,
        "title": e.title,
        "start_time": e.start_time,
        "end_time": e.end_time,
        "type": e.type,
        "format": e.format,
        "weight": e.weight,
        "url": e.url,
        "logo": e.logo_url
    } for e in events]

@router.get("/{event_id}")
async def get_event(event_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get details of a specific event.
    """
    result = await db.execute(select(Event).where(Event.id == event_id))
    event = result.scalar_one_or_none()
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
        
    return {
        "id": event.id,
        "title": event.title,
        "description": event.description,
        "raw_metadata": event.meta,
        **{k: getattr(event, k) for k in ["start_time", "end_time", "url", "type", "format"]}
    }
