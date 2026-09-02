from google.adk.agents import Agent
from google.adk.tools import ToolContext

def update_user_preference(state, preference_key: str, preference_value: str, tool_context: ToolContext) -> dict:
    """Updates a value in the session state mid-run."""
    tool_context.state[preference_key] = preference_value
    return {"status": "success", "updated_key": preference_key}

def get_user_preference(preference_key: str, tool_context: ToolContext) -> str:
    """Gets a saved user preference value from state."""
    val = tool_context.state.get(preference_key)
    if val is None:
        return f"No preference found for '{preference_key}'."
    return f"The stored value for '{preference_key}' is '{val}'."

root_agent = Agent(
    name="stateful_agent",
    model="gemini-3.5-flash",
    instruction="You help manage user settings. Update state when requested.",
    tools=[update_user_preference, get_user_preference]
)