# Aider Mini > Project Brief

## Executive Summary & Core Motivation

- **Aider Mini** is a lightweight, modular CLI wrapper built alongside and within the Aider codebase. 
- While frontier LLMs (e.g., Claude 3.5 Sonnet, Gemini 1.5 Pro, GPT-4o) offer massive context windows and superior reasoning, using them via web interfaces creates major pain points:
    - **Blindness:** LLMs via web interfaces cannot natively read local repository structure or active editor files.
    - **Lack of Agency:** LLMs via web interfaces cannot write code modifications directly back to disk.
    - Blindness and Lack of Agency forces web interface users to do tedious copy-pasting of context and edits.
- Conversely, standard CLI AI agents (like original Aider) re-send thousands of tokens (system prompts, active files, repo maps, and history) on every single turn to accommodate stateless API models. This creates unnecessary token bloat and rigid workflows when working with stateful, large-context web interfaces.
- Aider Mini bridges this gap by splitting responsibilities into a **Modular Prompt/Context Generator** (Eyes) and an **Automated Disk Executor** (Hands), completely bypassing heavy API loops while giving web models exact local repository vision and editing capabilities.

## Target Audience & Primary Use Case

- **Developer Persona:** Software engineers who prefer acessing high-performing frontier LLMs via web interfaces for interactive coding, architecture, and refactoring, but want full automation for context gathering and disk file edits.
- **Target Environment:** Local terminal (PowerShell / VS Code terminal) on Windows 11 / macOS / Linux, integrated directly into developer file-editing workflows.

## Architectural Pillars

**Aider Mini** is structured around two main pillars:

### Pillar 1: EYES | Modular On-Demand Context/Prompt Generator
- System Prompt (`/sys`)
- Tree-Sitter Repository Map (`/map`)
- Read-Only Files (`/read`)
- Active File (`/file`)

### Pillar 2: HANDS | Clipboard Listener & File Editor
- Reads web model response from clipboard.
- Parses `SEARCH/REPLACE` blocks.
- Validates line matching and diffs.
- Applies changes directly to disk.

## Key Features & CLI Commands

Instead of generating a massive, monolithic prompt on every interaction, **Aider Mini** features an **on-demand modular prompt pipeline**:
<br><br>
| Command | Feature | Description |
| :--- | :--- | :--- |
| `/sys` | **System Prompt Generator** | Copies a modern, non-bloated system instruction to the clipboard. Teaches the web model strictly to output `<<<<<<< SEARCH` ... `>>>>>>> REPLACE` diff blocks. |
| `/map` | **Repository Map Generator** | Triggers Tree-Sitter symbol parsing over the codebase to generate a compact graph of definitions and signatures. |
| `/read` | **Read-Only File Context** | Reads specified files, e.g., coding conventions, and formats their content as read-only context on the clipboard. |
| `/file` | **Active File Context** | Automatically detects the currently active tab in VS Code (or specified files) and bundles its content as editable context on the clipboard. |
| `/apply` | **File Editor (Pillar 2)** | Listens to the system clipboard, extracts returned `SEARCH/REPLACE` blocks, and uses Aider's diff engine to edit files on disk instantly. |

## Directory Structure & Technical Footprint

**Aider Mini** currently resides in the root directory of the forked **Aider** repository to maintain total isolation while preserving the ability to import battle-tested utilities (Tree-Sitter Repo Map, Diff Parsers, and local model connectors).
<br><br>
```text
aider-mini/ (Repository Root)
├── mini/                      # CLEAN CUSTOM SANDBOX
│   ├── __init__.py
│   ├── cli.py                 # Interactive CLI command loop (/sys, /map, /read, /file, /apply)
│   ├── sys_prompt.py          # System Prompt generator
│   ├── repomap.py             # Tree-Sitter Repository Map extractor wrapper
│   ├── context.py             # Read-Only and Active File context engine
│   ├── prompts.py             # Prompt template repository
│   ├── editor.py              # Clipboard listener and SEARCH/REPLACE diff applier
│   └── project-brief.md       # Project Brief and conversation reference
│
├── aider/                     # Original Aider codebase (dormant building blocks)
├── pyproject.toml             # Package config registering `mini` command
└── .venv/                     # Python virtual environment
```

## Development Roadmap

- **Phase 1: System Prompt Module (`mini/sys_prompt.py`)**
    - Builds modern system rules prompt, including `SEARCH/REPLACE` diff examples.
- **Phase 2: Tree-Sitter Repository Map Wrapper (`mini/repomap.py`)**
    - Exposes Aider's Tree-Sitter Repository Map generator to a standalone `/map` CLI output.
- **Phase 3: File Context Module (`mini/context.py`)**
    - Creates context from specified read-only files, e.g., coding conventions.
    - Autodetects focused/active editor files and assembles context from them.
- **Phase 4: File Editor (`mini/editor.py`)**
    - Extracts Aider's `EditBlockCoder` parsing logic to apply clipboard edits to local files.

## **Summary: Line-by-Line Stateful Parser Strategy**

* **Core Approach:** Replace the monolithic regex with a deterministic State Machine that parses payload line-by-line (`EXPECTING_FENCE` $\rightarrow$ `EXPECTING_PATH` $\rightarrow$ `EXPECTING_SEARCH` $\rightarrow$ `READING_SEARCH` $\rightarrow$ `READING_REPLACE` $\rightarrow$ `EXPECTING_CLOSING_FENCE`).
* **Strict Boundaries:** Shell markers (fences, path line, `<SEARCH`, `>REPLACE`) must strictly adhere to exact specifications. Any violation halts parsing immediately, returning a detailed error message for LLM retry/reprompting.
* **Raw Payload Integrity:** Code lines within `SEARCH` and `REPLACE` blocks are captured completely untouched into lists—preserving 100% of relative indentation, whitespace, and empty lines.
* **Line Ending Normalization:** Pre-process the payload at entry with `.replace("\r\n", "\n").split("\n")` to ensure OS-agnostic comparisons without stripping internal empty lines or trailing structural breaks.
