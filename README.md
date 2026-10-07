# Video-2: Custom Tools

> Part 2 of the [AI Agent Google ADK](https://github.com/Chavaphon/AI_Agent_Google_ADK) tutorial series.
> **Previous:** [← Video-1: Your First Agent](https://github.com/Chavaphon/AI_Agent_Google_ADK/tree/Video-1) · **Next:** [Video-3: Multi-Agent Orchestration →](https://github.com/Chavaphon/AI_Agent_Google_ADK/tree/Video-3)

An LLM only knows what was in its training data. **Tools** let an agent act in the real world: call an API, read a file, run code. This branch gives the Video-1 agent a plain Python function, `get_weather`, which fetches **live weather** from [wttr.in](https://wttr.in). The model decides on its own when to call it.

## What you'll learn

- Turning an ordinary Python function into an agent tool
- Why the **docstring and type hints** matter: they are how the model knows what the tool does and which arguments to pass
- Registering tools with `tools=[...]`
- Watching tool calls happen in the ADK Dev UI

## The code

`my_first_agent/agent.py`

```python
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
```

### How a tool call works

1. You ask: *"What's the weather in Bangkok?"*
2. The model reads the tool's name, docstring and signature (`city: str`) and decides to call `get_weather(city="Bangkok")`.
3. ADK runs your Python function and sends the JSON result back to the model.
4. The model turns the raw JSON into a short, readable answer.

**Writing good tools:**

- **Docstring:** describe what the tool does and each argument (`Args:`). The model reads this text.
- **Type hints:** `city: str` tells the model the argument's type.
- **Return value:** return a `dict` (JSON-serializable), so the model gets structured data.

## Earlier in this branch: built-in tools

Before settling on the custom weather tool, this branch experimented with ADK's **built-in tools**. These commits are worth checking out if you want to see them:

| Commit | What it tried |
|---|---|
| [`efe2de3`](https://github.com/Chavaphon/AI_Agent_Google_ADK/commit/efe2de3) | `BuiltInCodeExecutor`, so Gemini can write and run Python. Enabled with `generate_content_config=types.GenerateContentConfig(tool_config={"include_server_side_tool_invocations": True})`. Also includes a commented-out `google_search` import, because it caused `429 RESOURCE_EXHAUSTED` errors on the free tier. |
| [`406b8f0`](https://github.com/Chavaphon/AI_Agent_Google_ADK/commit/406b8f0) | Replaced the mock weather (`"Sunny"`) with the real wttr.in API and added a `write_to_file` tool. |
| [`4a92de5`](https://github.com/Chavaphon/AI_Agent_Google_ADK/commit/4a92de5) | Simplified to the final version above: a single custom tool and a concise instruction. |

```bash
git checkout efe2de3   # look around (detached HEAD)
git checkout Video-2   # come back
```

## Setup

**Prerequisites:** Python 3.10+ and a Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey).

```bash
git clone https://github.com/Chavaphon/AI_Agent_Google_ADK.git
cd AI_Agent_Google_ADK
git checkout Video-2

python -m venv .venv
# Windows: .venv\Scripts\activate    macOS / Linux: source .venv/bin/activate

pip install google-adk requests
```

Create `my_first_agent/.env`:

```env
GOOGLE_GENAI_USE_ENTERPRISE=0
GOOGLE_API_KEY=your_api_key_here
```

## Run it

From the repository root:

```bash
adk web            # http://localhost:8000, then select "my_first_agent"
# or
adk run my_first_agent
```

### Try asking

- "What's the weather in Bangkok right now?"
- "Is it colder in Tokyo or Seoul today?" (the agent calls the tool twice)
- "Should I bring an umbrella in London?"

In `adk web`, open the **Events** panel to see the `get_weather` function call, its arguments and the raw JSON response.

---

**Next:** [Video-3: Multi-Agent Orchestration →](https://github.com/Chavaphon/AI_Agent_Google_ADK/tree/Video-3), where several agents work together in a pipeline.
