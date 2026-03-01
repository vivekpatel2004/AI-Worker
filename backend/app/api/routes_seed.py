from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.worker import Worker
from app.models.workstation import Workstation
from app.models.event import Event
from datetime import datetime, timedelta
import random

router = APIRouter(prefix="/seed", tags=["Seed"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/data")
def seed_data(db: Session = Depends(get_db)):

    db.query(Event).delete()
    db.query(Worker).delete()
    db.query(Workstation).delete()
    db.commit()

    # Workers
    for i in range(1, 7):
        db.add(Worker(worker_id=f"W{i}", name=f"Worker {i}"))

    # Workstations
    for i in range(1, 7):
        db.add(Workstation(station_id=f"S{i}", name=f"Station {i}"))

    db.commit()

    # Events
    base_time = datetime.utcnow()

    for i in range(200):
        db.add(Event(
            timestamp=base_time + timedelta(minutes=i*5),
            worker_id=f"W{random.randint(1,6)}",
            workstation_id=f"S{random.randint(1,6)}",
            event_type=random.choice(["working", "idle", "product_count"]),
            confidence=round(random.uniform(0.8, 0.99), 2),
            count=random.randint(1,5)
        ))

    db.commit()

    return {"message": "Seed data created successfully"}