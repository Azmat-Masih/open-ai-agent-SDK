import os  # access environment variables and file/path utilities
import asyncio  # async support (imported for potential async tasks; not directly used below)
from openai import AsyncOpenAI  # async OpenAI-compatible client (here used for Gemini via OpenAI-compatible API)
from agents import (
    Agent,  # core Agent class used to define agent behavior
    OpenAIChatCompletionsModel,  # model wrapper connecting agents to an OpenAI-style chat model
    Runner,  # helper to run agents synchronously or asynchronously
    set_tracing_disabled,  # function to toggle internal tracing/telemetry
    handoff,  # utility for handing off tasks between agents (imported for completeness)
    function_tool,  # decorator/helper to expose functions as tools to agents (imported for completeness)
)

from agents import enable_verbose_stdout_logging  # enable more verbose logging to stdout for debugging

from dotenv import load_dotenv  # load environment variables from a .env file into the process env
load_dotenv()  # load .env immediately so os.getenv can read variables defined there
set_tracing_disabled(disabled=True)  # disable any built-in tracing to keep output minimal


# Read API key for Gemini (stored in GEMINI_API_KEY env var). None if not set.
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Reference: https://ai.google.dev/gemini-api/docs/openai
# Create an async OpenAI-compatible client that points at Google's Gemini REST endpoint.
# This client will be passed into the model wrapper used by agents below.
client = AsyncOpenAI(
    api_key=gemini_api_key,  # API key (string or None). Keep this confidential.
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",  # Gemini OpenAI-compatible base URL
)


# Define an entrepreneur agent: given a prompt, it should propose a business idea.
entrepreneur_Agent = Agent(
    name="Entrepreneur Agent",  # human-friendly name for logging and result attribution
    model=OpenAIChatCompletionsModel(openai_client=client, model="gemini-2.5-flash" ),  # model wrapper using the client
    instructions=(
        "You are an entrepreneur agent. Your task is to come up with a business idea."  # high-level instruction for the agent
    ),
)


# Define a business-planner agent: converts a business idea into a basic business plan.
bussiness_planner_Agent = Agent(
    name="Business Planner Agent",
    model=OpenAIChatCompletionsModel(openai_client=client, model="gemini-2.5-flash" ),
    instructions=(
        "You are a business planner agent. Your task is to create a business plan based on a business idea."
    ),
)


# Define a trigger agent whose role is to accept a user goal and hand off to the
# appropriate agent(s) (entrepreneur or business planner) to fulfill the task.
trigger_Agent = Agent(
    name="Trigger Agent",
    model=OpenAIChatCompletionsModel(openai_client=client, model="gemini-2.5-flash" ),
    instructions=(
        "You are a trigger agent. Your task is to handoffs to another agent that can perform a specific function."
    ),
    handoffs=[entrepreneur_Agent, bussiness_planner_Agent],  # agents this trigger may delegate work to
)


# Turn on verbose stdout logging so we can see what the agents do when they run.
enable_verbose_stdout_logging()


# Run the trigger agent synchronously with a user-level instruction.
# Runner.run_sync will execute the agent flow and return a Result-like object.
result = Runner.run_sync(
    trigger_Agent,  # agent to start the run from
    "Find the best business idea and create a business plan for it."  # user goal / prompt given to the trigger agent
)


# Print attribution: which agent produced the last step, and the final output text.
print("Agent Name:", result.last_agent.name)  # name of the agent that provided the final response
print("Final Result:", result.final_output)  # final text/result produced by the agent flow


# import os
# import asyncio
# from openai import AsyncOpenAI
# from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled, handoff, function_tool

# from agents import enable_verbose_stdout_logging

# from dotenv import load_dotenv
# load_dotenv()
# set_tracing_disabled(disabled=True)




# gemini_api_key = os.getenv("GEMINI_API_KEY")

# #Reference: https://ai.google.dev/gemini-api/docs/openai
# client = AsyncOpenAI(
#     api_key=gemini_api_key,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
# )


# entrepreneur_Agent = Agent(
#     name="Entrepreneur Agent",
#     model=OpenAIChatCompletionsModel(openai_client=client, model="gemini-2.5-flash" ),
#     instructions="You are an entrepreneur agent. Your task is to come up with a business idea.",
# )

# bussiness_planner_Agent = Agent(
#     name="Business Planner Agent",
#     model=OpenAIChatCompletionsModel(openai_client=client, model="gemini-2.5-flash" ),
#     instructions="You are a business planner agent. Your task is to create a business plan based on a business idea.",
# )

# trigger_Agent = Agent(
#     name="Trigger Agent",
#     model=OpenAIChatCompletionsModel(openai_client=client, model="gemini-2.5-flash" ),
#     instructions="You are a trigger agent. Your task is to handoffs to another agent that can perform a specific function.",
#     handoffs=[entrepreneur_Agent, bussiness_planner_Agent]
# )




# enable_verbose_stdout_logging()

# result = Runner.run_sync(
#     trigger_Agent, "Find the best business idea and create a business plan for it."
# )

# print("Agent Name:", result.last_agent.name)
# print("Final Result:", result.final_output)