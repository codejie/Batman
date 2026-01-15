"""
Agent configuration module for managing prompts, tools, and memory settings.
"""
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any
import json


@dataclass
class ToolConfig:
    """Configuration for a single tool."""
    name: str
    description: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    enabled: bool = True
    module: Optional[str] = None


@dataclass
class MemoryConfig:
    """Configuration for agent memory."""
    max_history: int = 10  # Maximum number of messages to keep in history
    memory_type: str = "message_window"  # "message_window" or "summary"
    enabled: bool = True


@dataclass
class AgentConfig:
    """Main configuration for the Agent."""
    name: str
    system_prompt: str
    tools: List[ToolConfig] = field(default_factory=list)
    memory: MemoryConfig = field(default_factory=MemoryConfig)
    model: str = "deepseek-chat"
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    top_p: float = 1.0
    top_k: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return asdict(self)
    
    def to_json(self) -> str:
        """Convert config to JSON string."""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'AgentConfig':
        """Create AgentConfig from dictionary."""
        memory_data = data.pop('memory', {})
        memory = MemoryConfig(**memory_data) if memory_data else MemoryConfig()
        
        tools_data = data.pop('tools', [])
        tools = [ToolConfig(**tool) for tool in tools_data]
        
        return AgentConfig(
            tools=tools,
            memory=memory,
            **data
        )


def load_agent_config_from_file(config_path: str) -> AgentConfig:
    """Load agent configuration from a JSON file."""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return AgentConfig.from_dict(data)
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file not found: {config_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON in config file: {config_path}")


def save_agent_config_to_file(config: AgentConfig, config_path: str) -> None:
    """Save agent configuration to a JSON file."""
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(config.to_json())
