"""
Agent implementation with DeepSeek model integration.
"""
import asyncio
import json
from typing import Optional, List, Dict, Any, AsyncGenerator, Tuple
from dataclasses import dataclass
from datetime import datetime
import httpx

from .config import AgentConfig
from app.logger import logger


@dataclass
class Message:
    """A message in the conversation."""
    role: str  # "user", "assistant", "system"
    content: str
    timestamp: Optional[datetime] = None
    thinking: Optional[str] = None


class Agent:
    """
    Agent class that integrates with DeepSeek model for chat functionality.
    Supports conversation memory, tools, and SSE output.
    """
    
    def __init__(self, config: AgentConfig):
        """
        Initialize the Agent with configuration.
        
        Args:
            config: AgentConfig object containing model, prompt, and memory settings
        """
        self.config = config
        self.conversation_history: List[Message] = []
        self.system_message = Message(
            role="system",
            content=config.system_prompt,
            timestamp=datetime.now()
        )
        self.deepseek_api_key = self._get_api_key()
        self.base_url = "https://api.deepseek.com"
        self.model = config.model
        
    def _get_api_key(self) -> str:
        """Get DeepSeek API key from environment."""
        import os
        api_key = os.getenv('DEEPSEEK_API_KEY')
        if not api_key:
            raise ValueError("DEEPSEEK_API_KEY environment variable not set")
        return api_key
    
    def add_message(self, role: str, content: str, thinking: Optional[str] = None) -> None:
        """
        Add a message to conversation history.
        
        Args:
            role: Message role ("user", "assistant")
            content: Message content
            thinking: Optional thinking content for assistant
        """
        message = Message(
            role=role,
            content=content,
            timestamp=datetime.now(),
            thinking=thinking
        )
        self.conversation_history.append(message)
        self._trim_history()
    
    def _trim_history(self) -> None:
        """Trim conversation history based on memory config."""
        if not self.config.memory.enabled:
            return
        
        max_history = self.config.memory.max_history
        if len(self.conversation_history) > max_history:
            # Keep the most recent messages
            self.conversation_history = self.conversation_history[-max_history:]
    
    def _get_messages_for_api(self) -> List[Dict[str, str]]:
        """
        Get messages formatted for DeepSeek API call.
        
        Returns:
            List of message dicts with role and content
        """
        messages = []
        
        # Add system message
        messages.append({
            "role": self.system_message.role,
            "content": self.system_message.content
        })
        
        # Add conversation history
        for msg in self.conversation_history:
            messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        return messages
    
    async def chat(
        self,
        user_message: str,
        use_thinking: bool = False
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Send a chat message and stream the response.
        
        Args:
            user_message: The user's message
            use_thinking: Whether to use thinking capability
            
        Yields:
            Dict with response content, thinking, or metadata
        """
        # Add user message to history
        self.add_message("user", user_message)
        
        # Prepare API call
        messages = self._get_messages_for_api()
        
        headers = {
            "Authorization": f"Bearer {self.deepseek_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": self.config.temperature,
            "top_p": self.config.top_p,
            "stream": True
        }
        
        # Add thinking if requested
        if use_thinking:
            # payload["thinking"] = {
            #     "type": "enabled",
            #     "budget_tokens": 1024
            # }
            payload["extra_body"] = {
                "thinking": {
                    "type": "enabled"
                }
            }        
        if self.config.max_tokens:
            payload["max_tokens"] = self.config.max_tokens
        
        if self.config.top_k > 0:
            payload["top_k"] = self.config.top_k
        
        try:
            async with httpx.AsyncClient(timeout=300.0) as client:
                async with client.stream(
                    "POST",
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status_code != 200:
                        error_text = await response.aread()
                        raise Exception(f"DeepSeek API error: {response.status_code} - {error_text.decode()}")
                    
                    full_content = ""
                    full_thinking = ""
                    
                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            data_str = line[6:]
                            if data_str == "[DONE]":
                                continue
                            
                            try:
                                chunk = json.loads(data_str)
                                
                                # Process choices
                                if "choices" in chunk and len(chunk["choices"]) > 0:
                                    choice = chunk["choices"][0]
                                    delta = choice.get("delta", {})
                                    
                                    # Handle thinking content
                                    if "thinking" in delta:
                                        thinking_text = delta["thinking"]
                                        full_thinking += thinking_text
                                        yield {
                                            "type": "thinking",
                                            "content": thinking_text
                                        }
                                    
                                    # Handle regular content
                                    if "content" in delta:
                                        content_text = delta["content"]
                                        full_content += content_text
                                        yield {
                                            "type": "content",
                                            "content": content_text
                                        }
                                    
                                    # Check for finish reason
                                    finish_reason = choice.get("finish_reason")
                                    if finish_reason:
                                        yield {
                                            "type": "finish",
                                            "reason": finish_reason
                                        }
                            
                            except json.JSONDecodeError:
                                logger.warning(f"Failed to parse JSON: {data_str}")
                                continue
                    
                    # Add assistant message to history
                    if full_content:
                        self.add_message(
                            "assistant",
                            full_content,
                            thinking=full_thinking if full_thinking else None
                        )
        
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            yield {
                "type": "error",
                "content": str(e)
            }
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """
        Get the conversation history.
        
        Returns:
            List of messages with role, content, and timestamps
        """
        history = []
        for msg in self.conversation_history:
            msg_dict = {
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat() if msg.timestamp else None
            }
            if msg.thinking:
                msg_dict["thinking"] = msg.thinking
            history.append(msg_dict)
        return history
    
    def clear_history(self) -> None:
        """Clear the conversation history."""
        self.conversation_history = []
    
    def get_config(self) -> Dict[str, Any]:
        """Get the agent configuration."""
        return self.config.to_dict()
