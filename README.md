# AI Agent Google ADK

A hands-on learning series for building AI agents with [Google Agent Development Kit (ADK)](https://google.github.io/adk-docs/). Each branch corresponds to a video tutorial and progressively introduces more advanced ADK concepts — from a minimal "hello world" agent all the way to persistent state, multi-agent orchestration, and automated testing.

---

## Branch Overview

| Branch | Topic |
|---|---|
| `Video-1` | Minimal LLM Agent |
| `Video-2` | Custom Tools & Code Execution |
| `Video-3` | Multi-Agent Orchestration (Sequential + Parallel) |
| `Video-4` | Stateful Agents & Persistent Session (SQLite) |
| `Video-5` | Upgraded Model & Automated Testing with pytest |
| `main` | Latest state (mirrors Video-4/5 with user-level state) |

---

## Branch Details

### `Video-1` — Your First Agent

A minimal working agent using `google.adk.agents.llm_agent.Agent`. No tools, no state — just an LLM wired up and ready to chat.

```python
from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    model='gemini-3.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
)
```

**Concepts covered:** `Agent`, `model`, `instruction`, `description`

---

### `Video-2` — Custom Tools & Code Execution

Extends Video-1 by adding a custom Python tool (`get_weather`) and enabling the `BuiltInCodeExecutor` so the agent can write and run code during a conversation.

```python
from google.adk.code_executors import BuiltInCodeExecutor

def get_weather(location: str) -> dict:
    """Retrieves the weather for a given location."""
    return {"location": location, "weather": "Sunny"}

root_agent = Agent(
    ...
    tools=[get_weather],
    code_executor=BuiltInCodeExecutor(),
)
```

**Concepts covered:** custom tool functions, `BuiltInCodeExecutor`, `GenerateContentConfig`, `tool_config`

> **Note:** The branch also includes a commented-out `google_search` tool reference with a warning that it causes `429 RESOURCE_EXHAUSTED` errors under the free tier.

---

### `Video-3` — Multi-Agent Orchestration

Demonstrates how to compose multiple specialized agents using `SequentialAgent` and `ParallelAgent`. A story-writing pipeline is built where one agent writes an English short story, then two translation agents run **in parallel** to produce Thai and Japanese versions simultaneously.

```
root_agent (SequentialAgent)
├── story_writer        → writes English story
└── parallel_translators (ParallelAgent)
    ├── thai_translator → translates to Thai
    └── japanese_translator → translates to Japanese
```

**Concepts covered:** `SequentialAgent`, `ParallelAgent`, sub-agents, agent pipelines

---

### `Video-4` — Stateful Agents & SQLite Persistence

Introduces session state and a persistent database backend. User preferences are stored with a `user:` key prefix, which makes them survive across different sessions for the same user. The agent uses `DatabaseSessionService` backed by SQLite via `aiosqlite`.

```python
from google.adk.sessions import DatabaseSessionService
from google.adk.runners import Runner
from google.adk.tools import ToolContext

def set_user_profile(key: str, value: str, tool_context: ToolContext) -> str:
    tool_context.state[f"user:{key}"] = value
    return f"Saved user preference: {key} = {value}"

session_service = DatabaseSessionService(db_url="sqlite+aiosqlite:///agent_data.db")

runner = Runner(
    app_name="my_first_agent",
    agent=root_agent,
    session_service=session_service,
    auto_create_session=True
)
```

The branch includes `agent_data.db` (the SQLite file) committed to the repo as a demo artifact.

**Concepts covered:** `ToolContext`, session-level vs user-level state (`user:` prefix), `DatabaseSessionService`, `Runner`, `auto_create_session`, `asyncio`

> The branch also contains commented-out code showing **session-level** state (without the `user:` prefix) as a contrast.

---

### `Video-5` — Model Upgrade & Automated Testing

Upgrades the agent model from `gemini-3.5-flash` to `gemini-2.5-flash` and adds a `pytest`-based test suite using `InMemoryRunner` for fast, side-effect-free agent testing.

**`test_agent.py`:**
```python
import pytest
from google.adk.runners import InMemoryRunner
from agent import root_agent

@pytest.mark.asyncio
async def test_agent_execution():
    runner = InMemoryRunner(agent=root_agent)
    response = await runner.run_debug("Calculate 10 + 5", verbose=False)
    assert "15" in str(response[-1])
```

Also the first branch to include a `requirement.txt` with pinned dependencies (key ones: `google-adk==2.8.0`, `google-genai==2.20.0`, `aiosqlite==0.22.1`, `dotenv==0.9.9`, `fastapi==0.141.1`).

**Concepts covered:** `InMemoryRunner`, `run_debug`, `pytest-asyncio`, dependency pinning

---

## Project Structure

```
my_first_agent/
├── __init__.py        # Exports the agent module
├── agent.py           # Agent definition (varies per branch)
├── test_agent.py      # Pytest suite (Video-5+ only)
└── agent_data.db      # SQLite session store (Video-4+ only)
requirement.txt        # Pinned dependencies (Video-5 only)
.gitignore
README.md
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- A Google AI API key (Gemini)

### Installation

```bash
git clone https://github.com/Chavaphon/AI_Agent_Google_ADK.git
cd AI_Agent_Google_ADK

# Check out the branch you want to explore
git checkout Video-5

# Install dependencies
pip install google-adk python-dotenv aiosqlite
# Or, on Video-5, use the pinned requirements:
pip install -r requirement.txt
```

### Configuration

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_api_key_here
```

### Running the Agent

```bash
# Interactive web UI (ADK Dev UI)
adk web

# Or run the agent script directly (Video-4/main)
python my_first_agent/agent.py
```

### Running Tests (Video-5)

```bash
pip install pytest pytest-asyncio
pytest my_first_agent/test_agent.py -v
```

---

## Key Dependencies

| Package | Purpose |
|---|---|
| `google-adk` | Agent Development Kit — agent types, runners, sessions |
| `google-genai` | Gemini model API client |
| `aiosqlite` | Async SQLite driver for persistent sessions |
| `python-dotenv` | Load API keys from `.env` |
| `pytest-asyncio` | Async test support for pytest |

---

## Learning Path

Follow the branches in order for a guided progression:

```
Video-1 → Video-2 → Video-3 → Video-4 → Video-5
  ↓           ↓          ↓           ↓          ↓
Basic      Tools &   Multi-     Persistent  Testing &
Agent     Code Exec  Agent      Sessions   Model v2
```

---

## Resources

- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [Gemini API](https://ai.google.dev/)