from google.adk.agents.llm_agent import Agent
from google.adk.agents import SequentialAgent, ParallelAgent

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

japanese_translator = Agent(
    name="japanese_translator",
    model="gemini-3.5-flash",
    instruction="""
    You are a professional English-to-Japanese translator.
    Translate the provided English story into natural, fluent Japanese.
    Output ONLY the translated Japanese text.
    """
)

parallel_translators = ParallelAgent(
    name="parallel_translators",
    sub_agents=[thai_translator, japanese_translator]
)

root_agent = SequentialAgent(
    name="root_agent",
    sub_agents=[story_writer, parallel_translators]
)