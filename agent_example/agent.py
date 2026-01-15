import os
import json
from typing import Optional, Union, Dict, Any, List
from pathlib import Path
from openai import OpenAI
from .config import AgentConfig
from .exceptions import AgentError, ToolError
from deepseek_framework.components.tools import ToolInstance
from deepseek_framework.components.prompts import PromptTemplate
from deepseek_framework.components.memory import Memory, WindowBufferMemory
from deepseek_framework.components.parsers import OutputParser, JsonOutputParser

class Agent:
    def __init__(self, config_path: Optional[Union[str, Path]] = None, config: Optional[Dict[str, Any]] = None, api_key: Optional[str] = None):
        """
        Initialize the agent from a YAML file or dictionary.
        
        Args:
            config_path: Path to .yaml file
            config: Direct dictionary configuration
            api_key: DeepSeek API key (defaults to DEEPSEEK_API_KEY env var)
        """
        if config_path:
            self.config = AgentConfig.from_yaml(config_path)
        elif config:
            self.config = AgentConfig.from_dict(config)
        else:
            raise AgentError("Must provide either config_path or config")

        # API Client
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise AgentError("DeepSeek API key not found. Set DEEPSEEK_API_KEY or pass api_key.")
            
        self.client = OpenAI(api_key=self.api_key, base_url="https://api.deepseek.com")
        # self.client = OpenAI(api_key=self.api_key, base_url="http://localhost:11434")

        # Runtime state
        self.tools: Dict[str, ToolInstance] = {}
        self.system_prompt: Optional[PromptTemplate] = None
        self.memory: Optional[Memory] = None
        self.output_parser: Optional[OutputParser] = None
        
        # Initialization
        self._initialize_components()

    def _initialize_components(self):
        """Initialize components based on config."""
        # Load tools
        for tool_config in self.config.tools:
            tool = ToolInstance.from_config(tool_config)
            self.register_tool(tool)
            
        # Load system prompt
        if self.config.system_prompt:
            self.system_prompt = PromptTemplate(self.config.system_prompt)
            
        # Load memory
        if self.config.memory:
            if self.config.memory.type == "window_buffer":
                self.memory = WindowBufferMemory(self.config.memory)
            else:
                self.memory = WindowBufferMemory(self.config.memory)
                
        # Load output parser
        if self.config.output_parser:
            if self.config.output_parser.type == "json":
                self.output_parser = JsonOutputParser(self.config.output_parser)

    def register_tool(self, tool: ToolInstance):
        """Register a tool instance."""
        self.tools[tool.name] = tool

    def get_tool_schemas(self) -> List[Dict[str, Any]]:
        """Get JSON schemas for all registered tools."""
        return [tool.to_schema() for tool in self.tools.values()]

    def render_system_prompt(self, context: Optional[Dict[str, Any]] = None) -> str:
        """Render the system prompt with context and parser instructions."""
        content = ""
        if self.system_prompt:
            content = self.system_prompt.render(**(context or {}))
            
        if self.output_parser:
            content += self.output_parser.get_instructions()
            
        return content

    def run(self, input_text: str, context: Optional[Dict[str, Any]] = None) -> Any:
        """
        Execute a turn of conversation, including tool execution loop.
        """
        # 1. Add user message to memory
        if self.memory:
            self.memory.add_message({"role": "user", "content": input_text})
            
        # 2. Construct initial messages for API
        messages = []
        system_content = self.render_system_prompt(context)
        if system_content:
            messages.append({"role": "system", "content": system_content})
            
        if self.memory:
            messages.extend(self.memory.get_history())
        else:
            messages.append({"role": "user", "content": input_text})
            
        # 3. Execution Loop (Handle tool calls)
        while True:
            response = self.chat(messages)
            message = response.choices[0].message
            
            # Output thinking content if available
            if hasattr(message, 'thinking') and message.thinking:
                print("\n" + "="*50)
                print("💭 THINKING PROCESS:")
                print("="*50)
                print(message.thinking)
                print("="*50 + "\n")
            
            if not message.tool_calls:
                # Terminal message from assistant
                content = message.content
                if content:
                    print("\n" + "="*50)
                    print("📝 RESPONSE:")
                    print("="*50)
                    print(content)
                    print("="*50 + "\n")
                
                if self.memory:
                    self.memory.add_message({"role": "assistant", "content": content})
                
                if self.output_parser:
                    return self.output_parser.parse(content)
                return content
            
            # Handle Tool Calls
            messages.append(message)
            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)
                
                print("\n" + "="*50)
                print(f"🔧 TOOL CALL: {tool_name}")
                print("="*50)
                print(f"Arguments: {json.dumps(tool_args, indent=2)}")
                
                if tool_name not in self.tools:
                    result = f"Error: Tool '{tool_name}' not found."
                else:
                    try:
                        result = self.tools[tool_name].execute(**tool_args)
                    except Exception as e:
                        result = f"Error executing tool: {e}"
                
                print(f"Result: {result}")
                print("="*50 + "\n")
                
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                })

    def chat(self, messages: List[Dict[str, Any]]) -> Any:
        """
        Low-level chat interface calling DeepSeek via OpenAI SDK.
        """
        tools = self.get_tool_schemas()
        kwargs = {
            "model": self.config.model,
            "messages": messages,
        }
        
        # Add thinking mode if enabled
        if self.config.thinking == "enabled":
            kwargs["extra_body"] = {
                "thinking": {
                    "type": "enabled"
                }
            }
        
        if tools:
            kwargs["tools"] = tools
            
        try:
            return self.client.chat.completions.create(**kwargs)
        except Exception as e:
            raise AgentError(f"API call failed: {e}")
