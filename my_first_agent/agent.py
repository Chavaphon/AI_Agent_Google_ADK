from google.adk.agents.llm_agent import Agent
from google.adk.agents import SequentialAgent
from google.adk.tools import AgentTool

story_writer = Agent(
    name="story_writer",
    model="gemini-2.5-flash",
    instructions="""
    You are a creative storyteller. Write a compelling, engaging short story 
    based on the user's prompt. Output ONLY the story in clear English.
    """
)

thai_translator = Agent(
    name="thai_translator",
    model="gemini-2.5-flash",
    instructions="""
    You are a professional English-to-Thai translator. 
    Translate the provided English story into natural, fluent Thai.
    Output ONLY the translated Thai text.
    """
)

# japanese_translator = Agent(
#     name="japanese_translator",
#     model="gemini-2.5-flash",
#     instructions="""
#     You are a professional English-to-Japanese translator. 
#     Translate the provided English story into natural, expressive Japanese.
#     Output ONLY the translated Japanese text.
#     """
# )

root_agent = Agent(
    name="root_agent",
    model="gemini-2.5-flash",
    instructions="""
    You are the coordinator for creative storytelling. 
    Format and display the results clearly with sections:
    1. English Original
    2. Thai Translation (ภาษาไทย)
    """,
    sub_agents=[story_writer, thai_translator]
)