# Video-4: Stateful Agents & SQLite Persistence

> Part 4 of the [AI Agent Google ADK](https://github.com/Chavaphon/AI_Agent_Google_ADK) tutorial series.
> **Previous:** [← Video-3: Multi-Agent Orchestration](https://github.com/Chavaphon/AI_Agent_Google_ADK/tree/Video-3) · **Next:** [Video-5: Testing & Cloud Run →](https://github.com/Chavaphon/AI_Agent_Google_ADK/tree/Video-5)

So far every conversation started from zero. This branch gives the agent **memory**: it saves user preferences into **session state**, and stores sessions in a **SQLite database**, so they survive restarts. Because the keys use the `user:` prefix, a preference saved in one session can be read back in a **completely different session** for the same user.

## What you'll learn

- **`ToolContext`:** giving a tool access to the current session's `state`
- **State scopes:** session-level keys vs. `user:`-prefixed keys
- **`DatabaseSessionService`:** persisting sessions to SQLite with `aiosqlite`
- **`Runner`:** running an agent from your own Python script instead of `adk web`
- Sending messages with `google.genai.types.Content` and reading the final response from the event stream

## State scopes in ADK

The prefix of a state key decides how long it lives and who can see it:

| Key | Scope | Lifetime |
|---|---|---|
| `car` | Current session only | Gone when you start a new session |
| `user:car` | All sessions of the **same `user_id`** in this app | Across sessions (persisted by the session service) |
| `app:car` | All users of this app | Across sessions |
| `temp:car` | Current invocation only | Discarded after the turn |

This branch uses `user:`.

## The code

`my_first_agent/agent.py` (abridged)

### 1. Tools that read and write user-level state

```python
from google.adk.tools import ToolContext

def set_user_profile(key: str, value: str, tool_context: ToolContext) -> str:
    """
    Saves a setting to the user's global profile across sessions.

    Args:
        key : name of the key. Do not include "user:"
    """
    tool_context.state[f"user:{key}"] = value      # 'user:' = user-level scope
    return f"Saved user preference: {key} = {value}"

def get_user_profile(key: str, tool_context: ToolContext) -> str:
    """
    Retrieves a setting from the user's global profile.

    Args:
        key : name of the key. Do not include "user:"
    """
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
```

ADK injects `tool_context` automatically. The model never sees it as an argument, and only fills in `key` and `value`. The docstring tells the model *not* to include `user:` itself, because the code adds the prefix.

### 2. A persistent session service and a Runner

```python
from google.adk.sessions import DatabaseSessionService
from google.adk.runners import Runner

session_service = DatabaseSessionService(db_url="sqlite+aiosqlite:///agent_data.db")

runner = Runner(
    app_name="my_first_agent",
    agent=root_agent,
    session_service=session_service,
    auto_create_session=True   # create the session if the ID doesn't exist yet
)
```

### 3. The demo: two different sessions, same user

```python
user_id = "user_42"

# Turn 1, session_001: "Save 'car' as Toyota"   → stores user:car = Toyota
# Turn 2, session_002: "Check the state 'car'"  → reads user:car from a NEW session
```

Each turn sends a `types.Content(role="user", parts=[...])` through `runner.run(...)` and prints the event where `event.is_final_response()` is true.

Turn 2 succeeds even though it runs in a new session, because the value was saved at **user** scope.

### Contrast: session-level state

The top of `agent.py` contains a commented-out version that saves keys **without** a prefix (`update_user_preference` / `get_user_preference`). Swap it in and turn 2 will report that nothing was found, because session-level state doesn't carry over to `session_002`.

> If you un-comment it, remove the stray `state` parameter from `update_user_preference(state, ...)`. Otherwise the model will see it as an extra required argument.

## Project structure

```
my_first_agent/
├── __init__.py
├── agent.py          # Tools, agent, session service, runner and demo main()
├── agent_data.db     # SQLite session store (committed as a demo artifact)
├── .env              # Your API key (not committed)
└── .gitignore
```

## Setup

**Prerequisites:** Python 3.10+ and a Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey).

```bash
git clone https://github.com/Chavaphon/AI_Agent_Google_ADK.git
cd AI_Agent_Google_ADK
git checkout Video-4

python -m venv .venv
# Windows: .venv\Scripts\activate    macOS / Linux: source .venv/bin/activate

pip install google-adk aiosqlite python-dotenv
```

Create `my_first_agent/.env`:

```env
GOOGLE_GENAI_USE_ENTERPRISE=0
GOOGLE_API_KEY=your_api_key_here
```

`load_dotenv()` at the top of `agent.py` loads this file when you run the script directly.

## Run it

Run the script from **inside** `my_first_agent/`, because the database path `sqlite+aiosqlite:///agent_data.db` is relative to your current directory:

```bash
cd my_first_agent
python agent.py
```

Expected output (wording varies):

```
Agent1: Saved user preference: car = Toyota
Agent2: User setting 'car' is 'Toyota'.
```

### Inspect the database

`agent_data.db` is a regular SQLite file. Open it with [DB Browser for SQLite](https://sqlitebrowser.org/) (or `sqlite3 agent_data.db`) to see the stored sessions, events and user state. Delete the file to start from a clean slate. It will be recreated on the next run.

### What about `adk web`?

`adk web` loads `root_agent` from this file, but it doesn't run `main()` or use the `runner` defined here. It uses its own session service. The tools still work in the UI, but the SQLite persistence demo is meant to be run with `python agent.py`.

---

**Next:** [Video-5: Automated Testing & Cloud Run Deployment →](https://github.com/Chavaphon/AI_Agent_Google_ADK/tree/Video-5)
