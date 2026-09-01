from google.adk.agents.llm_agent import Agent
from google.adk.agents import SequentialAgent

story_writer = Agent(
    name="story_writer",
    model="gemini-3.5-flash",
    instruction="""
    You are a creative storyteller. Write a compelling, engaging short story 
    based on the user's prompt. Output ONLY the story in clear English.
    """
)

thai_translator = Agent(
    name="thai_translator",
    model="gemini-3.5-flash",
    instruction="""
    You are a professional English-to-Thai translator. 
    Translate the provided English story into natural, fluent Thai.
    Output ONLY the translated Thai text.
    """
)

root_agent = SequentialAgent(
    name="root_agent",
    sub_agents=[story_writer, thai_translator]
)