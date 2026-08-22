from pathlib import Path
import pyperclip
from aider.repomap import RepoMap
from aider.io import InputOutput

class NoOpModel:
    """Lightweight stub to satisfy Aider's internal RepoMap requirements
    without loading tokenizers or making API calls.
    """
    def token_count(self, text):
        return len(text) // 4  # Fast, crude character-to-token approximation

    def get_token_limit(self):
        return 1000000

def collect_repository_files(root_dir: Path) -> list[str]:
    """Collects repository files while excluding build artifacts, virtual environments,
    and binary noise, preserving unignored configs and untracked scripts.
    """
    ignored_dirs = {
        ".venv", "venv", "env", "__pycache__", ".git", 
        ".pytest_cache", "node_modules", "build", "dist", ".idea", ".vscode"
    }
    ignored_exts = {
        ".pyc", ".pyo", ".pyd", ".so", ".dll", ".exe", 
        ".bin", ".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip", ".tar", ".gz"
    }

    valid_files = []
    for path in root_dir.rglob("*"):
        if path.is_file():
            rel_parts = path.relative_to(root_dir).parts
            
            # Skip noise directories
            if any(part in ignored_dirs for part in rel_parts):
                continue
            # Skip hidden folders (allow root dotfiles like .env.example)
            if any(part.startswith('.') and part not in {'.env', '.env.example'} for part in rel_parts[:-1]):
                continue
            # Skip binary and non-text formats
            if path.suffix.lower() in ignored_exts:
                continue

            valid_files.append(str(path))
            
    return valid_files

def generate_repo_map(root_path=".", max_tokens=2000, focus_files=None, copy_to_clipboard=True) -> str:
    """Generates a compressed Tree-Sitter repository map using core Aider modules.
    
    Args:
        root_path: Root path of the codebase.
        max_tokens: Token budget for the map output (default: 2000 for global, 1000 for file-focused).
        focus_files: List of file path strings to act as PageRank seed nodes (e.g., active files).
        copy_to_clipboard: Whether to automatically copy the resulting map text to clipboard.
    """
    root_dir = Path(root_path).resolve()
    io = InputOutput(yes=True)
    dummy_model = NoOpModel()

    repo_map = RepoMap(
        map_tokens=max_tokens,
        root=str(root_dir),
        main_model=dummy_model,
        io=io
    )

    all_files = collect_repository_files(root_dir)

    # Format focus files for Aider RepoMap seed node processing
    chat_files = []
    if focus_files:
        chat_files = [str(Path(f).resolve()) for f in focus_files if Path(f).exists()]

    # Generate AST signatures via Tree-Sitter with PageRank compression
    map_text = repo_map.get_repo_map(chat_files=chat_files, other_files=all_files)

    if map_text:
        # File backup fallback
        output_file = root_dir / "mini" / "repomap.txt"
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(map_text, encoding="utf-8")

        if copy_to_clipboard:
            pyperclip.copy(map_text)
            print(f"\n[✓] Repository map (~{max_tokens} token budget) copied to clipboard & dumped to: {output_file}\n")
    else:
        print("\n[!] Repository map generation returned no output.\n")

    return map_text or ""

def get_global_map(root_path=".", max_tokens=2000) -> str:
    """Helper for /sys or standalone /map: Generates a bird's-eye global repository map."""
    return generate_repo_map(root_path=root_path, max_tokens=max_tokens, focus_files=None)

def get_focused_map(focus_files: list[str], root_path=".", max_tokens=1000) -> str:
    """Helper for /file: Generates a 1k token repository map tailored specifically to active workspace files."""
    return generate_repo_map(root_path=root_path, max_tokens=max_tokens, focus_files=focus_files)

if __name__ == "__main__":
    generate_repo_map()