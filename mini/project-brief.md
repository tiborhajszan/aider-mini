# Aider Mini > Project Brief

## 1. Executive Summary & Core Motivation

- **Aider Mini** is a lightweight, modular CLI wrapper built alongside and within the Aider codebase. 
- While frontier LLMs (e.g., Claude 3.5 Sonnet, Gemini 1.5 Pro, GPT-4o) offer massive context windows and superior reasoning, using them via web interfaces creates major pain points:
   - **Blindness:** LLMs via web interfaces cannot natively read local repository structure or active editor files.
   - **Lack of Agency:** LLMs via web interfaces cannot write code modifications directly back to disk.
   - Blindness and Lack of Agency forces web interface users to do tedious copy-pasting of context and edits.
- Conversely, standard CLI AI agents (like original Aider) re-send thousands of tokens (system prompts, active files, repo maps, and history) on every single turn to accommodate stateless API models. This creates unnecessary token bloat and rigid workflows when working with stateful, large-context web interfaces.
- Aider Mini bridges this gap by splitting responsibilities into a **Modular Prompt/Context Generator** (Eyes) and an **Automated Disk Executor** (Hands), completely bypassing heavy API loops while giving web models exact local repository vision and editing capabilities.

## 2. Target Audience & Primary Use Case

- **Developer Persona:** Software engineers who prefer acessing high-performing frontier LLMs via web interfaces for interactive coding, architecture, and refactoring, but want full automation for context gathering and disk file edits.
- **Target Environment:** Local terminal (PowerShell / VS Code terminal) on Windows 11 / macOS / Linux, integrated directly into developer file-editing workflows.

## 3. Architectural Pillars

**Aider Mini** is structured around two main pillars:
<br><br>
```text
                          ┌─────────────────────────┐
                          │   AIDER-MINI ENGINE     │
                          └────────────┬────────────┘
                                       │
            ┌──────────────────────────┴──────────────────────────┐
            ▼                                                     ▼
  PILLAR 1: EYES (Context)                              PILLAR 2: HANDS (Code Edits)
  Modular On-Demand Prompt Generator                    Clipboard Listener & Disk Applier
  • System Prompt (/sys)                                • Reads response from clipboard
  • Read-Only Files (/read)                             • Parses SEARCH/REPLACE blocks
  • Tree-Sitter Repo Map (/map)                         • Validates line matching & diffs
  • Active File (/file)                                 • Applies changes directly to disk
```

## 4. Key Planned Features & CLI Commands

Instead of generating a massive, monolithic prompt on every interaction, **Aider Mini** features an **on-demand modular prompt pipeline**:
<br><br>
| Command | Feature | Description |
| :--- | :--- | :--- |
| `/sys` | **System Prompt Generator** | Copies a modern, non-bloated system instruction to the clipboard. Teaches the web model strictly to output `<<<<<<< SEARCH` ... `>>>>>>> REPLACE` diff blocks. |
| `/read` | **Read-Only File Context** | Reads workspace-level guidelines (e.g., `CONVENTIONS.md`) and formats them as read-only context on the clipboard. |
| `/map` | **Repo Map Generator** | Triggers Tree-Sitter symbol parsing over the codebase to generate a compact, bird's-eye graph of definitions and signatures. |
| `/file` | **Active File Context** | Automatically detects the currently active tab in VS Code (or specified files) and bundles its raw code with a user task. |
| `/apply` | **Disk Executor (Pillar 2)** | Listens to the system clipboard, extracts returned `SEARCH/REPLACE` blocks, and uses Aider's diff engine to edit files on disk instantly. |

## 5. Directory Structure & Technical Footprint

**Aider Mini** currently resides in the root directory of the forked **Aider** repository to maintain total isolation while preserving the ability to import battle-tested utilities (Tree-Sitter Repo Map, Diff Parsers, and local model connectors).
<br><br>
```text
aider-mini/ (Repository Root)
├── mini/                      # CLEAN CUSTOM SANDBOX
│   ├── __init__.py
│   ├── cli.py                 # Interactive CLI command loop (/sys, /read, /map, /file, /apply)
│   ├── sys_prompt.py          # Modular system prompt templates
│   ├── context.py             # Read-Only and active file context engine
│   ├── repomap.py             # Tree-Sitter repo map extractor wrapper
│   ├── editor.py              # Clipboard listener & SEARCH/REPLACE diff applier
│   └── project-brief.md       # Project brief & conversation reference
│
├── aider/                     # Original Aider codebase (dormant building blocks)
├── pyproject.toml             # Package config registering `mini` command
└── .venv/                     # Python virtual environment
```

## 6. Development Roadmap

- **Step 1: System Prompt Module (`mini/sys_prompt.py`)**
   - Builds modern system rules prompt, including `SEARCH/REPLACE` diff examples.
- **Step 2: File Context Module (`mini/context.py`)**
   - Creates context from specified read-only files, e.g., coding conventions.
   - Autodetects focused/active editor files and assembles context from them.
- **Step 3: Tree-Sitter Repo Map Wrapper (`mini/repomap.py`)**
   - Exposes Aider's Tree-Sitter repo map generator to a standalone `/map` CLI output.
- **Step 4: Clipboard Executor (`mini/editor.py`)**
   - Extracts Aider's `EditBlockCoder` parsing logic to apply clipboard diffs to local files.
