from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.event import Event
from app.schemas.event_schema import EventCreate

router = APIRouter(prefix="/events", tags=["Events"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/ingest")
def ingest_event(data: EventCreate, db: Session = Depends(get_db)):
    try:
        event = Event(
            timestamp=data.timestamp,   # ✅ FIXED
            worker_id=data.worker_id,
            workstation_id=data.workstation_id,
            event_type=data.event_type,
            confidence=data.confidence,
            count=data.count
        )

        db.add(event)
        db.commit()
        db.refresh(event)

        return {"message": "Event ingested successfully"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))