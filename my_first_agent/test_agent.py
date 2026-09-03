# pytest, pytest-asyncio
import pytest
from google.adk.runners import InMemoryRunner
from agent import root_agent
from dotenv import load_dotenv

load_dotenv()

@pytest.mark.asyncio
async def test_agent_execution():
    runner = InMemoryRunner(agent=root_agent)
    response = await runner.run_debug("Calculate 10 + 5", verbose=False)
    assert "15" in str(response[-1])