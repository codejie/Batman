from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import StreamingResponse
from app.routers.common import verify_token
import asyncio
from typing import Dict, List

class ConnectionManager:
    def __init__(self):
        # Store active connections as: {user_id: [EventSource_Queue]}
        self.active_connections: Dict[int, List[asyncio.Queue]] = {}

    async def connect(self, user_id: int) -> asyncio.Queue:
        """A new client connects, create a new queue for them."""
        # Allow multiple connections for the same user (e.g., multiple browser tabs)
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        
        queue = asyncio.Queue()
        self.active_connections[user_id].append(queue)
        print(f"User {user_id} connected. Total connections for user: {len(self.active_connections[user_id])}")
        return queue

    def disconnect(self, user_id: int, queue: asyncio.Queue):
        """A client disconnects, remove their queue."""
        if user_id in self.active_connections:
            self.active_connections[user_id].remove(queue)
            # If the user has no more active connections, remove the user entry
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
        print(f"User {user_id} disconnected.")

    async def send_personal_message(self, user_id: int, message: str):
        """Send a message to a specific user."""
        if user_id in self.active_connections:
            for queue in self.active_connections[user_id]:
                await queue.put(message)

# Create a single instance of the manager to be used by the application
manager = ConnectionManager()

# The router
router = APIRouter(
    prefix="/sse",
    tags=["sse"]
)

async def event_generator(request: Request, user_id: int):
    """
    Yields server-sent events for a specific user.
    """
    queue = await manager.connect(user_id)
    try:
        while True:
            # Wait for a new message to be added to the queue
            message = await queue.get()
            if await request.is_disconnected():
                break
            yield f"data: {message}\n\n"
    except asyncio.CancelledError:
        # This block is executed when the client disconnects
        pass
    finally:
        manager.disconnect(user_id, queue)
        print(f"Stopped event generation for user {user_id}")


@router.get("/report")
async def report(request: Request, uid: int = verify_token()):
    """
    Establishes an SSE connection for the authenticated user.
    """
    # if not current_user:
    #     raise HTTPException(status_code=403, detail="Not authenticated")
    
    # user_id = current_user.id 
    return StreamingResponse(event_generator(request, uid), media_type="text/event-stream")

# Example of how to use the manager from another part of your app
@router.post("/send/{user_id}")
async def send_message_to_user(user_id: int, message: str):
    """
    An example endpoint to trigger sending a message to a specific user.
    In a real app, this logic would be in your services or background tasks.
    """
    await manager.send_personal_message(user_id, f"A message for you: {message}")
    return {"status": "message sent"}