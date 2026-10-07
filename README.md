# Video-5: Automated Testing & Cloud Run Deployment

> Part 5 of the [AI Agent Google ADK](https://github.com/Chavaphon/AI_Agent_Google_ADK) tutorial series.
> **Previous:** [← Video-4: Stateful Agents](https://github.com/Chavaphon/AI_Agent_Google_ADK/tree/Video-4) · **Home:** [main](https://github.com/Chavaphon/AI_Agent_Google_ADK)

An agent you can only check by chatting with it by hand isn't production-ready. This branch covers two steps toward production:

1. **Automated testing:** a `pytest` test that runs the agent with `InMemoryRunner` and checks its answer.
2. **Deployment:** shipping the agent to **Google Cloud Run** so it runs as a public web service.

To keep the focus on testing and deployment, the agent is deliberately simple. It starts again from the Video-1 agent and adds one tool, `get_day`.

## What you'll learn

- **`InMemoryRunner`:** running an agent in-process with a throwaway in-memory session, which is ideal for tests
- **`run_debug`:** sending a single prompt and getting the events back in one call
- **`pytest-asyncio`:** writing `async` tests
- Pinning dependencies with `requirements.txt`
- Deploying an ADK agent with `adk deploy cloud_run`

## The agent

`my_first_agent/agent.py`

```python
from google.adk.agents.llm_agent import Agent
from datetime import datetime

def get_day() -> str:
    """
    Retrieves today's day
    """
    today = datetime.now()
    return today.strftime('%A')

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
    tools=[get_day]
)
```

`my_first_agent/__init__.py` exports `root_agent` directly, the form used for deployment:

```python
from .agent import root_agent

__all__ = ["root_agent"]
```

## The test

`my_first_agent/test_agent.py`

```python
import pytest
from google.adk.runners import InMemoryRunner
from agent import root_agent
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

@pytest.mark.asyncio
async def test_agent_execution():
    runner = InMemoryRunner(agent=root_agent)
    reponse = await runner.run_debug("What day is today?", verbose=False)
    assert datetime.now().strftime('%A') in str(reponse[-1])
```

The model can't know today's date on its own, so a passing test proves the agent **actually called the `get_day` tool** and used its result.

- `InMemoryRunner` needs no database or session setup, and nothing is saved after the test.
- `run_debug(...)` returns the list of events. `reponse[-1]` is the final reply.

> **Note:** this test calls the real Gemini API, so it needs a valid key in `.env` and uses a little quota. Model output is non-deterministic, so an occasional failure is possible. Treat it as an integration test.

## Setup

**Prerequisites:** Python 3.10+ and a Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey).

```bash
git clone https://github.com/Chavaphon/AI_Agent_Google_ADK.git
cd AI_Agent_Google_ADK
git checkout Video-5

python -m venv .venv
# Windows: .venv\Scripts\activate    macOS / Linux: source .venv/bin/activate

pip install -r requirements.txt
```

`requirements.txt` pins every package. Key ones: `google-adk==2.8.0`, `google-genai==2.20.0`, `pytest==9.1.1`, `pytest-asyncio==1.4.0`, `python-dotenv==1.2.3`.

Create `my_first_agent/.env`:

```env
GOOGLE_GENAI_USE_ENTERPRISE=0
GOOGLE_API_KEY=your_api_key_here
```

## Run the agent locally

```bash
adk web            # from the repository root, then select "my_first_agent"
```

Ask: *"What day is today?"*

## Run the tests

The test imports `agent` as a top-level module, so run it from **inside** `my_first_agent/` with `python -m pytest` (which adds the current folder to the import path):

```bash
cd my_first_agent
python -m pytest test_agent.py -v
```

## Deploy to Google Cloud Run

`adk deploy cloud_run` packages the agent folder into a container, builds it with Cloud Build and deploys it to Cloud Run. You don't need to write a Dockerfile. (This branch first tried a hand-written Dockerfile in commit [`6717ae8`](https://github.com/Chavaphon/AI_Agent_Google_ADK/commit/6717ae8). It was removed in the deployment commit [`0ed06b9`](https://github.com/Chavaphon/AI_Agent_Google_ADK/commit/0ed06b9), which also switched the model to `gemini-2.5-flash`.)

**Prerequisites**

- A Google Cloud project with billing enabled
- The [Google Cloud CLI](https://cloud.google.com/sdk/docs/install), logged in:

```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

**Deploy** (run from the repository root):

```bash
# Windows PowerShell: use $env:GOOGLE_CLOUD_PROJECT="..." instead of export
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_CLOUD_LOCATION="us-central1"

adk deploy cloud_run \
  --project=$GOOGLE_CLOUD_PROJECT \
  --region=$GOOGLE_CLOUD_LOCATION \
  --service_name=my-first-agent \
  --with_ui \
  ./my_first_agent
```

- `--with_ui` also deploys the ADK Dev UI, so you can chat with the agent in the browser. Leave it out to deploy the API server only.
- When it finishes, the command prints the service URL. Open it to use the deployed agent.
- If the agent needs extra packages, put a `requirements.txt` **inside** `my_first_agent/` so they're installed in the container.

For authentication options (API key secret vs. Vertex AI) and the full flag list, see the [ADK Cloud Run guide](https://adk.dev/deploy/cloud-run/).

**Clean up** when you're done, so you aren't billed:

```bash
gcloud run services delete my-first-agent --region=$GOOGLE_CLOUD_LOCATION
```

---

**Back to the series overview:** [main branch README](https://github.com/Chavaphon/AI_Agent_Google_ADK)
