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

> **How the deployed agent reaches Gemini:** locally the agent uses the API key in `.env`, but `.env` is **not** uploaded (`adk deploy` skips files listed in `my_first_agent/.gitignore`). The container ADK builds is set up to use **Vertex AI** in your project instead (`GOOGLE_GENAI_USE_ENTERPRISE=1`). That's why the steps below enable the Vertex AI API and give Cloud Run's service account the *Vertex AI User* role.

**Prerequisites:** a Google Cloud project with billing enabled.

The commands below are for **Windows PowerShell** and are meant to be run in order, in **one terminal**, from the repository root. A macOS / Linux (bash) version is further down.

### 1. Install and set up the Google Cloud CLI

```powershell
winget install -e --id Google.CloudSDK

# Allow PowerShell to run the gcloud script, and add gcloud to PATH for this terminal
# (or just open a new terminal after installing)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
$env:Path += ";$env:LOCALAPPDATA\Google\Cloud SDK\google-cloud-sdk\bin"

gcloud --version
gcloud init              # log in and choose a default project
gcloud projects list     # find your project ID
```

### 2. Set your project and enable the APIs

Replace `your-project-id` with your own project ID. The other values can stay as they are.

```powershell
$PROJECT_ID = "your-project-id"
$REGION     = "us-central1"
$SERVICE    = "my-first-agent"

gcloud config set project $PROJECT_ID
gcloud services enable run.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com aiplatform.googleapis.com
```

These variables only exist in the current terminal. If you open a new one, run the three `$... =` lines again.

### 3. Allow Cloud Run to call Vertex AI

Cloud Run services run as your project's default Compute Engine service account (`PROJECT_NUMBER-compute@developer.gserviceaccount.com`). Give it the *Vertex AI User* role:

```powershell
$PROJECT_NUM = gcloud projects describe $PROJECT_ID --format="value(projectNumber)"

gcloud projects add-iam-policy-binding $PROJECT_ID `
  --member="serviceAccount:${PROJECT_NUM}-compute@developer.gserviceaccount.com" `
  --role="roles/aiplatform.user" `
  --condition=None
```

### 4. Deploy

```powershell
adk deploy cloud_run `
  --project=$PROJECT_ID `
  --region=$REGION `
  --service_name=$SERVICE `
  --app_name=my_first_agent `
  ./my_first_agent
```

- The first deploy takes a few minutes. If `gcloud` asks to create an Artifact Registry repository, answer `y`.
- If it asks **"Allow unauthenticated invocations?"**, answer `y` for this tutorial, because the test in step 5 sends no auth token. Anyone who has the URL can then call your agent and use your quota, so delete the service when you're done (see *Clean up*).
- `--app_name` is the `appName` you use in API calls (step 5). It defaults to the folder name.
- If the agent needs extra packages, put a `requirements.txt` **inside** `my_first_agent/` so they're installed in the container.

### 5. Test the deployed agent

This looks up the service URL, creates a new session, then sends a message to the `/run` endpoint:

```powershell
$SERVICE_URL = gcloud run services describe $SERVICE --region=$REGION --format="value(status.url)"
$USER_ID     = "user_123"
$SESSION_ID  = "session_$(Get-Date -Format yyyyMMddHHmmss)"

# Create a session
Invoke-RestMethod -Method Post -Uri "$SERVICE_URL/apps/my_first_agent/users/$USER_ID/sessions/$SESSION_ID"

# Send a message
$body = @{
  appName    = "my_first_agent"
  userId     = $USER_ID
  sessionId  = $SESSION_ID
  newMessage = @{
    role  = "user"
    parts = @(@{ text = "What day is today?" })
  }
} | ConvertTo-Json -Depth 5

$response = Invoke-RestMethod -Method Post -Uri "$SERVICE_URL/run" -ContentType "application/json" -Body $body
$response.content.parts.text
```

The last line prints the agent's reply, for example *"Today is Wednesday."* Each run uses a new session ID, so you can run the block again.

### Clean up

Delete the service when you're done, so you aren't billed and the public URL stops working:

```powershell
gcloud run services delete $SERVICE --region=$REGION
```

The container images are stored in the Artifact Registry repository `cloud-run-source-deploy`. If nothing else in your project uses that repository, you can delete it too: `gcloud artifacts repositories delete cloud-run-source-deploy --location=$REGION`.

<details>
<summary><b>macOS / Linux (bash) version</b></summary>

Install the Google Cloud CLI by following the [official instructions](https://cloud.google.com/sdk/docs/install) (on macOS with Homebrew: `brew install --cask google-cloud-sdk`), then run from the repository root:

```bash
gcloud init

PROJECT_ID="your-project-id"
REGION="us-central1"
SERVICE="my-first-agent"

gcloud config set project "$PROJECT_ID"
gcloud services enable run.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com aiplatform.googleapis.com

PROJECT_NUM=$(gcloud projects describe "$PROJECT_ID" --format="value(projectNumber)")
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:${PROJECT_NUM}-compute@developer.gserviceaccount.com" \
  --role="roles/aiplatform.user" \
  --condition=None

adk deploy cloud_run \
  --project="$PROJECT_ID" \
  --region="$REGION" \
  --service_name="$SERVICE" \
  --app_name=my_first_agent \
  ./my_first_agent
```

Test it:

```bash
SERVICE_URL=$(gcloud run services describe "$SERVICE" --region="$REGION" --format="value(status.url)")
USER_ID="user_123"
SESSION_ID="session_$(date +%Y%m%d%H%M%S)"

curl -X POST "$SERVICE_URL/apps/my_first_agent/users/$USER_ID/sessions/$SESSION_ID"

curl -X POST "$SERVICE_URL/run" \
  -H "Content-Type: application/json" \
  -d '{
    "appName": "my_first_agent",
    "userId": "'"$USER_ID"'",
    "sessionId": "'"$SESSION_ID"'",
    "newMessage": {"role": "user", "parts": [{"text": "What day is today?"}]}
  }'
```

Clean up:

```bash
gcloud run services delete "$SERVICE" --region="$REGION"
```

</details>

For more options (custom service accounts, `--with_ui`, the full flag list), see the [ADK Cloud Run guide](https://adk.dev/deploy/cloud-run/).

---

**Back to the series overview:** [main branch README](https://github.com/Chavaphon/AI_Agent_Google_ADK)
