# Handsoff Agent-as-Tool — README

This repository contains example agent definitions that demonstrate how to build small multi-agent flows using an OpenAI-compatible (Gemini) backend and the `agents` helper library. The examples include:

- `main.py` — simple entrepreneur/business-planner handoff example
- `model_config.py` — movie recommender + details agents with trigger routing
- `agent_as_tool.py` — shows how agents can be exposed and used as tools

This README provides step-by-step instructions to set up, configure, and run the examples on Windows using PowerShell.

## Prerequisites

- Python 3.10+ installed (verify with `python --version`)
- Recommended: create and use a virtual environment (venv)
- A Gemini (Google generative models) API key stored in `GEMINI_API_KEY` (or another OpenAI-compatible key if you adapt the base_url)

## Quick setup (PowerShell)

1. Open PowerShell and change to the project directory:

```powershell
cd "D:\Agentic AI Course Practice\ope-ai-agent-SDK\handsoff-agent-as-tool"
```

2. Create a virtual environment (if you don't have one yet):

```powershell
python -m venv .venv
```

3. Activate the virtual environment in PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

4. Upgrade pip and install dependencies used by these examples (adjust package names to match your environment):

```powershell
python -m pip install --upgrade pip
python -m pip install black python-dotenv openai-agents openai
```

Notes:
- The project examples use an `agents` helper library. If your environment uses a different package name or a local package, install that accordingly.
- `black` is optional but recommended for formatting.

## Configure environment variables

1. Create a `.env` file in the project root (same folder as `main.py`) with the following content:

```
GEMINI_API_KEY=your_api_key_here
```

2. Alternatively, set the environment variable in PowerShell for the current session:

```powershell
$env:GEMINI_API_KEY = 'your_api_key_here'
```

Keep your API keys private — do not commit `.env` to source control.

## Running the examples

- Run the `agent_as_tool.py` example (the script will call the configured model and print results):

```powershell
python .\agent_as_tool.py
```

- Run the `model_config.py` example:

```powershell
python .\model_config.py
```

- Run the `main.py` example:

```powershell
python .\main.py
```

If you receive authentication errors, double-check `GEMINI_API_KEY` and the `base_url` used when creating the `AsyncOpenAI` client.

## Formatting and linting

- Format a file with Black:

```powershell
python -m black .\agent_as_tool.py
```

- Format the entire project directory:

```powershell
python -m black .
```

## Troubleshooting

- If you see network or HTTP errors, ensure your API key is valid and your machine can reach the `base_url`.
- If imports fail for `agents` or `openai`, verify the correct package names and that your virtual environment is active.
- For permission errors activating the venv on PowerShell, you may need to change the execution policy (temporary):

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

## Next steps / customization

- Swap models by changing the `model` parameter when creating `OpenAIChatCompletionsModel`.
- Add your own agents by instantiating `Agent(...)` and wiring them into `Runner.run_sync`.
- Expose functions as tools using `function_tool` if you need agents to call local Python helpers.

If you want, I can:
- Run one of the example scripts for you and show the output (requires GEMINI_API_KEY),
- Add short descriptions inside each example file (if you'd like more inline documentation), or
- Create a minimal `requirements.txt` or `pyproject.toml` listing the exact packages used.

---

End of README