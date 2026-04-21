"""
WebSocket Routes.
Provides real-time updates to the frontend dashboard.
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from anyio import from_thread
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


class ConnectionManager:
    """Manages active WebSocket connections for broadcasting updates."""

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"Client connected. Total connections: {len(self.active_connections)}")
        await websocket.send_json({"type": "connection", "status": "connected"})

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"Client disconnected. Total connections: {len(self.active_connections)}")

    async def broadcast(self, message: dict):
        """Send a message to all connected clients."""
        stale_connections: List[WebSocket] = []
        for connection in list(self.active_connections):
            try:
                await connection.send_json(message)
            except Exception:
                stale_connections.append(connection)

        for connection in stale_connections:
            self.disconnect(connection)


# Global connection manager instance
manager = ConnectionManager()


async def broadcast_incident_event(
    event_type: str,
    incident: Optional[dict] = None,
    incident_id: Optional[int] = None,
):
    """Broadcast a normalized incident event to connected clients."""
    message = {"type": event_type}
    if incident is not None:
        message["incident"] = incident
    if incident_id is not None:
        message["incident_id"] = incident_id
    await manager.broadcast(message)


def queue_incident_event(
    event_type: str,
    incident: Optional[dict] = None,
    incident_id: Optional[int] = None,
):
    """Bridge sync API routes to the async websocket broadcaster."""
    try:
        from_thread.run(broadcast_incident_event, event_type, incident, incident_id)
    except RuntimeError:
        logger.warning(
            "Skipped websocket broadcast for %s because no request event loop was available.",
            event_type,
        )


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time incident updates."""
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive, listen for client messages
            data = await websocket.receive_text()
            # Echo back or handle client commands
            await websocket.send_json({"type": "ack", "message": f"Received: {data}"})
    except WebSocketDisconnect:
        manager.disconnect(websocket)
