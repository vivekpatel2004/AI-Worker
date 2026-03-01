🚀 AI-Powered Worker Productivity Dashboard
📌 Overview

This project simulates an AI-powered CCTV monitoring system for a manufacturing factory.
The system ingests structured AI-generated events and computes productivity metrics at:

Worker Level

Workstation Level

Factory Level

It demonstrates full-stack engineering with ML Ops considerations, scalability planning, and production-ready architecture.

🏗 Architecture Overview
🔄 End-to-End Data Flow
AI CCTV Cameras (Edge)
        ↓
FastAPI Backend (Event Ingestion API)
        ↓
SQLite Database (Persistent Storage)
        ↓
Metrics Computation Layer
        ↓
React Dashboard (Visualization)
🧩 System Components
1️⃣ Edge Layer (Simulated)

AI-powered computer vision system generates structured events such as:

working

idle

absent

product_count

2️⃣ Backend (FastAPI)

Handles:

Event ingestion

Data persistence

Metric computation

Seed data generation

Confidence filtering

3️⃣ Database (SQLite)

Stores:

Workers

Workstations

AI Events

4️⃣ Frontend (React + Tailwind)

Displays:

Factory summary

Worker metrics

Workstation metrics

Filtering options

🗄 Database Schema
Workers Table
Column	Description
id	Primary Key
worker_id	Unique Worker Identifier (W1–W6)
name	Worker Name
Workstations Table
Column	Description
id	Primary Key
station_id	Unique Station Identifier (S1–S6)
name	Station Name
Events Table
Column	Description
id	Primary Key
timestamp	Event time
worker_id	Associated worker
workstation_id	Associated station
event_type	working / idle / absent / product_count
confidence	Model confidence score
count	Units produced (for product_count events)
created_at	Record creation time
🔐 Data Integrity

A composite unique constraint prevents duplicate events:

(worker_id, timestamp, event_type)

This ensures idempotent ingestion.

📊 Metrics Definition & Logic
🧑 Worker-Level Metrics
🔹 Active Time

Calculated as the time difference between consecutive working state events.

🔹 Idle Time

Calculated as the time difference between consecutive idle state events.

🔹 Utilization Percentage
Utilization % = Active Time / (Active Time + Idle Time) × 100
🔹 Total Units Produced

Sum of count for all product_count events.

🔹 Units per Hour
Units per Hour = Total Units / Active Hours
🏭 Workstation-Level Metrics
🔹 Occupancy Time

Total duration where event_type = working at that station.

🔹 Throughput Rate
Throughput = Total Units / Occupancy Hours
🏢 Factory-Level Metrics

Total Active Minutes

Total Production Units

Average Production Rate per Hour

🧠 Assumptions

Event duration is calculated using the time difference between consecutive state events.

Events are sorted by timestamp before computing metrics.

Production events are aggregated by summing the count field.

The last event duration is not extended beyond available timestamps.

Only events above min_confidence threshold are considered when filtering.

⚠️ Handling Real-World Edge Cases
1️⃣ Intermittent Connectivity

In real-world deployment:

Edge devices buffer events locally.

Events are sent in batches once connectivity is restored.

Backend supports batch ingestion.

2️⃣ Duplicate Events

Prevented using:

Database-level composite unique constraint

Idempotent ingestion logic

3️⃣ Out-of-Order Timestamps

Mitigation:

Events are sorted by timestamp before metric computation.

Insertion order is never used for calculations.

🤖 ML Ops Considerations

Although no ML model is implemented in this assessment, the system is designed with ML Ops best practices.

🔹 Confidence Filtering

Frontend allows filtering events based on:

min_confidence

This simulates real-world noise reduction in computer vision outputs.

🔹 Model Versioning (Future Ready)

The system can be extended with:

model_version column

to track:

Which model generated which events

Performance comparison across versions

🔹 Drift Detection Strategy

Potential drift detection signals:

Drop in average confidence scores

Sudden changes in idle/working distribution

Production anomalies

🔹 Retraining Trigger Strategy

Retraining can be triggered if:

Confidence mean drops below threshold

Error rates increase

QA validation detects systematic errors

📈 Scaling Strategy
From 5 Cameras → 100+ Cameras

Recommended enhancements:

Introduce Kafka for event streaming

Async background workers for ingestion

Horizontal backend scaling

Database indexing & partitioning

Multi-Site Deployment

Add:

factory_id column

Benefits:

Partition by site

Multi-factory dashboard support

Centralized monitoring

🖥 Running Locally
Backend
cd backend
uvicorn app.main:app --reload

Backend runs at:

http://127.0.0.1:8000
Frontend
cd frontend
npm install
npm run dev

Frontend runs at:

http://localhost:5174
🌱 Seeding Demo Data

You can seed demo data using:

POST /seed/data

Or click "Seed Data" button in the UI.

🐳 (Optional) Docker Deployment

If Docker is configured:

docker-compose up --build

This will start:

Backend service

Frontend service

🧪 Features Implemented

✅ Event ingestion API
✅ Data persistence
✅ Worker metrics
✅ Workstation metrics
✅ Factory metrics
✅ Confidence filtering
✅ Duplicate prevention
✅ Out-of-order handling
✅ Seed data generation
✅ Interactive dashboard
✅ Worker filter dropdown
✅ Production-ready architecture

🎯 Design Goals Achieved

Clean layered architecture

ML-aware event handling

Production-ready ingestion logic

Scalable system design

Clear separation of concerns

Real-time analytics dashboard

👨‍💻 Tech Stack

Backend

FastAPI

SQLAlchemy

SQLite

Frontend

React (Vite)

Tailwind CSS

Axios

Containerization

Docker (optional)

📌 Conclusion

This project demonstrates:

Full-stack engineering capability

ML Ops awareness

Data modeling expertise

Metric computation logic

Production-level architectural thinking

Scalability planning

It reflects how an AI-driven monitoring system can be built, extended, and scaled in real-world manufacturing environments.