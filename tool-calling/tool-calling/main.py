# Import required modules and components
import os
from agents import (
    Agent,                           # Core agent class for creating AI agents
    function_tool,                   # Decorator to create function-based tools
    OpenAIChatCompletionsModel,      # Model class for chat completions
    handoff,                         # Utility for agent handoffs
    Runner,                          # Runner class for executing agent tasks
    AsyncOpenAI,                     # Async client for API calls
    ModelSettings,                   # Settings class for model configuration
    set_tracing_disabled,           # Function to disable tracing
    enable_verbose_stdout_logging,   # Function to enable verbose logging
)
from dotenv import load_dotenv      # For loading environment variables

# Load environment variables from .env file
load_dotenv()

# Disable tracing for cleaner output
set_tracing_disabled(disabled=True)

# Get Gemini API key from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Set the base URL for the Gemini API
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

# Create an async client for API calls
external_client = AsyncOpenAI(api_key=GEMINI_API_KEY, base_url=BASE_URL)


# Define tool functions for basic arithmetic operations
@function_tool
def sum_numbers(num1: int, num2: int) -> int:
    """
    Add two numbers together.
    Args:
        num1 (int): First number
        num2 (int): Second number
    Returns:
        int: Sum of the two numbers
    """
    return sum([num1, num2])  # Using sum() function for addition


@function_tool
def multiply_numbers(num1: int, num2: int) -> int:
    """
    Multiply two numbers together.
    Args:
        num1 (int): First number
        num2 (int): Second number
    Returns:
        int: Product of the two numbers
    """
    return num1 * num2


@function_tool
def divide_numbers(num1: int, num2: int) -> float:
    """
    Divide first number by second number.
    Args:
        num1 (int): Dividend (number being divided)
        num2 (int): Divisor (number to divide by)
    Returns:
        float: Result of division
    Raises:
        ValueError: If attempting to divide by zero
    """
    if num2 == 0:
        raise ValueError("Cannot divide by zero.")
    return num1 / num2


@function_tool
def subtract_numbers(num1: int, num2: int) -> int:
    """
    Subtract second number from first number.
    Args:
        num1 (int): First number (minuend)
        num2 (int): Second number (subtrahend)
    Returns:
        int: Difference between the two numbers
    """
    return num1 - num2


# Create an AI agent specialized in mathematical operations
trigger_agent = Agent(
    # Configure the model with Gemini's API
    model=OpenAIChatCompletionsModel(
        openai_client=external_client,
        model="gemini-2.5-flash"  # Using Gemini's model
    ),
    # Set model parameters
    model_settings=ModelSettings(temperature=0.1),  # Low temperature for more deterministic output
    # Define the agent's role and capabilities
    instructions="You are a helpful math assistant. You can perform basic arithmetic operations such as addition, subtraction, multiplication, and division. Use the provided tools to perform calculations when necessary.",
    # Provide the arithmetic tools to the agent
    tools=[sum_numbers, multiply_numbers, divide_numbers, subtract_numbers],
    name="Math Assistant",  # Give the agent a name
)

# Enable detailed logging for better debugging and understanding
enable_verbose_stdout_logging()

# Execute the agent with a mathematical query
result = Runner.run_sync(
    trigger_agent,
    "Using DMAS rule, What is 25 multiplied by 4, then divided by 2, and finally add 10 to the result? ",
)

# Print the final calculation result
print("Final Result:", result.final_output)
