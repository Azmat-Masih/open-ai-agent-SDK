# Tool Calling Practice Project

This project demonstrates the implementation of an AI agent capable of performing mathematical operations using tool calling capabilities. It showcases how to create and use custom tools with an AI model, specifically using the Gemini API.

## Project Overview

The project implements a math assistant that can:
- Perform basic arithmetic operations (addition, subtraction, multiplication, division)
- Follow mathematical order of operations (DMAS rule)
- Handle user queries and provide calculated results
- Implement error handling (e.g., division by zero)

## Project Structure

```
tool-calling/
├── main.py           # Main implementation file with AI agent and tools
├── pyproject.toml    # Project configuration and dependencies
└── README.md        # Project documentation
```

## Setup Instructions

1. **Environment Setup**

First, initialize UV (Universal Virtualenv) for better dependency management:
```powershell
uv init
```

Then create and activate a virtual environment:
```powershell
python -m venv venv
.\venv\Scripts\activate
```

2. **Install Dependencies**

Install the required packages:
```powershell
pip install openai-agents python-dotenv
```

3. **Environment Variables**

Create a `.env` file in the project root and add your Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
```

## Code Structure

The main.py file is structured as follows:

1. **Imports and Configuration**
   - Imports necessary modules from the agents package
   - Sets up environment variables and API configuration

2. **Tool Definitions**
   - `sum_numbers`: Adds two numbers
   - `multiply_numbers`: Multiplies two numbers
   - `divide_numbers`: Divides two numbers with zero-division check
   - `subtract_numbers`: Subtracts second number from first

3. **Agent Configuration**
   - Creates an AI agent with Gemini model
   - Configures model settings and instructions
   - Assigns mathematical tools to the agent

4. **Execution**
   - Enables verbose logging for debugging
   - Runs the agent with a mathematical query
   - Displays the calculated result

## Usage

To run the project:

```powershell
python main.py
```

The program will execute a sample mathematical operation following the DMAS rule (Division, Multiplication, Addition, Subtraction).

## Key Features

1. **Tool-based Architecture**
   - Custom function tools for each operation
   - Decorated with `@function_tool` for integration
   - Type hints for better code clarity

2. **Error Handling**
   - Division by zero protection
   - Type checking through annotations

3. **Configurability**
   - Environment variable based API key management
   - Adjustable model parameters (temperature, etc.)
   - Verbose logging option for debugging

4. **Extensibility**
   - Easy to add new mathematical operations
   - Modular design for adding more functionality

## Development Notes

- The project uses async capabilities but runs synchronously for simplicity
- Model temperature is set to 0.1 for consistent results
- Verbose logging helps in understanding the tool calling process
- The Gemini model is used through a custom API endpoint

## Troubleshooting

1. **API Key Issues**
   - Ensure the `.env` file exists
   - Verify the API key is correctly set
   - Check for any whitespace in the key

2. **Execution Errors**
   - Verify Python version compatibility
   - Ensure all dependencies are installed
   - Check for proper virtual environment activation

## Future Enhancements

- Add more complex mathematical operations
- Implement async execution mode
- Add unit tests for tools
- Expand error handling capabilities
- Add support for batch calculations
