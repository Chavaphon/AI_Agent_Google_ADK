# Video-1: Your First Agent

> Part 1 of the [AI Agent Google ADK](https://github.com/Chavaphon/AI_Agent_Google_ADK) tutorial series.
> **Next:** [Video-2: Custom Tools →](https://github.com/Chavaphon/AI_Agent_Google_ADK/tree/Video-2)

This branch builds the smallest working agent you can make with [Google Agent Development Kit (ADK)](https://adk.dev/): one Gemini model with an instruction. It has no tools and no memory. The goal is to understand the folder layout ADK expects and how to chat with an agent in the ADK Dev UI.

## What you'll learn

- How an ADK agent folder is structured (`__init__.py` + `agent.py` + `.env`)
- The core `Agent` parameters: `model`, `name`, `description`, `instruction`
- Why the variable must be called `root_agent`
- Running an agent with `adk web` (browser UI) and `adk run` (terminal)

## The code

`my_first_agent/agent.py`

```python
from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    model='gemini-3.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='You are a helpful assistant who answers in a short and concise manner',
)
```

| Parameter | What it does |
|---|---|
| `model` | The Gemini model that powers the agent. |
| `name` | A unique identifier for the agent. It matters once you have several agents (see Video-3). |
| `description` | A short summary of what the agent does. Other agents read it to decide whether to delegate to this one. |
| `instruction` | The system prompt. It shapes the agent's behavior and tone (here: short, concise answers). |

`my_first_agent/__init__.py`

```python
from . import agent
```

ADK loads the `my_first_agent` package and looks for a variable named **`root_agent`** in `agent.py`. That variable is the entry point for every conversation.

## Project structure

```
AI_Agent_Google_ADK/
├── my_first_agent/
│   ├── __init__.py     # Makes the folder a package and imports agent.py
│   ├── agent.py        # Defines root_agent
│   ├── .env            # Your API key (not committed)
│   └── .gitignore      # Ignores .env and .adk/
├── .gitignore
└── README.md
```

## Setup

**Prerequisites:** Python 3.10+ and a Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey).

```bash
git clone https://github.com/Chavaphon/AI_Agent_Google_ADK.git
cd AI_Agent_Google_ADK
git checkout Video-1

python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install google-adk
```

Create `my_first_agent/.env`:

```env
GOOGLE_GENAI_USE_ENTERPRISE=0
GOOGLE_API_KEY=your_api_key_here
```

`GOOGLE_GENAI_USE_ENTERPRISE=0` tells ADK to use the Gemini API with your API key instead of Vertex AI.

## Run it

Run these from the repository root (the folder that **contains** `my_first_agent/`):

```bash
# Browser UI at http://localhost:8000. Pick "my_first_agent" from the dropdown.
adk web

# Or chat in the terminal
adk run my_first_agent
```

### Try asking

- "What is an AI agent?"
- "Explain recursion in one sentence."

Try editing `instruction` (for example, "Always answer like a pirate") and restart the agent to see how much it changes the replies.

## Tip

You can generate this starter folder yourself with `adk create my_first_agent`, which creates `__init__.py`, `agent.py` and `.env` for you.

---

**Next:** [Video-2: Custom Tools →](https://github.com/Chavaphon/AI_Agent_Google_ADK/tree/Video-2), where the agent gets its first tool and fetches live weather data.
