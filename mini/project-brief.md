# Aider Mini > Project Brief

Aider Mini is a lightweight coding assistant with a CLI interface based on and built alongside the forked Aider codebase. It is intended primarily for the personal use of its developer.

## Core Motivation

- **Limitations of Web Interfaces:** While frontier LLMs used via stateful web interfaces offer massive context windows and superior reasoning, the web interface itself has major limitations. *Blindness:* Web interfaces do not allow frontier LLMs to read repository structure and local files. *Lack of Agency:* Web interfaces do not allow frontier LLMs to write code modifications directly back to local files. *Copy/Pasting:* The limitations of web interfaces force users to perform tedious copy/pasting of context and edits.
- **Limitations of APIs:** LLMs used via standard CLI and stateless API interfaces (like original Aider) re-send thousands of tokens (system prompts, repo maps, active files, and chat history) on every single turn, creating unnecessary *token bloat* and *rigid workflows*.
- **Aider Mini** bridges this gap by aiding the user in exploiting the full potential of stateful web interfaces while avoiding the heavy prompting via stateless APIs. Aider Mini automates prompting (*Prompt/Context Generator*, Eyes), applies LLM edit instructions to local files (*File Editor*, Right Hand) and executes CLI commands requested by the LLM (*CLI Executor*, Left Hand).

## Target Audience & Primary Use Case

- **Developer Persona:** Software engineers who prefer acessing high-performing frontier LLMs via web interfaces for interactive coding, architecture, and refactoring, but want full automation for context gathering and disk file edits.
- **Target Environment:** Local terminal (PowerShell / VS Code terminal) on Windows 11 / macOS / Linux, integrated directly into developer file-editing workflows.

## Architectural Pillars and Directory Structure

**Aider Mini** is structured around three main pillars:

### Pillar 1: EYES | Context/Prompt Generator
- **System Prompt Generator (`/sys`):** Copies the *system prompt* to the clipboard that teaches the LLM how to assist the user and how to output `SEARCH/REPLACE` diff edit blocks.
- **Repository Prompt Generator (`/repo`):** Copies the *repository prompt* to the clipboard that tells the LLM how to access the project repository and where to find general project context.
- **Active File Selector (`/file`):** Copies the *active file prompt* to the clipboard with instructions for the LLM on which file to edit and how to retrieve its current contents.

### Pillar 2 > Local File Editor
- **CLI Command:** `/apply`
- **Location:** `mini/editor/`
- **`editor.py`:** Reads the LLM response from clipboard. Reads content from the local target file. Orchestrates the file edit pipeline.
- **`response_parser.py`:** Parses the LLM response to locate the `SEARCH/REPLACE` markers.
- **`search.py`:** Identifies `SEARCH` lines to be replaced in the local file.
- **`replace.py`:** Replaces `SEARCH` lines with `REPLACE` lines in the local file.

### Pillar 3: LEFT HAND | Command Line Executor (`/run`)
- Executes terminal commands requested by the LLM to perform os operations and copies terminal output back to the clipboard.

## Directory Structure

### Project Root: `aider-mini/`
Contains all folders/files of the forked **Aider** repository.
- `markdown.css`: Stylesheet for Vs Code markdown viewer.
- `pyproject.toml`: Package configuration file registering the `mini` CLI launch command.

### Environment: `aider-mini/.venv/`
Contains the **Python 3.14.3** virtual environment.

### Custom Sandbox: `aider-mini/mini/`
Contains all folders/files of **Aider Mini** in isolation while preserving the ability to import Aider utilities.
- `cli.py`: Aider Mini launch point, interactive CLI command loop.
- `project-brief.md`: Aider Mini project blueprint (this file).

### Prompt Generator Module: `aider-mini/mini/prompter`
**Aider Mini Eyes:** Copies context/prompts to the clipboard for sending to the LLM.
- `sys.py`: System Prompt Generator

## Development Roadmap

- **Phase 1:** Builds the *EYE > System Prompt Generator Module*.
- **Phase 2: Repository Prompter Module | `mini/repo.py`:** Responds to the `/repo` CLI command. Copies the repository prompt to the clipboard. Under development...
- **Phase 3: File Context Module (`mini/context.py`)**
    - Creates context from specified read-only files, e.g., coding conventions.
    - Autodetects focused/active editor files and assembles context from them.
- **Phase 4:** Builds the *Local File Editor Module*.
