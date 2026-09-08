from google.adk.agents.llm_agent import Agent
# from google.adk.tools import google_search
# Using this will cause 429 RESOURCE_EXHAUSTED error
from google.adk.code_executors import BuiltInCodeExecutor
from google.genai import types
import requests

def get_weather(city: str) -> dict:
    """
    Retrieves the weather for a given city

    Args:
        city: The name of the city to retrieve weather for
    """
    url = f'https://wttr.in/{city}?format=j1'
    response = requests.get(url)
    
    return response.json()

def write_to_file(filename: str, content: str) -> dict:
    """
    Writes the given content to a file.

    Args:
        filename: The name of the file to write to
        content: The text content to write into the file
    """
    try:
        with open(filename, 'w') as f:
            f.write(content)
        return {"status": "success", "message": f"Content written to {filename}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

root_agent = Agent(
    model='gemini-3.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
    tools=[get_weather, write_to_file],
    code_executor=BuiltInCodeExecutor(),
    generate_content_config=types.GenerateContentConfig(
        tool_config={"include_server_side_tool_invocations": True}
    )
)
