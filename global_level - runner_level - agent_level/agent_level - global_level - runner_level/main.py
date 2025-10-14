"""
Global Level Configuration Example
--------------------------------
This example demonstrates how to configure the OpenAI Agents SDK at a global level.
It sets up a default OpenAI client that will be used by all agents unless overridden.
Key features:
- Uses set_default_openai_client() for global configuration
- Sets tracing disabled globally
- Creates an agent that inherits the global configuration
"""

import os
import asyncio
from agents import Agent, Runner, AsyncOpenAI, set_default_openai_client, set_tracing_disabled, OpenAIChatCompletionsModel
from dotenv import load_dotenv
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
set_tracing_disabled(True)



external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    
)
set_default_openai_client(external_client)

agent: Agent = Agent(name="Assistant", instructions="You are a helpful assistant",  model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=external_client),)

result = Runner.run_sync(agent, "Hello")

print(result.final_output)