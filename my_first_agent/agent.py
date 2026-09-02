from google.adk.agents import Agent
from google.adk.tools import ToolContext
from google.adk.sessions import DatabaseSessionService
from google.adk.runners import Runner
from google.genai import types
import asyncio
from dotenv import load_dotenv

load_dotenv()

# Session-Level State
# def update_user_preference(state, preference_key: str, preference_value: str, tool_context: ToolContext) -> dict:
#     """Updates a value in the session state mid-run."""
#     tool_context.state[preference_key] = preference_value
#     return {"status": "success", "updated_key": preference_key}

# def get_user_preference(preference_key: str, tool_context: ToolContext) -> str:
#     """Gets a saved user preference value from state."""
#     val = tool_context.state.get(preference_key)
#     if val is None:
#         return f"No preference found for '{preference_key}'."
#     return f"The stored value for '{preference_key}' is '{val}'."

# root_agent = Agent(
#     name="stateful_agent",
#     model="gemini-3.5-flash",
#     instruction="You help manage user settings. Update state when requested.",
#     tools=[update_user_preference, get_user_preference]
# )

# User-Level State
def set_user_profile(key: str, value: str, tool_context: ToolContext) -> str:
    """Saves a setting to the user's global profile across sessions."""
    # Prefixing with 'user:' designates user-level scope
    tool_context.state[f"user:{key}"] = value
    return f"Saved user preference: {key} = {value}"

def get_user_profile(key: str, tool_context: ToolContext) -> str:
    """Retrieves a setting from the user's global profile."""
    value = tool_context.state.get(f"user:{key}")
    if value is None:
        return f"No user setting found for '{key}'."
    return f"User setting '{key}' is '{value}'."

root_agent = Agent(
    name="stateful_agent",
    model="gemini-3.5-flash-lite",
    instruction="You help manage user settings. Update state when requested.",
    tools=[set_user_profile, get_user_profile]
)

# Persistant Database
session_service = DatabaseSessionService(db_url="sqlite+aiosqlite:///agent_data.db")

runner = Runner(
    app_name="my_first_agent",
    agent=root_agent,
    session_service=session_service,
    auto_create_session=True
)

# Test
async def main():
    session_id = "session_001"
    user_id = "user_42"

    # Now execute turn 1
    user_message1 = types.Content(
        role="user",
        parts=[types.Part.from_text(text="Save my preferred language as Japanese.")]
    )

    events1 = runner.run(
        session_id=session_id,
        user_id=user_id,
        new_message=user_message1
    )

    for event in events1:
        if event.is_final_response():
            print("Agent1:", event.content.parts[0].text)
    
    # Now execute turn 2
    user_message2 = types.Content(
        role="user",
        parts=[types.Part.from_text(text="What is my preferred language?")]
    )

    events2 = runner.run(
        session_id="session_002",
        user_id=user_id,
        new_message=user_message2
    )

    for event in events2:
        if event.is_final_response():
            print("Agent2:", event.content.parts[0].text)

if __name__ == "__main__":
    asyncio.run(main())