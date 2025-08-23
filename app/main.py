from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import asyncio
import signal
import os
from app.routers import register_routers
from app.logger import logger
from app.exception import AppException
from app.database import dbEngine
from app.services import start_tasks, graceful_shutdown

SHUTDOWN_EVENT = asyncio.Event()

def _signal_handler(*_):
    """Signal handler that triggers the shutdown event."""
    # It's generally unsafe to do anything complex in a signal handler.
    # Setting an asyncio event is safe.
    SHUTDOWN_EVENT.set()

async def main_shutdown_logic(app: FastAPI):
    """Coroutine that waits for the shutdown signal and then cleans up."""
    await SHUTDOWN_EVENT.wait()
    logger.info("Shutdown signal received, running cleanup...")
    await graceful_shutdown()
    dbEngine.shutdown()
    logger.info("Cleanup complete. Forcing exit.")
    os._exit(0)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application is starting up...")
    
    # Start background services
    dbEngine.start()
    start_tasks()
    
    # Register signal handlers to trigger a graceful shutdown
    signal.signal(signal.SIGINT, _signal_handler)
    signal.signal(signal.SIGTERM, _signal_handler)
    
    # Create a background task to listen for the shutdown event
    shutdown_task = asyncio.create_task(main_shutdown_logic(app))
    
    yield
    
    logger.info("Application shutdown sequence started.")
    if not SHUTDOWN_EVENT.is_set():
        SHUTDOWN_EVENT.set() # Ensure shutdown happens even if not triggered by signal
    try:
        await shutdown_task
    except asyncio.CancelledError:
        pass # This is expected during a forceful shutdown

app = FastAPI(title='Batman API', version='v0.3', lifespan=lifespan)

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
  expose_headers=["Content-Disposition"]  # Add this line
)

# @app.middleware("http")
# async def log_requests(request: Request, call_next):
#   logger = logger.getLogger("app")
#   logger.info(f"Request: {request.method} {request.url}")
#   response = await call_next(request)
#   logger.info(f"Response: {response.status_code}")
#   return response

@app.exception_handler(AppException)
async def app_exception_handler(request, exc):
  return JSONResponse(
    status_code=status.HTTP_200_OK,
    content={
      'code': exc.code,
      'message': exc.message
    }
  )

@app.get("/")
def read_root():
  return {"message": "Welcome to Batman Platform!"}

register_routers(app)