from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from app.routers.common import verify_token
from app.services.sse_manager import manager, make_sse_task_queue
from app.services.tasks.calc_sse_task import CalcSseTask

# The router
router = APIRouter(
    prefix="/sse",
    tags=["sse"]
)

@router.get("/calc_report")
async def calc_report(request: Request, uid: int = verify_token()):
    """
    Establishes an SSE connection for calculation reports.
    """
    return StreamingResponse(make_sse_task_queue(request, uid, type=CalcSseTask.TYPE), media_type="text/event-stream")

# Example of how to use the manager from another part of your app
# @router.post("/send/{uid}/{type}")
# async def send_message_to_user(uid: int, type: str, message: str):
#     """
#     An example endpoint to trigger sending a message to a specific user and type.
#     """
#     await manager.send_message(uid, type, f"A message for you: {message}")
#     return {"status": "message sent"}