
from sqlalchemy import Column, Integer, String, Float, DateTime, UniqueConstraint
from app.database import Base
from datetime import datetime

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, index=True)
    worker_id = Column(String, index=True)
    workstation_id = Column(String, index=True)
    event_type = Column(String)
    confidence = Column(Float)
    count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("worker_id", "timestamp", "event_type", name="unique_event"),
    )