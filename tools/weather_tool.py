from datetime import datetime
from llama_index.core.tools import FunctionTool, ToolMetadata

# This is a mock weather API - in a real application, you would use an actual weather API
def get_weather(location: str, date: str = None) -> str:
    """Get weather information for a location and date."""
    # Simple mock implementation for demonstration purposes
    weather_data = {
        "new york": {"temperature": 72, "condition": "sunny"},
        "london": {"temperature": 65, "condition": "cloudy"},
        "tokyo": {"temperature": 80, "condition": "partly cloudy"},
        "sydney": {"temperature": 85, "condition": "clear"},
        "paris": {"temperature": 70, "condition": "rainy"},
    }
    
    # Default to today if no date is provided
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    # Convert location to lowercase for case-insensitive matching
    location = location.lower()
    
    if location in weather_data:
        temp = weather_data[location]["temperature"]
        condition = weather_data[location]["condition"]
        return f"The weather in {location.title()} on {date} is {condition} with a temperature of {temp}°F."
    else:
        available_locations = ", ".join(city.title() for city in weather_data.keys())
        return f"Weather data for {location} is not available. Available locations: {available_locations}."

def get_weather_tool():
    """Create and return a weather FunctionTool."""
    return FunctionTool.from_defaults(
        fn=get_weather,
        name="weather_tool",
        description="Get weather information for a specific location and optional date (format: YYYY-MM-DD). If no date is provided, current weather is returned."
    )