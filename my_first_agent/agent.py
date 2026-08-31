from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    model='gemini-3.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
    tools=['get_weather']
)

def get_weather(location: str) -> dict:
    """
    Retrieves the weather for a given location

    Args:
        location: The name of the city to retrieve weather for
    """
    return {"location": location, "weather": "Sunny"}

# search_agent = LlmAgent(
#     model='gemini-3.5-flash',
#     name="WebSearchAgent",
#     instruction="Answer questions using live web data.",
#     tools=["google_search"]
# )

# coder_agent = LlmAgent(
#     model='gemini-3.5-flash',
#     name="MathAgent",
#     instruction="Solve complex math problems by running Python code.",
#     tools=["built_in_code_execution"]
# )