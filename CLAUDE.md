# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

An interactive CLI chatbot that sends prompts to one of several LLM HTTP APIs (Ollama, Claude, OpenAI) using raw `requests` calls, not vendor SDKs. Python 3.14, managed with `uv` (created with `uv init --no-package`, so there's no installable entry point).

## Commands

```bash
uv sync                                  # install deps (including the dev group with pylint)
uv run python python_cli_chatbot         # run the app (run the package directory, see below)
PYTHONPATH=python_cli_chatbot uv run pylint python_cli_chatbot   # lint (PYTHONPATH needed for the import style below)
```

There's no test suite yet.

**Imports:** modules import each other as top-level packages (`from agent.agent import ...`, `from utils.constants import ...`), not as `python_cli_chatbot.agent...`. This only works when `python_cli_chatbot/` itself is on `sys.path`, which is why the app runs as `python python_cli_chatbot` and not `python -m python_cli_chatbot`. New modules should follow the same import style.

## Configuration

`.env` (loaded by `python-dotenv` at startup) supplies each provider's endpoint and key:
`ANTHROPIC_API_URL`/`ANTHROPIC_API_KEY`, `OPENAI_API_URL`/`OPENAI_API_KEY`, `OLLAMA_API_URL`/`OLLAMA_API_KEY`. Model names are hardcoded in the `Agent.setup_*` methods.

## Architecture

Control flow (`__main__.py`): `MainMenu.show()` loops until a provider is chosen, then a prompt loop calls `Agent.infer()` until the user types something containing "quit".

- **Singletons via `@lru_cache(maxsize=1)` factories:** `get_agent()`, `get_convo()`, and `get_stop()` return shared instances. Use these factories, not the constructors.
- **`Stop` flag** (`utils/stop.py`) is the shared loop-exit signal. Menu handlers call `get_stop().stop()` to leave the menu loop, and `main()` calls `clear()` before entering the prompt loop.
- **Provider dispatch** uses dicts keyed by the `API` enum (`utils/constants.py`) everywhere: menu choice → `Agent.change()` → `setup_*` fills an `ApiRecord` dataclass (url, key, model, headers); `Agent.create_payload()` builds the provider-specific request body; `agent/response.py` holds `post_request()` and `handle_response()`, which dispatches to a per-provider `handle_*_result`. Adding a provider means adding an `API` member plus an entry in each of these dicts.
- **Request payloads** are built only in `Agent.create_payload()`; `response.py` handles sending and parsing.
- **Ollama is handled differently:** `post_request` sends it without headers, and `handle_ollama_result` reads the body line by line as NDJSON, prints the content, and saves it to `Conversation`. The Claude and OpenAI handlers only log the answer.
- **`Conversation`** (`conversation/conversation.py`) is a placeholder: `save_prompt` and `save_response` only log for now.

The current branch (`15-add-pydantic-data-validation-for-response`) adds `pydantic` to validate the provider responses that `response.py` currently parses as raw dicts.

## Conventions

Every module starts with the `## python-cli-chatbot / ## module: <name>` banner docstring, and every function and class has a docstring (pylint expects them). Type annotations go on locals as well (`menu: MainMenu = MainMenu()`).
