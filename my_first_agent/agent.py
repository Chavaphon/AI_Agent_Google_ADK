from google.adk.agents.llm_agent import Agent
from datetime import datetime

def get_day() -> str:
    """
    Retrieves today's day 
    """
    today = datetime.now()
    return today.strftime('%A')

root_agent = Agent(
    model='gemini-3.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
    tools=[get_day]
)
