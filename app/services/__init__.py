import asyncio
from app.services.task_spot_data import SpotDataFetchTask
from app.setting import TASK_SPOT_DATA_FETCH_ENABLED
from app.services.task_manager import taskManager
from app.services.sse_manager import manager as sse_manager
from app.services.task_spot_data import spotDataClientManagerTask

def start_tasks() -> None:
  taskManager.start()
  if TASK_SPOT_DATA_FETCH_ENABLED:
    spotTask = taskManager.add_task(task=SpotDataFetchTask)
    spotDataClientManagerTask.set_fetch_task(spotTask)
    taskManager.add_instance(spotDataClientManagerTask)


async def graceful_shutdown() -> None:
  """The main entry point for shutting down all services gracefully."""
  # First, signal SSE clients to disconnect. This is async.
  await sse_manager.shutdown()
  
  # Then, shut down the task manager. This is a blocking call.
  # Run the blocking call in a separate thread to avoid deadlocking the main event loop.
  loop = asyncio.get_running_loop()
  await loop.run_in_executor(None, taskManager.shutdown)