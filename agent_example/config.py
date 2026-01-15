from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, Field
import yaml
from pathlib import Path
from .exceptions import ConfigurationError

class PromptConfig(BaseModel):
    template: str
    defaults: Dict[str, Any] = Field(default_factory=dict)
    
    @property
    def variables(self) -> List[str]:
        # Basic variable extraction, can be improved later or via Jinja inspection
        import re
        return re.findall(r"{{(.*?)}}", self.template)

class ToolConfig(BaseModel):
    name: str
    module: str
    function: str
    description: Optional[str] = None

class MemoryConfig(BaseModel):
    type: str = "window_buffer"
    size: int = 10
    storage: str = "in_memory"

class ParserConfig(BaseModel):
    type: str
    schema_model: Optional[str] = None

class AgentConfig(BaseModel):
    name: str
    model: str = "deepseek-chat"
    system_prompt: Optional[PromptConfig] = None
    memory: Optional[MemoryConfig] = None
    tools: List[ToolConfig] = Field(default_factory=list)
    output_parser: Optional[ParserConfig] = None
    thinking: str = "disabled"  # "enabled" or "disabled"

    @classmethod
    def from_yaml(cls, path: Union[str, Path]) -> 'AgentConfig':
        """Load configuration from a YAML file."""
        path = Path(path)
        if not path.exists():
            raise ConfigurationError(f"Config file not found: {path}")
        
        try:
            with open(path, 'r') as f:
                data = yaml.safe_load(f)
            
            if not data or 'agent' not in data:
                raise ConfigurationError("Invalid config: missing 'agent' root key")
            
            return cls(**data['agent'])
        except yaml.YAMLError as e:
            raise ConfigurationError(f"Failed to parse YAML: {e}")
        except Exception as e:
            raise ConfigurationError(f"Failed to load config: {e}")

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AgentConfig':
        """Load configuration from a dictionary."""
        if 'agent' in data:
            return cls(**data['agent'])
        return cls(**data)
