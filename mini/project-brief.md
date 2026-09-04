# Aider Mini > Project Brief

Aider Mini is a lightweight CLI coding assistant based on and built alongside the forked Aider codebase. It is intended primarily for the personal use of its developer.

## Core Motivation

- **Limitations of Web Interfaces:** While frontier LLMs used via stateful web interfaces offer massive context windows and superior reasoning, the web interface itself has major limitations. *Blindness:* Web interfaces do not allow frontier LLMs to read repository structure and local files. *Lack of Agency:* Web interfaces do not allow frontier LLMs to write code modifications directly back to local files. *Copy/Pasting:* The limitations of web interfaces force users to perform tedious copy/pasting of context and edits.
- **Limitations of APIs:** LLMs used via standard CLI and stateless API interfaces (like original Aider) re-send thousands of tokens (system prompts, repo maps, active files, and chat history) on every single turn, creating unnecessary *token bloat* and *rigid workflows*.
- **Aider Mini** bridges this gap by aiding the user in exploiting the full potential of stateful web interfaces while avoiding the heavy prompting via stateless APIs. Aider Mini automates prompting (*Prompt/Context Generator*, Eyes), applies LLM edit instructions to local files (*File Editor*, Right Hand) and executes CLI commands requested by the LLM (*CLI Executor*, Left Hand).

## Target Audience & Primary Use Case

- **Developer Persona:** Software engineers who prefer acessing high-performing frontier LLMs via web interfaces for interactive coding, architecture, and refactoring, but want full automation for context gathering and disk file edits.
- **Target Environment:** Local terminal (PowerShell / VS Code terminal) on Windows 11 / macOS / Linux, integrated directly into developer file-editing workflows.

## Architectural Pillars

**Aider Mini** is structured around three main pillars:

### Pillar 1: EYES | Modular On-Demand Context/Prompt Generator
- **System Prompt Generator (`/sys`):** Copies the *system prompt* to the clipboard that teaches the LLM how to assist the user and how to output `SEARCH/REPLACE` diff edit blocks.
- **Repository Prompt Generator (`/repo`):** Copies the *repository prompt* to the clipboard that tells the LLM how to access the project repository and where to find general project context.
- **Active File Selector (`/file`):** Copies the *active file prompt* to the clipboard with instructions for the LLM on which file to edit and how to retrieve its current contents.

### Pillar 2: RIGHT HAND | File Editor (`/apply`)
- Reads web model response from the clipboard.
- Parses `SEARCH/REPLACE` diff edit blocks.
- Matches `SEARCH` block content to local target files.
- Applies diff edit blocks to modify content of local target files.

### Pillar 3: LEFT HAND | Command Line Executor

## Key Features & CLI Commands

Instead of generating a massive, monolithic prompt on every interaction, **Aider Mini** features an **on-demand modular prompt pipeline**:
<br><br>
| Command | Feature | Description |
| :--- | :--- | :--- |
| `/file` | **Active File Context** | Automatically detects the currently active tab in VS Code (or specified files) and bundles its content as editable context on the clipboard. |

## Directory Structure & Technical Footprint

### Project Root: `aider-mini/`
Contains all folders/files of the forked **Aider** repository.
- `markdown.css`: Stylesheet for Vs Code markdown viewer.
- `pyproject.toml`: Package configuration file registering the `mini` CLI launch command.

### Environment: `aider-mini/.venv/`
Contains the Python 3.14.3 virtual environment.

### Custom Sandbox: `aider-mini/mini/`
Contains all folders/files of **Aider Mini** in isolation while preserving the ability to import battle-tested **Aider** utilities (Tree-Sitter Repo Map, Diff Parsers, and local model connectors).
- `cli.py`: **Aider Mini** launch point, interactive CLI command loop.
- `project-brief.md`: **Aider Mini** project blueprint (this file).

### Editor Module: `aider-mini/mini/editor/`
**Aider Mini Right Hand:** Applies web model edit instructions to local files.
- `editor.py`: Module launch point and workflow orchestrator.
- `parser.py`: Model response parser that isolates `SEARCH/REPLACE` diff edit blocks.
- `search.py`: Search engine matching `SEARCH` block content to local target files.
- `apply.py` : Diff edit executor that modifies and writes content to local target files.

## Development Roadmap

- **Phase 1: System Prompt Module (`mini/sys_prompt.py`)**
    - Builds modern system rules prompt, including `SEARCH/REPLACE` diff examples.
- **Phase 2: Repository Prompter Module | `mini/repo.py`:** Responds to the `/repo` CLI command. Copies the repository prompt to the clipboard. Under development...
- **Phase 3: File Context Module (`mini/context.py`)**
    - Creates context from specified read-only files, e.g., coding conventions.
    - Autodetects focused/active editor files and assembles context from them.
- **Phase 4: Editor Module (`aider-mini/mini/editor/*`):** Responds to the `/apply` CLI command. Extracts LLM resposes from the clipboard. Parses LLM responses to isolate `SEARCH/REPLACE` diff edit blocks. Matches `SEARCH` block contents to local target files. Applies diff edit blocks to modify local target files.
