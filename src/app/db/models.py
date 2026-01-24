from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

from src.app.db.session import Base

class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # Core Fields
    title: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    url: Mapped[str] = mapped_column(String, nullable=False)
    logo_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    # Classification
    type: Mapped[str] = mapped_column(String, default="ctf", index=True) # ctf, conference
    format: Mapped[Optional[str]] = mapped_column(String, nullable=True) # Jeopardy, Attack-Defense
    
    # Timing (UTC)
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    
    # Metadata
    weight: Mapped[float] = mapped_column(Float, default=0.0)
    source_id: Mapped[str] = mapped_column(String, unique=True, index=True) # e.g. ctftime_123
    
    # Flexible Storage (Raw Payload + Extra Fields)
    meta: Mapped[dict] = mapped_column(JSONB, default=dict)

    def __repr__(self):
        return f"<Event {self.title} ({self.start_time})>"
