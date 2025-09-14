# My Agent Project

## Overview
This project demonstrates a simple AI agent using Google's Gemini API to answer math-related questions. The agent is implemented in Python and can be run from the command line.

## Setup Steps

1. **Clone the repository**
   - Place the project files in your working directory.

2. **Install dependencies**
   - Run the following command in PowerShell:
     ```powershell
     pip install -r requirements.txt
     ```

3. **Set up environment variables**
   - Create a `.env` file in the project root.
   - Add your Gemini API key:
     ```env
     GEMINI_API_KEY=your_api_key_here
     ```

4. **Run the agent**
   - Execute the main script:
     ```powershell
     python main.py
     ```

## Main Components
- `main.py`: Contains the agent logic and example usage.
- `requirements.txt`: Lists required Python packages.
- `.env`: Stores your Gemini API key (not included in repo).

## Issues to Avoid
- **Missing `.env` file or API key**: The script will raise an error if `GEMINI_API_KEY` is not set.
- **Incorrect Python version**: Ensure you are using Python 3.13 or newer (see `pyproject.toml`).
- **Dependency installation**: Always run `pip install -r requirements.txt` before executing the script.
- **Event loop errors**: If running in Jupyter or other async environments, `nest_asyncio` is applied to avoid event loop issues.

## Troubleshooting
- If you see `ValueError: ❌ GEMINI_API_KEY not found in .env file`, check your `.env` file and ensure the key is correct.
- For package errors, verify all dependencies are installed and compatible with your Python version.

## Key Value Takeaways

- **Environment Variables**: Always keep your API keys secure and never commit them to version control.
- **Dependency Management**: Use `requirements.txt` to ensure consistent environments across machines.
- **Python Version**: Match your Python version to the one specified in `pyproject.toml` for best compatibility.
- **Error Handling**: The script checks for missing API keys and will alert you if setup is incomplete.
- **Async Support**: `nest_asyncio` is used to avoid event loop issues, especially in Jupyter environments.
- **Modularity**: The agent logic is encapsulated in a function for easy reuse and extension.
- **Troubleshooting**: Clear error messages help quickly identify and resolve setup issues.

## License
This project is for educational purposes.
