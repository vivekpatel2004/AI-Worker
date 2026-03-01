from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EventCreate(BaseModel):
    timestamp: datetime
    worker_id: str
    workstation_id: str
    event_type: str
    confidence: Optional[float] = 0
    count: Optional[int] = 0