# Aider Mini > File Editor Module > Clipboard Parser
# Path: mini/editor/parser.py

import re

def parse_edit_blocks(raw_text: str) -> dict[str, str]:
    """
    ### SEARCH/REPLACE Block Parsing
    - Parses raw clipboard payload using regex patterns derived from Aider's `EditBlockCoder`.
    - Extracts target file path, SEARCH code block, and REPLACE code block.
    - Converts extracted information into a structured data object.
    """

    # empty clipboard or invalid payload > error message > returning empty dict
    if not isinstance(raw_text, str) or not raw_text.strip():
        print("[!] Editor Parsing Error: Clipboard is empty or contains invalid payload.\n")
        return {}

    # defining regex search pattern (diff-fenced format)
    regex_pattern: re.Pattern[str] = re.compile(
        r"^[ \t]*```[a-zA-Z0-9_-]*[ \t]*\r?\n"  # opening fence line (allows leading/trailing spaces + CRLF)
        r"[ \t]*(?P<path>[^\r\n]+?)[ \t]*\r?\n"  # filepath line inside the fence
        r"^[ \t]*<{5,9}\s*SEARCH\s*>?\s*\r?\n"   # SEARCH marker
        r"(?P<search>[\s\S]*?)"                 # SEARCH block content
        r"^[ \t]*={5,9}\s*\r?\n"                # DIVIDER marker
        r"(?P<replace>[\s\S]*?)"                # REPLACE block content
        r"^[ \t]*>{5,9}\s*REPLACE\s*\r?\n"      # REPLACE marker
        r"^[ \t]*```[ \t]*$",                   # closing fence line (allows leading/trailing spaces)
        re.MULTILINE
    )
    # extracting edit block
    edit_block: re.Match[str] | None = regex_pattern.search(raw_text)
    if not edit_block:
        print("[!] Editor Parsing Error: No valid SEARCH/REPLACE block was found on the clipboard.\n")
        return {}

    # building dictionary > returning
    return {
        "path": edit_block.group("path").strip(),
        "search": edit_block.group("search"),
        "replace": edit_block.group("replace"),
    }

if __name__ == "__main__":
    print("\n[!] Running in Test Mode...\n")
    raw_text: str = """
    ```python
    src/utils/calculator.py
    <<<<<<< SEARCH
    def add(a: int, b: int) -> int:
        return a + b
    =======
    def add(a: int, b: int) -> int:
        c = a + b
        return c
    >>>>>>> REPLACE
    ```
    """
    print(raw_text)
    return_dict: dict[str,str] = parse_edit_blocks(raw_text=raw_text)
    print(return_dict, "\n")
