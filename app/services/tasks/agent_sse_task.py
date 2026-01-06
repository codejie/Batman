"""
Agent SSE Task - Handles agent chat requests and streams responses via SSE.
Similar to CalcSseTask but for agent-based chat functionality.
"""
import asyncio
import json
from typing import Optional
from dataclasses import asdict

from app.services.task_manager import Task
from app.services.sse_manager import manager as sse_manager
from app.services.agent import Agent, AgentConfig
from app.logger import logger


class AgentSseTask(Task):
    """
    Task for handling agent chat requests with SSE output.
    Manages the agent lifecycle and streams responses back to the user.
    """
    
    NAME = "agent_sse_task"
    TYPE = "agent_chat"
    
    def __init__(self, name=None, **kwargs):
        """
        Initialize the Agent SSE Task.
        
        Args:
            name: Task name
            uid: User ID
            agent_config: AgentConfig object
            user_message: The user's chat message
            use_thinking: Whether to use thinking capability
        """
        super().__init__(name, **kwargs)
        self.uid = kwargs.get('uid')
        self.agent_config = kwargs.get('agent_config')
        self.user_message = kwargs.get('user_message')
        self.use_thinking = kwargs.get('use_thinking', False)
        
        if self.uid is None or self.agent_config is None or self.user_message is None:
            raise ValueError("uid, agent_config, and user_message must be provided for AgentSseTask")
        
        self.agent: Optional[Agent] = None
    
    async def _send_data(self, data: dict):
        """
        Send data to the user via SSE.
        
        Args:
            data: Dictionary to send to user
        """
        await sse_manager.send_data(self.uid, self.TYPE, data=data)
    
    async def _send_event(self, event: str, data: dict):
        """
        Send a custom event to the user via SSE.
        
        Args:
            event: Event name
            data: Event data
        """
        await sse_manager.send_event(self.uid, self.TYPE, event=event, data=data)
    
    async def run(self, exit_event: asyncio.Event):
        """
        Main task logic for handling agent chat and SSE streaming.
        
        Args:
            exit_event: Event to signal task cancellation
        """
        await asyncio.sleep(0.5)  # Short delay to ensure setup is complete
        await self._send_event(event="action", data={"action": "start"})
        
        try:
            # Initialize agent with provided configuration
            self.agent = Agent(self.agent_config)
            
            await self._send_event(
                event="action",
                data={"action": "log", "message": f"[AgentTask] Agent initialized with model: {self.agent_config.model}"}
            )
            
            # Stream chat response
            message_parts = []
            thinking_parts = []
            
            async for response in self.agent.chat(self.user_message, use_thinking=self.use_thinking):
                if exit_event.is_set():
                    logger.info(f"[AgentTask] Task cancelled.")
                    break
                
                response_type = response.get("type")
                content = response.get("content", "")
                
                if response_type == "thinking":
                    thinking_parts.append(content)
                    # Send thinking chunks as they arrive
                    await self._send_data({
                        "type": "thinking",
                        "content": content
                    })
                
                elif response_type == "content":
                    message_parts.append(content)
                    # Send content chunks as they arrive
                    await self._send_data({
                        "type": "content",
                        "content": content
                    })
                
                elif response_type == "finish":
                    # Send finish signal with reason
                    await self._send_data({
                        "type": "finish",
                        "reason": response.get("reason")
                    })
                
                elif response_type == "error":
                    # Send error message
                    await self._send_event(
                        event="action",
                        data={"action": "error", "message": content}
                    )
                
                await asyncio.sleep(0.01)  # Small delay to allow other tasks to run
        
        except asyncio.CancelledError:
            logger.info(f"Task '{self.name}' was stopped (cancelled).")
            await self._send_event(
                event="action",
                data={"action": "log", "message": "[AgentTask] Task was cancelled."}
            )
        
        except Exception as e:
            logger.error(f"[AgentTask] Error: {e}")
            await self._send_event(
                event="action",
                data={"action": "error", "message": f"[AgentTask] Error: {e}"}
            )
        
        finally:
            logger.info(f"[AgentTask] Finished.")
            await self._send_event(event="action", data={"action": "finish"})
