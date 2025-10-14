import os
import asyncio
from openai import AsyncOpenAI
from agents import (
    Agent,
    OpenAIChatCompletionsModel,
    Runner,
    set_tracing_disabled,
    handoff,
    function_tool,
)

from agents import enable_verbose_stdout_logging

from dotenv import load_dotenv

load_dotenv()
set_tracing_disabled(disabled=True)


gemini_api_key = os.getenv("GEMINI_API_KEY")

# Reference: https://ai.google.dev/gemini-api/docs/openai
client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)


entrepreneur_Agent = Agent(
    name="Entrepreneur Agent",
    model=OpenAIChatCompletionsModel(openai_client=client, model="gemini-2.5-flash"),
    instructions="You are an entrepreneur agent. Your task is to come up with a business idea.",
).as_tool(
    tool_name="entrepreneur_Agent",
    tool_description="You are an entrepreneur agent. Your task is to come up with a business idea.",
)

bussiness_planner_Agent = Agent(
    name="Business Planner Agent",
    model=OpenAIChatCompletionsModel(openai_client=client, model="gemini-2.5-flash"),
    instructions="You are a business planner agent. Your task is to create a business plan based on a business idea.",
).as_tool(
    tool_name="business_planner_Agent",
    tool_description="You are a business planner agent. Your task is to create a business plan based on a business idea.",
)

trigger_Agent = Agent(
    name="Trigger Agent",
    model=OpenAIChatCompletionsModel(openai_client=client, model="gemini-2.5-flash"),
    # instructions="You are a trigger agent. Your task is to handoffs to another agent that can perform a specific function.",
    # handoffs=[entrepreneur_Agent, bussiness_planner_Agent],
    instructions="based on the user's request. Use the available tools when appropriate.",
    tools=[bussiness_planner_Agent, entrepreneur_Agent],
)


enable_verbose_stdout_logging()

result = Runner.run_sync(
    trigger_Agent, "Find the best business idea and create a business plan for it."
)

print("Agent Name:", result.last_agent.name)
print("Final Result:", result.final_output)
print("type of result:", type(result))
