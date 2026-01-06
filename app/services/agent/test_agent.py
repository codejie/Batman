#!/usr/bin/env python3
"""
Quick test script for DeepSeek Agent API.
Usage: python test_agent.py
"""

import requests
import json
import time
import sys
from typing import Optional

# Configuration
API_BASE_URL = "http://localhost:8000"
UID = 123  # Example user ID
TOKEN = "your-bearer-token"  # Replace with actual token

# Example Agent Configuration
AGENT_CONFIG = {
    "name": "Code Assistant",
    "system_prompt": "You are an expert Python programmer. Help users with coding problems and provide clear explanations.",
    "model": "deepseek-chat",
    "temperature": 0.5,
    "top_p": 1.0,
    "top_k": 0,
    "max_tokens": 1000,
    "tools": [
        {
            "name": "search_documentation",
            "description": "Search Python documentation for specific topics",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    }
                },
                "required": ["query"]
            },
            "enabled": True
        }
    ],
    "memory": {
        "max_history": 10,
        "memory_type": "message_window",
        "enabled": True
    }
}

class AgentTestClient:
    """Simple client for testing Agent API."""
    
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    
    def submit_chat(self, uid: int, config: dict, message: str, use_thinking: bool = False) -> Optional[dict]:
        """Submit a chat request to the Agent."""
        url = f"{self.base_url}/agent/chat"
        payload = {
            "config": config,
            "message": message,
            "use_thinking": use_thinking
        }
        
        try:
            response = requests.post(url, json=payload, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error submitting chat: {e}")
            return None
    
    def listen_sse(self, uid: int, timeout: int = 60):
        """Listen for SSE responses from the Agent."""
        url = f"{self.base_url}/sse/agent"
        params = {"uid": uid}
        
        try:
            print(f"\n[SSE] Connecting to {url}...")
            with requests.get(url, params=params, headers=self.headers, stream=True, timeout=timeout) as response:
                response.raise_for_status()
                print("[SSE] Connected!")
                
                for line in response.iter_lines():
                    if not line:
                        continue
                    
                    line = line.decode('utf-8') if isinstance(line, bytes) else line
                    
                    # Parse SSE format
                    if line.startswith('event: '):
                        event = line[7:]
                        print(f"\n>>> Event: {event}")
                    
                    elif line.startswith('data: '):
                        try:
                            data = json.loads(line[6:])
                            
                            if isinstance(data, dict):
                                if data.get("type") == "thinking":
                                    print(f"[Thinking] {data.get('content', '')}", end="", flush=True)
                                elif data.get("type") == "content":
                                    print(f"{data.get('content', '')}", end="", flush=True)
                                elif data.get("type") == "finish":
                                    print(f"\n[Finish] Reason: {data.get('reason')}")
                                elif data.get("action") == "finish":
                                    print("\n[Done] Task completed")
                                    break
                                elif data.get("action") == "error":
                                    print(f"\n[Error] {data.get('message')}")
                                elif data.get("action") == "log":
                                    print(f"\n[Log] {data.get('message')}")
                        except json.JSONDecodeError:
                            print(f"[Raw] {line}")
        
        except requests.exceptions.RequestException as e:
            print(f"[Error] SSE Connection failed: {e}")

def test_basic_chat():
    """Test basic chat without thinking."""
    print("\n=== Test 1: Basic Chat (No Thinking) ===")
    client = AgentTestClient(API_BASE_URL, TOKEN)
    
    # Submit chat request
    print(f"Submitting chat request with message: 'Write a simple Python function to calculate factorial'")
    result = client.submit_chat(UID, AGENT_CONFIG, "Write a simple Python function to calculate factorial", use_thinking=False)
    
    if result:
        print(f"Response: {json.dumps(result, ensure_ascii=False, indent=2)}")
        if result.get("result") == 0:
            print("\n[Info] Connecting to SSE to receive response...")
            client.listen_sse(UID)
        else:
            print("[Info] Task already running")
    else:
        print("[Error] Failed to submit chat")

def test_chat_with_thinking():
    """Test chat with thinking enabled."""
    print("\n=== Test 2: Chat with Thinking ===")
    client = AgentTestClient(API_BASE_URL, TOKEN)
    
    # Submit chat request with thinking
    print(f"Submitting chat request with thinking enabled")
    result = client.submit_chat(
        UID,
        AGENT_CONFIG,
        "What are the differences between list and tuple in Python? Explain in detail.",
        use_thinking=True
    )
    
    if result:
        print(f"Response: {json.dumps(result, ensure_ascii=False, indent=2)}")
        if result.get("result") == 0:
            print("\n[Info] Connecting to SSE to receive response...")
            client.listen_sse(UID)
        else:
            print("[Info] Task already running")
    else:
        print("[Error] Failed to submit chat")

def test_save_and_load_config():
    """Test saving and loading configuration."""
    print("\n=== Test 3: Save and Load Config ===")
    client = AgentTestClient(API_BASE_URL, TOKEN)
    
    # Save config
    config_path = "/tmp/test_agent_config.json"
    print(f"Saving config to {config_path}...")
    
    payload = {
        "config": AGENT_CONFIG,
        "config_path": config_path
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/agent/save_config",
            json=payload,
            headers=client.headers,
            timeout=10
        )
        response.raise_for_status()
        print(f"Save response: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    except Exception as e:
        print(f"Error saving config: {e}")

def main():
    """Run tests."""
    print("DeepSeek Agent API Test")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        test_type = sys.argv[1]
        if test_type == "basic":
            test_basic_chat()
        elif test_type == "thinking":
            test_chat_with_thinking()
        elif test_type == "config":
            test_save_and_load_config()
        else:
            print(f"Unknown test type: {test_type}")
            print("Available tests: basic, thinking, config")
    else:
        # Run a quick test
        test_basic_chat()
        
        # Wait a bit and try another test
        print("\n\nWaiting 5 seconds before next test...")
        time.sleep(5)
        
        test_chat_with_thinking()

if __name__ == "__main__":
    main()
