from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.event import Event
from collections import defaultdict

router = APIRouter(prefix="/metrics", tags=["Metrics"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- WORKER METRICS ----------------

@router.get("/workers")
def worker_metrics(
    min_confidence: float = Query(0.0),
    db: Session = Depends(get_db)
):

    events = db.query(Event).order_by(Event.worker_id, Event.timestamp).all()

    worker_events = defaultdict(list)

    for e in events:
        worker_events[e.worker_id].append(e)

    results = []

    for worker_id, ev_list in worker_events.items():

        active = 0
        idle = 0
        units = 0

        for i in range(len(ev_list) - 1):
            curr = ev_list[i]
            next_event = ev_list[i + 1]

            duration = (next_event.timestamp - curr.timestamp).total_seconds() / 60

            if curr.event_type == "working":
                active += duration
            elif curr.event_type == "idle":
                idle += duration

            if curr.event_type == "product_count":
                units += curr.count

        total_time = active + idle
        utilization = (active / total_time * 100) if total_time > 0 else 0
        units_per_hour = (units / (active / 60)) if active > 0 else 0

        results.append({
            "worker_id": worker_id,
            "active_minutes": round(active, 2),
            "idle_minutes": round(idle, 2),
            "utilization_percent": round(utilization, 2),
            "total_units": units,
            "units_per_hour": round(units_per_hour, 2)
        })

    return results


# ---------------- WORKSTATION METRICS ----------------

@router.get("/workstations")
def workstation_metrics(db: Session = Depends(get_db)):

    events = db.query(Event).order_by(Event.workstation_id, Event.timestamp).all()

    station_events = defaultdict(list)

    for e in events:
        station_events[e.workstation_id].append(e)

    results = []

    for station_id, ev_list in station_events.items():

        occupancy = 0
        units = 0

        for i in range(len(ev_list) - 1):
            curr = ev_list[i]
            next_event = ev_list[i + 1]

            duration = (next_event.timestamp - curr.timestamp).total_seconds() / 60

            if curr.event_type == "working":
                occupancy += duration

            if curr.event_type == "product_count":
                units += curr.count

        throughput = (units / (occupancy / 60)) if occupancy > 0 else 0

        results.append({
            "station_id": station_id,
            "occupancy_minutes": round(occupancy, 2),
            "total_units": units,
            "throughput_per_hour": round(throughput, 2)
        })

    return results


# ---------------- FACTORY METRICS ----------------

@router.get("/factory")
def factory_metrics(db: Session = Depends(get_db)):

    events = db.query(Event).order_by(Event.timestamp).all()

    active = 0
    units = 0

    for i in range(len(events) - 1):
        curr = events[i]
        next_event = events[i + 1]

        duration = (next_event.timestamp - curr.timestamp).total_seconds() / 60

        if curr.event_type == "working":
            active += duration

        if curr.event_type == "product_count":
            units += curr.count

    avg_production_rate = (units / (active / 60)) if active > 0 else 0

    return {
        "total_active_minutes": round(active, 2),
        "total_production_units": units,
        "average_production_rate_per_hour": round(avg_production_rate, 2)
    }