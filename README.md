# AI Agent Google ADK

A hands-on tutorial series for building AI agents with [Google Agent Development Kit (ADK)](https://adk.dev/) and Gemini. Each branch goes with one video and teaches one concept, starting from a minimal "hello world" agent and moving on to tools, multi-agent pipelines, persistent memory, testing and deployment to Google Cloud Run.

Every branch has its own README with a full walkthrough, setup steps and things to try.

## Branches

| Branch | Topic | You'll learn |
|---|---|---|
| [`Video-1`](https://github.com/Chavaphon/AI_Agent_Google_ADK/tree/Video-1) | Your First Agent | `Agent`, `model`, `instruction`, `root_agent`, `adk web` / `adk run` |
| [`Video-2`](https://github.com/Chavaphon/AI_Agent_Google_ADK/tree/Video-2) | Custom Tools | Python functions as tools, docstrings & type hints, a live weather API (plus an earlier look at built-in tools) |
| [`Video-3`](https://github.com/Chavaphon/AI_Agent_Google_ADK/tree/Video-3) | Multi-Agent Orchestration | `SequentialAgent`, `ParallelAgent`, `sub_agents` |
| [`Video-4`](https://github.com/Chavaphon/AI_Agent_Google_ADK/tree/Video-4) | Stateful Agents & SQLite Persistence | `ToolContext`, `user:` state scope, `DatabaseSessionService`, `Runner` |
| [`Video-5`](https://github.com/Chavaphon/AI_Agent_Google_ADK/tree/Video-5) | Automated Testing & Cloud Run Deployment | `InMemoryRunner`, `pytest-asyncio`, `requirements.txt`, `adk deploy cloud_run` |
| `main` | Series overview | This README, plus the Video-4 stateful agent (merged in PR #1) |

> **Each branch is self-contained.** Video-2 to Video-5 all start from the Video-1 agent and add **one** concept, rather than building on each other. For example, Video-5 doesn't include the state or multi-agent code from Video-3 and Video-4. That keeps each lesson small and easy to read.

## Learning path

```
Video-1 ──► Video-2 ──► Video-3 ──► Video-4 ──► Video-5
First       Custom      Multi-agent  State &      Testing &
agent       tools       pipelines    persistence  Cloud Run
```

### Video-1: Your First Agent

A single Gemini model with an instruction, and nothing else. It introduces the folder layout ADK expects (`__init__.py`, `agent.py`, `.env`) and the `root_agent` entry point.

### Video-2: Custom Tools

Adds a `get_weather(city)` tool that calls the [wttr.in](https://wttr.in) API for **live** weather, and shows how the model uses the docstring and type hints to decide when and how to call it. The branch history also has an earlier experiment with built-in tools (`BuiltInCodeExecutor`, and `google_search`, which caused `429 RESOURCE_EXHAUSTED` on the free tier).

### Video-3: Multi-Agent Orchestration

A story pipeline. A `story_writer` writes an English story, then a `ParallelAgent` runs a Thai translator and a Japanese translator **at the same time**, all wrapped in a `SequentialAgent`.

```
root_agent (SequentialAgent)
├── story_writer
└── parallel_translators (ParallelAgent)
    ├── thai_translator
    └── japanese_translator
```

### Video-4: Stateful Agents & SQLite Persistence

Tools read and write `tool_context.state["user:<key>"]`. The `user:` prefix makes a value available in **every session of the same user**. Sessions are stored in SQLite with `DatabaseSessionService` (`sqlite+aiosqlite:///agent_data.db`), and a `Runner` script shows a value saved in `session_001` being read back from `session_002`.

### Video-5: Automated Testing & Cloud Run Deployment

A simple agent with a `get_day` tool, a `pytest` test that runs it through `InMemoryRunner` and checks it really used the tool, pinned dependencies in `requirements.txt`, and deployment to **Google Cloud Run** with `adk deploy cloud_run`.

## What's on `main`

`main` holds the Video-4 stateful agent with a slightly different demo: it saves *"my preferred language as Japanese"* in one session and asks *"What is my preferred language?"* in another. Run it from inside the agent folder:

```bash
cd my_first_agent
python agent.py
```

## Getting started

**Prerequisites:** Python 3.10+ and a Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey).

```bash
git clone https://github.com/Chavaphon/AI_Agent_Google_ADK.git
cd AI_Agent_Google_ADK
git checkout Video-1          # or any branch you want to explore

python -m venv .venv
# Windows: .venv\Scripts\activate    macOS / Linux: source .venv/bin/activate

pip install google-adk        # see each branch's README for extra packages
```

Create `my_first_agent/.env` (it's git-ignored):

```env
GOOGLE_GENAI_USE_ENTERPRISE=0
GOOGLE_API_KEY=your_api_key_here
```

Then, from the repository root:

```bash
adk web                  # ADK Dev UI at http://localhost:8000
adk run my_first_agent   # chat in the terminal
```

## Project structure

```
AI_Agent_Google_ADK/
├── my_first_agent/
│   ├── __init__.py       # Exposes the agent module to ADK
│   ├── agent.py          # Agent definition (different on every branch)
│   ├── .env              # Your API key (not committed)
│   ├── agent_data.db     # SQLite session store (Video-4 and main)
│   └── test_agent.py     # pytest test (Video-5)
├── requirements.txt      # Pinned dependencies (Video-5)
├── .gitignore
└── README.md
```

## Key dependencies

| Package | Used in | Purpose |
|---|---|---|
| `google-adk` | All | Agent types, tools, runners, sessions, CLI (`adk web`, `adk deploy`) |
| `google-genai` | All (installed with ADK) | Gemini API client and `types.Content` |
| `requests` | Video-2 | HTTP calls to the weather API |
| `aiosqlite` | Video-4, main | Async SQLite driver for `DatabaseSessionService` |
| `python-dotenv` | Video-4, Video-5, main | Load `.env` when running scripts or tests directly |
| `pytest`, `pytest-asyncio` | Video-5 | Async agent tests |

## Resources

- [Google ADK documentation](https://adk.dev/)
- [Deploying ADK agents to Cloud Run](https://adk.dev/deploy/cloud-run/)
- [Gemini API](https://ai.google.dev/)
- [Google AI Studio (API keys)](https://aistudio.google.com/apikey)
