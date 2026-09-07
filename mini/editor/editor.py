########################################################################################################################
### Aider Mini > File Editor Module > Edit Orchestrator
### Path: mini/editor/editor.py
########################################################################################################################

import pyperclip
from pathlib import Path
from . import parser, search, apply

### run editor function ################################################################################################
def run_editor(target_path: str = "") -> dict[str, int | str]:
    """
    Reads the LLM response from clipboard and orchestrates the file edit pipeline.
    #### Params:
    - *target_path* > path to local target file as string
    #### Returns:
    - *dict* > status code, status message
    """

    ### function init --------------------------------------------------------------------------------------------------

    ### invalid target path > returning error payload
    if (
        not isinstance(target_path, str)
        or not target_path.strip()
    ):
        return {"status": -1, "message": "[!] File Editor > Invalid Param > run_editor(target_path)"}

    ### invalid target file > returning error payload
    target_file: Path = Path(target_path)
    if not target_file.is_file():
        return {"status": -1, "message": "[!] File Editor > Invalid Param > run_editor(target_path)"}

    ### retrieving llm response from clipboard -------------------------------------------------------------------------

    ### reading clipboard content > handling clipboard errors
    try:
        clipboard_content: str = pyperclip.paste()
    except Exception as error:
        return {"status": -1, "message": f"[!] File Editor > Clipboard Error:\n{error}"}

    ### invalid clipboard content > returning error payload
    if (
        not clipboard_content
        or not isinstance(clipboard_content, str)
        or not clipboard_content.strip()
    ):
        return {"status": -1, "message": "[!] File Editor > Invalid Clipboard Content"}

    ### creating clipboard line list
    clipboard_list: list[str] = clipboard_content.splitlines()

    ### retrieving target file content ---------------------------------------------------------------------------------

    ### reading target file content > handling file read errors
    try:
        file_content: str = target_file.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        return {"status": -1, "message": f"[!] File Editor > File Read Error > {target_path}:\n{error}"}
    
    ### creating content line list
    content_list: list[str] = file_content.splitlines()
    
    ### applying llm edit to local file --------------------------------------------------------------------------------

    ### parsing llm response > handling parsing errors
    parsing_response: dict = parser.parse_edit_blocks(clipboard_list=clipboard_list)
    if parsing_response["status"] != 0:
        return {"status": -1, "message": f"[!] File Editor > {parsing_response['message']}"}

    ### matching search block content > handling search errors
    search_response: dict = search.match_search_block(
        content_list=content_list,
        search_list=parsing_response["search"]
    )
    if search_response["status"] != 0:
        return {"status": -1, "message": f"[!] File Editor > {search_response['message']}"}

    ### applying llm edit instructions > handling execution errors
    apply_response: dict = apply.apply_edits(
        content_list=content_list,
        search_index=search_response["indices"],
        replace_list=parsing_response["replace"],
        target_path=str(target_file)
    )
    if apply_response["status"] != 0:
        return {"status": -1, "message": f"[!] File Editor > {apply_response['message']}"}

    ### clearing clipboard
    pyperclip.copy("")

    ### function ends //////////////////////////////////////////////////////////////////////////////////////////////////

    ### returning success payload
    return {"status": 0, "message": "OK"}

### manual testing block ###############################################################################################
if __name__ == "__main__":
    print("\n[!] Edit Orchestrator > No Test Specified\n")
