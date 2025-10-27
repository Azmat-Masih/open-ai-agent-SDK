import os
import asyncio
from dataclasses import dataclass
from agents import (
    Agent,
    function_tool,
    OpenAIChatCompletionsModel,
    handoff,
    Runner,
    AsyncOpenAI,
    ModelSettings,
    set_tracing_disabled,
    enable_verbose_stdout_logging,
    RunContextWrapper
)
from dotenv import load_dotenv
load_dotenv()
set_tracing_disabled(disabled=True)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
external_client = AsyncOpenAI(api_key=GEMINI_API_KEY, base_url=BASE_URL)

# Define a simple context using a dataclass
@dataclass
class UserInfo:  
    name: str
    uid: int

# A tool function that accesses local context via the wrapper
@function_tool
async def fetch_user_age(wrapper: RunContextWrapper[UserInfo]) -> str:  
    return f"User {wrapper.context.name} is 47 years old"

async def main():
    # Create your context object
    user_info = UserInfo(name="John", uid=123)  

    # Define an agent that will use the tool above
    agent = Agent[UserInfo](  
        name="Assistant",
        model=OpenAIChatCompletionsModel(
            openai_client=external_client,
            model="gemini-2.5-flash" ,
        ),
        tools=[fetch_user_age],
    )
    
# enable_verbose_stdout_logging( )

    # Run the agent, passing in the local context
    result = await Runner.run(
        starting_agent=agent,
        input="What is the age of the user?",
        context=user_info,
    )

    print(result.final_output)  # Expected output: The user John is 47 years old.

if __name__ == "__main__":
    asyncio.run(main())



# result = Runner.run_sync( )