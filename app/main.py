from fastapi import FastAPI, status #, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.exception import AppException
# from app.logger import logger

app = FastAPI(title='Batman API', version='v0.3')

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
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

