# Aider Mini > Editor Module > Edit Executor
# Path: mini/editor/apply.py

from pathlib import Path

### apply edits function ###############################################################################################
def apply_edits(
    content_list: list[str],
    search_index: tuple[int,int],
    replace_list: list[str],
    target_path: Path
) -> dict[str,int|str]:
    """
    ### Disk Execution & Validation
    Applies diff edit blocks to modify file content and writes modified content to disk.
    #### Params:
    - *content_list:* target file content as list of lines.
    - *search_index:* start/stop lines of SEARCH block matched to target file content.
    - *replace_list:* replace block content as list of lines.
    - *target_path:* path to target file.
    #### Returns:
    - *dict:* status code and status message.
    """

    ### function init --------------------------------------------------------------------------------------------------

    ### invalid content list > returning error
    if (
        not isinstance(content_list, list)
        or not all(isinstance(line, str) for line in content_list)
        or any("\n" in line for line in content_list)
    ):
        return {
            "status": -1,
            "message": "Invalid Param: apply_edits(content_list)",
        }

    ### invalid search index > returning error
    if (
        not isinstance(search_index, tuple)
        or len(search_index) != 2
        or not all(isinstance(i, int) for i in search_index)
        or search_index[0] < 0
        or search_index[0] > search_index[1]
        or len(content_list) < search_index[1]
    ):
        return {
            "status": -1,
            "message": "Invalid Param: apply_edits(search_index)",
        }

    ### invalid replace list > returning error
    if (
        not isinstance(replace_list, list)
        or not all(isinstance(line, str) for line in replace_list)
        or any("\n" in line for line in replace_list)
    ):
        return {
            "status": -1,
            "message": "Invalid Param: apply_edits(replace_list)",
        }

    ### invalid target path > returning error
    if (
        not isinstance(target_path, Path)
        or not target_path.exists()
        or not target_path.is_file()
    ):
        return {
            "status": -1,
            "message": "Invalid Param: apply_edits(target_path)",
        }
    
    ### main logic -----------------------------------------------------------------------------------------------------

    ### applying changes to content list
    modified_content: list[str] = content_list[:]
    modified_content[search_index[0]:search_index[1]] = replace_list

    ### rebuilding raw file content from content list
    raw_content: str = "\n".join(modified_content) + "\n"

    ### writing raw file content to target file
    try:
        target_path.write_text(raw_content, encoding="utf-8", newline=None)
    except Exception as error:
        return {
            "status": -1,
            "message": f"File I/O Error: Failed to write to {target_path}: {error}",
        }
    
    ### function ends //////////////////////////////////////////////////////////////////////////////////////////////////

    ### returning success
    return {"status": 0, "message": "OK"}

### manual test block ##################################################################################################

if __name__ == "__main__":

    # target path
    target_path: Path = Path(__file__).parent / "testtest.py"

    # content list
    existing_lines: list[str] = target_path.read_text(encoding="utf-8").splitlines()

    # search index
    search_index: tuple[int,int] = (5, 8)
    
    # replace lines
    replace_list = []

    # running test
    print(f"Applying edits to {target_path.name}...")
    res = apply_edits(existing_lines, search_index, replace_list, target_path)

    # displaying returns
    print(f"Status: {res['status']} ({res['message']})")
