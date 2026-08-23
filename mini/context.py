import argparse
import json
import platform
import shlex
from pathlib import Path

class ContextEngine:
    """Handles parsing active file paths/selections and building plain-text clipboard payloads."""

    def __init__(self, workspace_root: str = "."):
        self.workspace_root = Path(workspace_root).resolve()

    def read_file_content(self, file_path: Path) -> str:
        """Reads file content safely with UTF-8 encoding."""
        try:
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                return f.read()
        except Exception as e:
            return f"[Error reading file {file_path}: {e}]"

    def format_plain_text(self, file_path: Path, selection: str | None = None) -> str:
        """Formats file content and selection into a clean plain-text payload with text banners."""
        try:
            rel_path = file_path.relative_to(self.workspace_root)
        except ValueError:
            rel_path = file_path

        content = self.read_file_content(file_path)
        divider = "=" * 80
        blocks = []

        if selection and selection.strip():
            blocks.append(f"{divider}\nFOCUSED SELECTION: {rel_path}\n{divider}\n{selection.strip()}\n")

        blocks.append(f"{divider}\nFILE: {rel_path}\n{divider}\n{content}")

        return "\n\n".join(blocks)

    def handle_file_command(self, raw_args: str) -> tuple[str, str | None]:
        """
        Parses incoming /file arguments.
        Returns: tuple(formatted_payload_or_error, relative_file_path_display)
        """
        parser = argparse.ArgumentParser(prog="/file", add_help=False)
        parser.add_argument("path", type=str, nargs="?", default=None)
        parser.add_argument("--selection", type=str, default=None)

        try:
            args_list = shlex.split(raw_args)
            parsed, _ = parser.parse_known_args(args_list)
        except Exception as e:
            return f"Error parsing arguments: {e}", None

        if not parsed.path:
            return "Error: No file path provided. Usage: /file <path> [--selection <text>]", None

        target_path = Path(parsed.path).resolve()
        if not target_path.exists():
            return f"Error: File not found - {parsed.path}", None

        try:
            display_name = str(target_path.relative_to(self.workspace_root))
        except ValueError:
            display_name = target_path.name

        payload = self.format_plain_text(target_path, parsed.selection)
        return payload, display_name


def ensure_vscode_keybinding_configured() -> bool:
    """
    Ensures VS Code's global user keybindings.json contains the Ctrl+Alt+F shortcut.
    Operates strictly in user settings (zero project folder litter).
    """
    system = platform.system()
    if system == "Windows":
        user_dir = Path.home() / "AppData" / "Roaming" / "Code" / "User"
        key_combo = "ctrl+alt+f"
    elif system == "Darwin":  # macOS
        user_dir = Path.home() / "Library" / "Application Support" / "Code" / "User"
        key_combo = "cmd+alt+f"
    else:  # Linux
        user_dir = Path.home() / ".config" / "Code" / "User"
        key_combo = "ctrl+alt+f"

    keybindings_file = user_dir / "keybindings.json"
    binding_entry = {
        "key": key_combo,
        "command": "workbench.action.terminal.sendSequence",
        "args": {
            "text": "/file \"${file}\" --selection \"${selectedText}\"\u000d"
        },
        "when": "editorTextFocus"
    }

    user_dir.mkdir(parents=True, exist_ok=True)
    keybindings: list[dict[str,any]] = []

    if keybindings_file.exists():
        try:
            with open(keybindings_file, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    keybindings = json.loads(content)
        except Exception:
            keybindings = []

    # Prevent duplicate injection
    for entry in keybindings:
        if (entry.get("command") == "workbench.action.terminal.sendSequence" and 
            "/file" in entry.get("args", {}).get("text", "")):
            return False

    keybindings.append(binding_entry)
    with open(keybindings_file, "w", encoding="utf-8") as f:
        json.dump(keybindings, f, indent=2)

    return True