import asyncio
import json
from typing import Dict, List
from fastapi import Request

from app.services.task_manager import taskManager

class ConnectionManager:
  def __init__(self):
    # Store active connections as: {uid: {type: [Queue]}}
    self.active_connections: Dict[int, Dict[str, List[asyncio.Queue]]] = {}

  async def connect(self, uid: int, type: str) -> asyncio.Queue:
    """A new client connects, create a new queue for them based on user and type."""
    if uid not in self.active_connections:
      self.active_connections[uid] = {}
    
    if type not in self.active_connections[uid]:
      self.active_connections[uid][type] = []
    
    queue = asyncio.Queue()
    self.active_connections[uid][type].append(queue)
    print(f"User {uid} connected with type '{type}'. Total connections for type: {len(self.active_connections[uid][type])}")
    return queue

  def disconnect(self, uid: int, type: str, queue: asyncio.Queue):
    """A client disconnects, remove their queue."""
    if uid in self.active_connections and type in self.active_connections[uid]:
      self.active_connections[uid][type].remove(queue)
      if not self.active_connections[uid][type]:
        del self.active_connections[uid][type]
      if not self.active_connections[uid]:
        del self.active_connections[uid]
    print(f"User {uid} with type '{type}' disconnected.")

  async def send_message(self, uid: int, type: str, message: str):
    """Send a message to a specific user and type."""
    if uid in self.active_connections and type in self.active_connections[uid]:
      for queue in self.active_connections[uid][type]:
        await queue.put(message)

  async def send_data(self, uid: int, type: str, data: dict | None = None, code: int = 0, message: str | None = None):
    """Wraps data in a standard format and sends it to a specific user and type."""
    if uid in self.active_connections and type in self.active_connections[uid]:
      # Wrap the data in the standard format
      payload = {
          "code": code,
          "message": message,
          "type": type,
          "data": data
      }
      # Serialize to a JSON string
      message_str = json.dumps(payload)
      for queue in self.active_connections[uid][type]:
        await queue.put(message_str)

  async def shutdown(self):
    """Signal all active connections to terminate."""
    print("Shutting down SSE manager, signaling all clients to disconnect.")
    for uid in list(self.active_connections.keys()):
      for type in list(self.active_connections[uid].keys()):
        for queue in self.active_connections[uid][type]:
          await queue.put(None) # Sentinel value to signal shutdown

# Create a single instance of the manager to be used by the application
manager = ConnectionManager()

async def make_sse_task_queue(request: Request, uid: int, type: str):
  """Yields server-sent events for a specific user and type."""  
  # Start a background task to send messages to this user for this type
  # task_name = f"sse_{uid}_{type}"
  # if taskManager.get_instance(task_name) is None:
  #   if type == "calc_report":
  #     from app.services.tasks.calc_sse_task import CalcSseTask
  #     taskManager.add_task(CalcSseTask, name=task_name, uid=uid, cid=0)
  #   else:
  #     print(f"Unknown SSE type '{type}' for user {uid}, no task created.")
  #     return
  # else:
  #   print(f"SSE task '{task_name}' already exists for user {uid}.")
  #   return

  queue = await manager.connect(uid, type)
  try:
    while True:
      message = await queue.get()

      if message is None: # Shutdown signal
        break

      if await request.is_disconnected():
        break
          
      yield f"{message}"
  except asyncio.CancelledError:
    pass
  finally:
    manager.disconnect(uid, type, queue)
    print(f"Stopped event generation for user {uid} with type '{type}'")