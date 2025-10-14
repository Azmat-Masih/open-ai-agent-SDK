# OpenAI Agents SDK Configuration Examples

This project demonstrates different ways to configure and use the OpenAI Agents SDK with Gemini API integration. It showcases three distinct configuration levels: Global, Runner, and Agent level configurations.

## Configuration Levels Overview

### 1. Global Level Configuration (`main.py`)
- Sets up default configuration that applies to all agents
- Uses `set_default_openai_client()` for global client configuration
- Configures global settings like tracing
- Best for: Application-wide defaults and settings

### 2. Runner Level Configuration (`main_2.py`)
- Configures settings at the execution level using `RunConfig`
- Allows different configurations for different execution contexts
- Can override global settings for specific runs
- Best for: Execution-specific configurations and overrides

### 3. Agent Level Configuration (`main_3.py`)
- Configures individual agents with custom settings
- Provides agent-specific model and client configurations
- Allows unique instructions per agent
- Best for: Agent-specific customization and behavior

## Project Details

- **Name:** global-level-practicing
- **Version:** 0.1.0
- **Description:** Example agent using OpenAI Agents SDK and Gemini API.

## Requirements

- Python >= 3.13
- `openai-agents` >= 0.3.1
- `python-dotenv` (for environment variable management)

## Installation

1. **Clone the repository** (if not already):
	```powershell
	git clone <your-repo-url>
	cd global-level-practicing
	```

2. **Install dependencies:**
	```powershell
	pip install -r requirements.txt
	# Or, if using pyproject.toml:
	pip install .

## Understanding the Examples

### Global Level Configuration (`main.py`)
```python
# Set global defaults
set_default_openai_client(external_client)
set_tracing_disabled(True)

# Create agent using global config
agent = Agent(name="Assistant", instructions="You are a helpful assistant")
```

### Runner Level Configuration (`main_2.py`)
```python
# Create runner config
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# Use config in runner
result = Runner.run_sync(agent, "Hello", run_config=config)
```

### Agent Level Configuration (`main_3.py`)
```python
# Configure individual agent
agent = Agent(
    name="Assistant",
    instructions="You only respond in haikus",
    model=OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=client
    )
)
```

## Installation & Setup (Step-by-Step)

### 1. Clone the Repository
```powershell
git clone <your-repo-url>
cd global-level-practicing
```

### 2. Install Python Dependencies
You can use either `pip` or `uv` (if available):

```powershell
# Using pip and pyproject.toml
pip install openai-agents python-dotenv

# Or, if you want to install all project dependencies
pip install .

# If you use uv (recommended for modern Python projects)
uv pip install -r requirements.txt
```

### 3. Configure Environment Variables and Files

1. Create a `.env` file in the project root:
   ```env
   GEMINI_API_KEY=your-gemini-api-key
   ```

2. Set up the example files:
   - `main.py` - Global configuration example
   - `main_2.py` - Runner level configuration example
   - `main_3.py` - Agent level configuration example

3. Understanding Configuration Precedence:
   - Agent-level settings override Runner-level settings
   - Runner-level settings override Global-level settings
   - Global settings serve as defaults
- Create a `.env` file in the project root (optional, recommended for secrets).
- Add your Gemini API key to `.env`:
  ```env
  GEMINI_API_KEY=your-gemini-api-key
  ```
- Alternatively, you can set the API key directly in `main.py`.

### 4. Review and Edit Agent Logic
- Open `main.py` and review the agent setup.
- The agent uses the Gemini API via the `openai-agents` SDK.
- You can customize the agent's instructions and model as needed.

### 5. Try Different Configuration Levels

Run each example to see how different configuration levels work:

```powershell
# Global Level Configuration
python main.py

# Runner Level Configuration
python main_2.py

# Agent Level Configuration
python main_3.py
```

### 6. Experiment with Configurations

Try modifying the examples:
1. Change agent instructions in different files
2. Experiment with different model settings
3. Try combining different configuration levels
4. Observe how configurations override each other
```powershell
python main.py
```

## Example Code
	 api_key=gemini_api_key,
	 base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
set_default_openai_client(external_client)

agent: Agent = Agent(name="Assistant", instructions="You are a helpful assistant", model="gemini-2.0-flash")

result = Runner.run_sync(agent, "Hello")

print(result.final_output)
```

## Notes

- Make sure your API key is valid and has access to Gemini API.
- You can customize the agent's instructions and model as needed.

## License

MIT
