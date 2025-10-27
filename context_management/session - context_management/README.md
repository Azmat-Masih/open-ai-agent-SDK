# Context Management Practice — Session

This repository contains small example scripts demonstrating context management patterns using an agent framework (examples use constructs such as Agent, Runner, function_tool, and RunContextWrapper). The purpose of these examples is to practice passing local context into tools and agents, understand how to structure context objects, and highlight best practices for handling sensitive information.

## Files

- `main.py`
- `main_1.py`
- `main_2.py`
- `pyproject.toml`

## Quick project overview

These scripts show minimal examples of defining dataclass-based context objects and using them with an `Agent` and `Runner`. They demonstrate:

- How to create a local context dataclass (for user info or session info).
- How to write `function_tool` functions that accept a `RunContextWrapper[T]` and access `wrapper.context`.
- How to run an agent with `Runner.run(..., context=...)` to pass local data into the tools.

The code uses an async OpenAI-compatible client (`AsyncOpenAI`) with the GEMINI API key read from environment variables. Make sure you never commit your API keys to source control.

## main.py — summary

Purpose: A concise example showing a `UserInfo` dataclass and a function tool that uses the wrapper to return the user's age.

Key points:

- `UserInfo` dataclass: has `name` and `uid` fields.
- `fetch_user_age(wrapper: RunContextWrapper[UserInfo])` reads `wrapper.context.name` and returns a string.
- `Runner.run(..., context=user_info)` runs the agent with the local `user_info` instance.

Usage:

```powershell
# Set your API key in .env or environment
$Env:GEMINI_API_KEY = "your_api_key_here"
python main.py
```

Expected output: Prints the tool output referencing the `UserInfo` (e.g., "User John is 47 years old").

## main_1.py — summary

Purpose: Demonstrates a richer `UserInfo` dataclass with sensitive fields included (age, pswd, email, uid) and a tool that returns many fields.

Key points:

- `UserInfo` contains `pswd` and `email` fields. The example tool `fetch_user_info` returns all fields — including the password string.
- This file intentionally demonstrates what *not* to do in production: exposing plaintext secrets in context objects and printing them.

Security note (important):

- Never include plaintext passwords, tokens, or secrets in context objects that may be passed to remote models or logged. If you must include a credential-like value, replace it with a reference (an ID, token reference, or secure handle). Use a secret manager or environment variables and keep secrets out of agent-visible context.

Usage:

```powershell
$Env:GEMINI_API_KEY = "your_api_key_here"
python main_1.py
```

## main_2.py — summary

Purpose: Shows a different context dataclass (`UserContext`) and an example agent with `instructions` that inspect the context. Also includes a `search` tool that simulates a blocking delay.

Key points:

- `UserContext` is small with `username` and optional `email`.
- `special_prompt(special_context, agent)` demonstrates using the context and agent name to produce system-style instructions dynamically.
- `search(local_context: RunContextWrapper[UserContext], query: str)` simulates I/O (with a time.sleep(30) in the example) — useful to illustrate how longer-running tools can be modeled.

Usage:

```powershell
$Env:GEMINI_API_KEY = "your_api_key_here"
python main_2.py
```

## Context management best practices (summary and recommendations)

1. Principle: Keep context minimal and domain-specific
- Include only the data necessary for the task. Prefer small, explicit dataclasses or typed structures.

2. Sensitive data: never pass secrets to untrusted models or tools
- Replace raw secrets with opaque references (IDs, tokens managed by a secrets service).
- Read secrets from environment variables, OS-level secret stores, or dedicated secret managers (HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, GCP Secret Manager).
- Rotate and audit keys frequently.

3. Logging and telemetry
- Never log raw sensitive fields (passwords, tokens, PII). Mask or redact fields before logging.
- If you must log a reference, log only stable, non-secret identifiers.

4. Agents and external models
- Treat model calls as external network calls. Avoid sending raw credentials or PII unless the model is designed for and authorized to receive them.

5. Least privilege
- Provide the agent/tool with the minimum privileges required to perform its job. Use service accounts and short-lived tokens where possible.

6. Storage and caching
- Avoid caching plaintext secrets. If caching is necessary, encrypt at rest and restrict access.

7. Testing and reviews
- Include unit tests that assert secrets are not present in example outputs or logs. Use code reviews and automated linters to detect accidental secrets.

## Sensitive data examples from this repo

- `main_1.py` currently includes a `pswd` field and prints it. For practice, replace `pswd` with a reference ID or remove it entirely. Example: store password in the environment as `APP_USER_PASSWORD` and only use it in a server-side authentication call — don't include it in `RunContextWrapper`.

## How to run (Windows PowerShell)

Set the environment variable (temporary, current session):

```powershell
$Env:GEMINI_API_KEY = "your_api_key_here"
python main.py
python main_1.py
python main_2.py
```

If you prefer a .env file, create a `.env` with:

```
GEMINI_API_KEY=your_api_key_here
```

and ensure `python-dotenv` is installed (the examples call `load_dotenv()`).

## Dependencies

- The code references an `agents` package (Agent, Runner, function_tool, RunContextWrapper, AsyncOpenAI, OpenAIChatCompletionsModel). Install the project's dependencies using the project tooling in `pyproject.toml` or add the required packages to your environment. Example (if using pip and a requirements file):

```powershell
# If you have requirements.txt
# pip install -r requirements.txt
# Or with pyproject.toml (poetry):
# poetry install
pip install python-dotenv
```

Note: Replace package installation commands with your environment's package manager instructions if this repo uses Poetry or similar.

## Quick checklist to make examples safer

- Remove plaintext secrets from dataclasses.
- Replace sensitive fields with references or IDs.
- Ensure `load_dotenv()` is only used for local development and `.env` is in `.gitignore`.
- Add automated checks (pre-commit hooks) to detect accidental secrets.

## Contributing and next steps

- If you'd like, I can:
	- Add a small test to verify no sensitive fields are printed.
	- Refactor `main_1.py` to remove the `pswd` field and show a secure pattern.
	- Add a requirements.txt or update `pyproject.toml` with the used packages.

## License

This repository contains example code for learning purposes. No license specified — add one if you plan to publish or share.

---

If you'd like, I can now:

1. Refactor `main_1.py` to remove the password field and show a secure pattern (recommended).
2. Add a small test that checks for sensitive fields being printed.

Tell me which of those you'd like next, or I can proceed with both.

