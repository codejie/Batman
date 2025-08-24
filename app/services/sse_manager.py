import asyncio
import json
from typing import Dict
from fastapi import Request

from app.services.task_manager import taskManager
from app.logger import logger

class ConnectionManager:
  def __init__(self):
    # Store active connections as: {uid: {type: Queue}}
    self.active_connections: Dict[int, Dict[str, asyncio.Queue]] = {}

  async def connect(self, uid: int, type: str) -> asyncio.Queue:
    """A new client connects, create a new queue for them based on user and type."""
    if uid not in self.active_connections:
      self.active_connections[uid] = {}
    
    # If a connection for this uid and type already exists, it will be replaced.
    # The old connection will stop receiving messages.
    queue = asyncio.Queue()
    self.active_connections[uid][type] = queue
    logger.info(f"User {uid} connected with type '{type}'.")
    return queue

  def disconnect(self, uid: int, type: str, queue: asyncio.Queue):
    """A client disconnects, remove their queue."""
    if uid in self.active_connections and type in self.active_connections[uid]:
      # Only delete if the queue being disconnected is the currently active one
      if self.active_connections[uid][type] is queue:
        del self.active_connections[uid][type]
        if not self.active_connections[uid]:
          del self.active_connections[uid]
    logger.info(f"User {uid} with type '{type}' disconnected.")

  async def send_message(self, uid: int, type: str, message: str):
    """Send a message to a specific user and type."""
    if uid in self.active_connections and type in self.active_connections[uid]:
      logger.info(f"Queueing SSE message for uid={uid}, type={type}: {message}")
      await self.active_connections[uid][type].put(message)

  async def send_event(self, uid: int, type: str, event: str, data: dict):
    """Send a custom event message to a specific user and type."""
    if uid in self.active_connections and type in self.active_connections[uid]:
      payload = f"event: {event}\ndata: {json.dumps(data)}\n\n"
      logger.info(f"Queueing SSE event for uid={uid}, type={type}: {payload}")
      await self.active_connections[uid][type].put(payload)

  async def send_data(self, uid: int, type: str, data: dict):
    """Sends data to a specific user and type."""
    if uid in self.active_connections and type in self.active_connections[uid]:
      payload = f"data: {json.dumps(data)}\n\n"
      logger.info(f"Queueing SSE data for uid={uid}, type={type}: {payload}")
      await self.active_connections[uid][type].put(payload)

  async def shutdown(self):
    """Signal all active connections to terminate."""
    logger.info("Shutting down SSE manager, signaling all clients to disconnect.")
    for uid in list(self.active_connections.keys()):
      for type, queue in list(self.active_connections[uid].items()):
        await queue.put(None) # Sentinel value to signal shutdown

# Create a single instance of the manager to be used by the application
manager = ConnectionManager()

async def make_sse_task_queue(request: Request, uid: int, type: str):
  """Yields server-sent events for a specific user and type."""
  queue = await manager.connect(uid, type)
  try:
    while True:
      message = await queue.get()

      if message is None: # Shutdown signal
        break

      if await request.is_disconnected():
        break
          
      logger.info(f"Yielding SSE message to uid={uid}, type={type}: {message}")
      yield f"{message}\n\n"
  except asyncio.CancelledError:
    logger.info(f"Event generation for user {uid} with type '{type}' cancelled.")
  finally:
    manager.disconnect(uid, type, queue)
    logger.info(f"Stopped event generation for user {uid} with type '{type}'")