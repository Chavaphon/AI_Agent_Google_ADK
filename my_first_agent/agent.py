from google.adk.agents.llm_agent import Agent
# from google.adk.tools import google_search
# Using this will cause 429 RESOURCE_EXHAUSTED error
from google.adk.code_executors import BuiltInCodeExecutor
from google.genai import types

def get_weather(location: str) -> dict:
    """
    Retrieves the weather for a given location

    Args:
        location: The name of the city to retrieve weather for
    """
    return {"location": location, "weather": "Sunny"}

root_agent = Agent(
    model='gemini-3.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
    tools=[get_weather],
    code_executor=BuiltInCodeExecutor(),
    generate_content_config=types.GenerateContentConfig(
        tool_config={"include_server_side_tool_invocations": True}
    )
)
