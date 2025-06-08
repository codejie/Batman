from fastapi import FastAPI, status #, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.routers import register_routers
from app.logger import logger
from app.exception import AppException
from app.database import dbEngine
from app.services import start_tasks, shutdown_tasks

@asynccontextmanager
async def lifespan(app: FastAPI):
  logger.info("Application is starting up...")
  dbEngine.start()
  start_tasks()
  yield
  logger.info("Application is shutting down...")
  shutdown_tasks()
  dbEngine.shutdown()

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
