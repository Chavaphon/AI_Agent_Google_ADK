# Video-3: Multi-Agent Orchestration (Sequential + Parallel)

> Part 3 of the [AI Agent Google ADK](https://github.com/Chavaphon/AI_Agent_Google_ADK) tutorial series.
> **Previous:** [← Video-2: Custom Tools](https://github.com/Chavaphon/AI_Agent_Google_ADK/tree/Video-2) · **Next:** [Video-4: Stateful Agents →](https://github.com/Chavaphon/AI_Agent_Google_ADK/tree/Video-4)

One agent with one prompt can only do so much. ADK lets you split work across **specialized agents** and connect them with **workflow agents** that control the order they run in. This branch builds a story pipeline:

1. A **story writer** writes a short story in English from your prompt.
2. Two **translators** then run **at the same time**, one producing Thai and one producing Japanese.

```
root_agent (SequentialAgent)            runs its children one after another
├── story_writer (Agent)                1. writes the English story
└── parallel_translators (ParallelAgent) 2. runs its children concurrently
    ├── thai_translator (Agent)            → Thai translation
    └── japanese_translator (Agent)        → Japanese translation
```

## What you'll learn

- **`SequentialAgent`:** runs sub-agents in a fixed order (step 1, then step 2)
- **`ParallelAgent`:** runs sub-agents concurrently, which suits independent tasks
- **`sub_agents`:** nesting workflow agents to build a pipeline
- How later agents see earlier output: agents in the pipeline share the same session, so the translators can read the story from the conversation history

## The code

`my_first_agent/agent.py`

```python
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
```

### Key points

- **Workflow agents don't call an LLM themselves.** `SequentialAgent` and `ParallelAgent` have no `model` or `instruction`. They only orchestrate their `sub_agents`.
- **The translators are independent**, so running them in parallel saves time compared with translating one after the other.
- **Parallel branches don't see each other's output.** The Thai translator can't read the Japanese translation, and that's fine here.
- **Each `name` must be unique** within the agent tree.

## Setup

**Prerequisites:** Python 3.10+ and a Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey).

```bash
git clone https://github.com/Chavaphon/AI_Agent_Google_ADK.git
cd AI_Agent_Google_ADK
git checkout Video-3

python -m venv .venv
# Windows: .venv\Scripts\activate    macOS / Linux: source .venv/bin/activate

pip install google-adk
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

- "A cat who wants to become an astronaut"
- "A lost robot finding its way home in Bangkok"

You'll get three replies: the English story, then the Thai and Japanese versions. In `adk web`, the event list shows which agent produced each message, and you can see the two translators running side by side.

## Going further

- Give `story_writer` an `output_key="story"` and reference `{story}` in the translators' instructions. This passes the story through **session state** instead of relying on conversation history (state is the topic of Video-4).
- Add a third step to the `SequentialAgent`, such as a reviewer agent that compares the two translations.

---

**Next:** [Video-4: Stateful Agents & SQLite Persistence →](https://github.com/Chavaphon/AI_Agent_Google_ADK/tree/Video-4), where the agent remembers things across sessions.
