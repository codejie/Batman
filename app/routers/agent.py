"""
Agent API Router - Handles agent chat requests via API.
"""
from fastapi import APIRouter, Depends, HTTPException
import os

from app.routers.common import RequestModel, ResponseModel, verify_token
from app.services.task_manager import taskManager
from app.services.tasks.agent_sse_task import AgentSseTask
from app.services.agent import AgentConfig
from app.logger import logger
import json

router: APIRouter = APIRouter(
    prefix="/agent",
    tags=["Agent"],
    dependencies=[Depends(verify_token)]
)

# Load agent config at startup
_agent_config = None

def _load_agent_config():
    """Load agent configuration from file (singleton)."""
    global _agent_config
    if _agent_config is None:
        config_path = os.getenv('AGENT_CONFIG_PATH', 'app/services/agent/data_agent_config.json')  # Default to 'app/services/agent example_config.json')
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            _agent_config = AgentConfig.from_dict(config_data)
            logger.info(f"[Agent] Config loaded from {config_path}")
        except Exception as e:
            logger.error(f"[Agent] Failed to load config from {config_path}: {e}")
            raise
    return _agent_config


class ChatRequest(RequestModel):
    """Request model for agent chat."""
    message: str
    use_thinking: bool = False


class ChatResponse(ResponseModel):
    """Response model for agent chat submission."""
    result: int  # 0 for success, 1 if task already running


@router.post('/chat', response_model=ChatResponse)
async def chat_with_agent(
    request: ChatRequest,
    uid: int = Depends(verify_token)
):
    """
    Submit a chat request to the agent.
    Response will be streamed via SSE at /sse/agent endpoint.
    
    Uses static configuration loaded from AGENT_CONFIG_PATH environment variable
    or defaults to 'app/services/agent/example_config.json'.
    
    Args:
        request: Chat request with message and thinking preference
        uid: User ID (from token)
    
    Returns:
        ChatResponse with result status (0=success, 1=task already running)
    """
    try:
        # Load agent config (cached)
        agent_config = _load_agent_config()
        
        # Create a unique task name based on user ID and timestamp
        task_name = f"{AgentSseTask.NAME}_{uid}_{AgentSseTask.TYPE}"
        
        # Check if a task for this user is already running
        if taskManager.get_instance(task_name) is None:
            # Add the agent task to task manager
            taskManager.add_task(
                AgentSseTask,
                name=task_name,
                uid=uid,
                agent_config=agent_config,
                user_message=request.message,
                use_thinking=request.use_thinking
            )
            logger.info(f"[Agent] Chat task started for user {uid}: {request.message[:100]}")
            return ChatResponse(result=0)
        else:
            logger.warning(f"[Agent] Task already running for user {uid}")
            return ChatResponse(result=1)
    
    except Exception as e:
        logger.error(f"[Agent] Error submitting chat: {e}")
        raise HTTPException(status_code=500, detail=f"Error submitting chat: {str(e)}")



