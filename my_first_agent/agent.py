from google.adk.agents.llm_agent import Agent
import requests

def get_weather(city: str) -> dict:
    """
    Retrieves the weather for a given city

    Args:
        city: The name of the city to retrieve weather for
    """
    url = f'https://wttr.in/{city}?format=j1'
    reponse = requests.get(url)

    return reponse.json()

root_agent = Agent(
    model='gemini-3.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='You are a helpful assistant who answers in a short and concise manner',
    tools=[get_weather]
)