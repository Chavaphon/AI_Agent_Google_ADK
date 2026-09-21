# pytest, pytest-asyncio
import pytest
from google.adk.runners import InMemoryRunner
from agent import root_agent
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

@pytest.mark.asyncio
async def test_agent_execution():
    runner = InMemoryRunner(agent=root_agent)
    response = await runner.run_debug("What day is today", verbose=False)
    assert datetime.now().strftime('%A') in str(response[-1])