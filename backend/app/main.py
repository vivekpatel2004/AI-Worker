from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.api import routes_events, routes_seed, routes_metrics

app = FastAPI(title="AI Worker Productivity Dashboard")

# ---------------- CORS CONFIG ----------------
origins = [
    "http://localhost:5174",
    "http://127.0.0.1:5174",
    "https://ai-worker-ten.vercel.app",   # 👈 your Vercel frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ------------------------------------------------

# Create tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(routes_events.router)
app.include_router(routes_seed.router)
app.include_router(routes_metrics.router)

@app.get("/")
def root():
    return {"message": "Backend Running"}