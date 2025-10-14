import os  # used for reading environment variables (like API keys)
from agents import (
    Agent,  # class for defining an agent with model, instructions, and options
    handoff,  # helper to perform explicit handoffs between agents (imported for completeness)
    function_tool,  # decorator/helper to expose python functions as tools to agents (imported for completeness)
    Runner,  # provides run_sync / run_async helpers to execute agents
    set_tracing_disabled,  # controls internal tracing/telemetry behavior
    OpenAIChatCompletionsModel,  # model adapter for OpenAI-style chat completions
    enable_verbose_stdout_logging,  # toggles more verbose agent stdout logging
    ModelSettings,  # container for model-specific runtime settings (temperature, tokens, tools)
)
from openai import AsyncOpenAI  # async OpenAI-style client used to call the model backend (Gemini via OpenAI API surface)
import asyncio  # provides async primitives if needed elsewhere

from dotenv import load_dotenv  # loads environment variables from a .env file into os.environ
load_dotenv()  # immediately load any .env in the project root for local development
set_tracing_disabled(disabled=True)  # disable tracing to avoid noisy telemetry/logs during runs

# Read Gemini API key from environment (configured via .env or OS env)
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Create an async client pointed at Google's Gemini OpenAI-compatible endpoint.
# The client will be passed into the model adapters used by agents below.
client = AsyncOpenAI(
    api_key=gemini_api_key,  # API key string used to authenticate requests
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",   # Gemini OpenAI-compatible base URL
)

# Agent 1 : Movie Recommender Agent according to mood
movie_recommender_agent = Agent(
    name="Movie Recommender Agent",  # readable name used in logs and result attribution
    model=OpenAIChatCompletionsModel(openai_client=client, model="gemini-2.5-flash" ),  # model wrapper using the shared client
    instructions=(
        "You are a movie recommender agent. Your task is to recommend a movie based on the user's mood."
    ),  # instruction string guides the agent's behavior
    model_settings=ModelSettings(temperature=0.1)  # low temperature for deterministic recommendations
)

# Agent 2 : Movie Details Agent to provide details about the movie
movie_details_agent = Agent(
    name="Movie Details Agent",
    model=OpenAIChatCompletionsModel(openai_client=client, model="gemini-2.5-flash" ),
    instructions=(
        "You are a movie details agent. Your task is to provide details about a given movie."
    ),  # instruction string for the details agent
    model_settings=ModelSettings(max_tokens=1000)  # allow longer responses for movie details
)

# Trigger Agent to handoff tasks to the appropriate agent
trigger_agent = Agent(
    name="Trigger Agent",
    model=OpenAIChatCompletionsModel(openai_client=client, model="gemini-2.5-flash" ),
    instructions=(
        "You are a trigger agent. Your task is to handoff to another agent that can perform a specific function."
    ),  # this agent's role is routing/dispatch
    handoffs=[movie_recommender_agent, movie_details_agent],  # agents this trigger may delegate work to
    model_settings= ModelSettings(tool_choice="auto", max_tokens=1200, parallel_tool_calls=True)  # use auto tool selection and allow parallel tool calls
)

enable_verbose_stdout_logging()  # enable verbose logs to stdout for debugging / visibility
result = Runner.run_sync(
    trigger_agent, 
    # Different user prompts (commented out) demonstrating possible input variations.
    # "I am feeling adventurous and want to watch a movie. Can you recommend one and provide some details about it?" # user goal / prompt given to the trigger agent
    # "I am feeling low, and want to watch a movie. Can you recommend one and provide some details about it?"  # user goal / prompt given to the trigger agent
    # "I am feeling happy and want to watch a movie. Can you recommend one and provide some details about it?"  # user goal / prompt given to the trigger agent
    # "I am feeling sad and want to watch a movie. Can you recommend one and provide some details about it?"  # user goal / prompt given to the trigger agent
    "I am feeling excited and want to watch a movie. Can you recommend one and provide some details about it?"  # user goal / prompt given to the trigger agent
    # "I am feeling nostalgic and want to watch a movie. Can you recommend one and provide some details about it?"  # user goal / prompt given to the trigger agent
)

print("Agent Name:", result.last_agent.name)  # name of the agent that provided the final response
print("Final Result:", result.final_output)  # final text/result produced by the agent flow