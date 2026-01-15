"""
Agent implementation with DeepSeek model integration.
"""
# import asyncio
import json
from typing import Optional, List, Dict, Any, AsyncGenerator, Tuple
from dataclasses import dataclass
from datetime import datetime
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessage, ChatCompletionMessageToolCall

from .config import AgentConfig
from app.logger import logger
import importlib
# from . import local_tools


@dataclass
class Message:
    """A message in the conversation."""
    role: str  # "user", "assistant", "system"
    content: str
    timestamp: Optional[datetime] = None
    thinking: Optional[str] = None
    tool_calls: Optional[List[ChatCompletionMessageToolCall]] = None


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
        
        # Initialize OpenAI client for DeepSeek
        self.client = AsyncOpenAI(
            api_key=self.deepseek_api_key,
            base_url=self.base_url
        )
        
        self.tools: Dict[str, callable] = {}
        self._load_tools()
        
    def _load_tools(self):
        """Load tools from the config and map them to functions in modules."""
        for tool_config in self.config.tools:
            if tool_config.enabled:
                try:
                    # Default to local_tools if module is not specified
                    module_name = tool_config.module if tool_config.module else 'app.services.agent.local_tools'
                    module = importlib.import_module(module_name)
                    
                    tool_func = getattr(module, tool_config.name, None)
                    
                    if callable(tool_func):
                        self.tools[tool_config.name] = tool_func
                    else:
                        logger.warning(f"Tool '{tool_config.name}' not found or not callable in module '{module_name}'.")

                except ImportError:
                    logger.error(f"Failed to import module '{tool_config.module}' for tool '{tool_config.name}'.")
                except Exception as e:
                    logger.error(f"Error loading tool '{tool_config.name}': {e}")
    
    def _get_tool_schemas(self) -> List[Dict[str, Any]]:
        """Get JSON schemas for all registered tools from config."""
        schemas = []
        for tool_config in self.config.tools:
            if tool_config.enabled and tool_config.name in self.tools:
                schemas.append({
                    "type": "function",
                    "function": {
                        "name": tool_config.name,
                        "description": tool_config.description,
                        "parameters": tool_config.parameters,
                    }
                })
        return schemas

    def _get_api_key(self) -> str:
        """Get DeepSeek API key from environment."""
        import os
        api_key = os.getenv('DEEPSEEK_API_KEY')
        if not api_key:
            raise ValueError("DEEPSEEK_API_KEY environment variable not set")
        return api_key
    
    def add_message(self, role: str, content: str, thinking: Optional[str] = None, tool_calls: Optional[List[ChatCompletionMessageToolCall]] = None) -> None:
        """
        Add a message to conversation history.
        
        Args:
            role: Message role ("user", "assistant")
            content: Message content
            thinking: Optional thinking content for assistant
        """
        message = Message(
            role=role,
            content=str(content),
            timestamp=datetime.now(),
            thinking=thinking,
            tool_calls=tool_calls
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
    
    def _get_messages_for_api(self) -> List[Dict[str, Any]]:
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
            api_msg = {
                "role": msg.role,
                "content": msg.content
            }
            if msg.tool_calls:
                api_msg["tool_calls"] = [tc.model_dump() for tc in msg.tool_calls]
            messages.append(api_msg)

        return messages
    
    async def chat(
        self,
        user_message: str,
        use_thinking: bool = False
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Send a chat message and stream the response, handling tool calls.
        """
        self.add_message("user", user_message)
        
        messages = self._get_messages_for_api()

        while True:
            params = {
                "model": self.model,
                "messages": messages,
                "temperature": self.config.temperature,
                "top_p": self.config.top_p,
                "stream": True,
            }

            if self.config.max_tokens:
                params["max_tokens"] = self.config.max_tokens

            tools = self._get_tool_schemas()
            if tools:
                params["tools"] = tools
                params["tool_choice"] = "auto"
            
            try:
                stream = await self.client.chat.completions.create(**params)
                
                full_content = ""
                thinking_text = ""
                tool_calls: List[ChatCompletionMessageToolCall] = []
                tool_call_chunks = {}

                async for chunk in stream:
                    if not chunk.choices:
                        continue
                    
                    delta = chunk.choices[0].delta
                    finish_reason = chunk.choices[0].finish_reason

                    if delta.content:
                        full_content += delta.content
                        yield {"type": "content", "content": delta.content}

                    if delta.tool_calls:
                        for tool_call_chunk in delta.tool_calls:
                            index = tool_call_chunk.index
                            if index not in tool_call_chunks:
                                tool_call_chunks[index] = {
                                    "id": "", "type": "function", "function": {"name": "", "arguments": ""}
                                }
                            
                            chunk_dict = tool_call_chunks[index]
                            if tool_call_chunk.id:
                                chunk_dict["id"] += tool_call_chunk.id
                            if tool_call_chunk.function:
                                if tool_call_chunk.function.name:
                                    chunk_dict["function"]["name"] += tool_call_chunk.function.name
                                if tool_call_chunk.function.arguments:
                                    chunk_dict["function"]["arguments"] += tool_call_chunk.function.arguments

                    if finish_reason == "tool_calls":
                        tool_calls = [ChatCompletionMessageToolCall(**chunk) for chunk in tool_call_chunks.values()]
                        break 
                    
                    if finish_reason:
                        yield {"type": "finish", "reason": finish_reason}
                        break
                
                if tool_calls:
                    # Assistant message with tool calls
                    assistant_message = ChatCompletionMessage(role='assistant', content=full_content, tool_calls=tool_calls)
                    messages.append(assistant_message.model_dump(exclude_none=True))
                    self.add_message('assistant', content=full_content, tool_calls=tool_calls)
                    
                    for tool_call in tool_calls:
                        tool_name = tool_call.function.name
                        
                        yield {"type": "thinking", "content": f"Executing tool: {tool_name}..."}
                        
                        if tool_name not in self.tools:
                            error_msg = f"Tool '{tool_name}' not found."
                            tool_result = json.dumps({"error": error_msg})
                        else:
                            try:
                                tool_args = json.loads(tool_call.function.arguments)
                                tool_func = self.tools[tool_name]
                                tool_result = tool_func(**tool_args)
                            except Exception as e:
                                tool_result = json.dumps({"error": f"Error executing tool '{tool_name}': {e}"})

                        yield {"type": "thinking", "content": f"Tool Result: {tool_result}"}
                        
                        tool_message = {
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": tool_name,
                            "content": str(tool_result),
                        }
                        messages.append(tool_message)
                    continue
                else:
                    # No tool calls, conversation is finished
                    if full_content:
                        self.add_message("assistant", full_content)
                    break
            
            except Exception as e:
                logger.error(f"Error in chat: {e}")
                yield {"type": "error", "content": str(e)}
                break

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

