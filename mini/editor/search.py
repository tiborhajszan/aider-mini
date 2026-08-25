# Aider Mini > Editor Module > Search Engine
# Path: mini/editor/search.py

from pathlib import Path

def match_search_block(
    target_path: Path,
    active_path: Path,
    search_block: str,
) -> dict[str, int|str|Path|tuple[int,int]]:
    """
    ### File & Search Block Matching Engine
    - Creates/Loads target local file.
    - Matches SEARCH block to target file.
    - Matching allows for formatting variations.
    - Returns structured payload dictionary (status, message, target path, slice indices).
    """
    # -------------------------------------------------------------------------
    # Filepath Resolution & Scenario Validation (using pathlib)
    # -------------------------------------------------------------------------
    # Scenario 1: Existing Active File Edit
    # - Verify target_path matches active_path (via target_path.resolve() ==
    #   active_path.resolve() or target_path.name == active_path.name).
    # - Confirm target_path exists on disk and read file content directly from target_path.
    # - Reject execution if target_path points to a different existing file on disk.
    # Scenario 2: New File Creation
    # - Check if not target_path.exists().
    # - Treat as a file creation request and bypass SEARCH block disk matching:
    #   -> Return {"status": 201, "target_path": target_path, "indices": (0, 0), "message": "NEW_FILE"}
    # -------------------------------------------------------------------------

    # resolving target path > resolving active path
    resolved_target: Path = target_path.resolve()
    resolved_active: Path = active_path.resolve()

    # Verify target matches the active file
    is_active_match = (resolved_target == resolved_active) or (
        target_path.name == active_path.name
    )

    if not is_active_match:
        return {
            "status": 403,
            "error": "TARGET_FILE_MISMATCH",
            "message": f"Target file '{target_path}' differs from active file '{active_path}'.",
        }

    # Confirm file exists on disk and read content directly from target_path
    if not target_path.exists():
        return {
            "status": 404,
            "error": "FILE_NOT_FOUND",
            "message": f"Active file '{target_path}' does not exist on disk.",
        }

    try:
        file_content = target_path.read_text(encoding="utf-8")
    except Exception as e:
        return {
            "status": 500,
            "error": "FILE_READ_ERROR",
            "message": f"Failed to read file '{target_path}': {e}",
        }

    # -------------------------------------------------------------------------
    # Search Block Text Matching (Tiers 1-3 pending)
    # -------------------------------------------------------------------------

    return {
        "status": 200,
        "target_path": resolved_target,
        "indices": (-1, -1),
        "message": "SEARCH_PENDING",
    }