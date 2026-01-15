"""
Mock functions for Agent tools.
"""
import json

def get_current_weather(location: str, unit: str = "celsius"):
    """Get the current weather in a given location"""
    if "beijing" in location.lower():
        return json.dumps({"location": "Beijing", "temperature": "10", "unit": unit})
    elif "san francisco" in location.lower():
        return json.dumps({"location": "San Francisco", "temperature": "72", "unit": unit})
    else:
        return json.dumps({"location": location, "temperature": "unknown"})
