"""
Incident Management System - Backend Entry Point
FastAPI application with WebSocket support for real-time incident tracking.
"""

import threading
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routes import incidents, alerts, websocket, teams, users
from tasks.check_ack_timeouts import run_ack_checker
from tasks.watcher import run_watcher

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Incident Management System",
    description="Event-driven incident management API for DevOps alert handling",
    version="1.0.0",
)

# CORS middleware - allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(incidents.router, prefix="/api/incidents", tags=["Incidents"])
app.include_router(alerts.router, prefix="/api/alerts", tags=["Alerts"])
app.include_router(teams.router, prefix="/api/teams", tags=["Teams"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(websocket.router, tags=["WebSocket"])


@app.on_event("startup")
def start_background_tasks():
    threading.Thread(target=run_ack_checker, daemon=True).start()
    threading.Thread(target=run_watcher, daemon=True).start()

@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint."""
    return {"status": "running", "service": "Incident Management System"}
