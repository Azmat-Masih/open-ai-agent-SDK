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
    age: int
    pswd: str
    email: str
    uid: int    
    

# A tool function that accesses local context via the wrapper
@function_tool  
async def fetch_user_info(wrapper: RunContextWrapper[UserInfo])->str:
    return f"user: {wrapper.context.name}, age: {wrapper.context.age}, pswd: {wrapper.context.pswd}, email: {wrapper.context.email}, uid: {wrapper.context.uid}"


async def main():
    # Create your context object
    user_info = UserInfo(name="John", age=47, pswd="s3cr3t", email="john@abc.com", uid=123)
    # Define an agent that will use the tool above
    agent = Agent[UserInfo](
        name="Assistant",
        model=OpenAIChatCompletionsModel(
            openai_client=external_client,
            model="gemini-2.5-flash" ,
        ),
        tools=[fetch_user_info],
    )
    #enable_verbose_stdout_logging( )   
    # Run the agent, passing in the local context
    result = await Runner.run(
        starting_agent=agent,
        input="Fetch the user name.",
        context=user_info,
    )   
    print(result.final_output)  # Expected output: The user John is 47 years old.
    
if __name__ == "__main__":
    asyncio.run(main())