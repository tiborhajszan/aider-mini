########################################################################################################################
### Aider Mini > File Editor Module > Diff Edit Executor
### Path: aider-mini/mini/editor/replace.py
########################################################################################################################

from pathlib import Path

### apply edits function ###############################################################################################
def apply_edits(
    content_list: list[str],
    search_index: tuple[int,int],
    replace_list: list[str],
    target_path: str
) -> dict[str, int | str]:
    """
    Applies the `REPLACE` block content to modify target lines in the local file.
    #### Params:
    - *content_list* > target file content as list of lines
    - *search_index* > SEARCH block slice indices as tuple
    - *replace_list* > REPLACE block content as list of lines
    - *target_path* > path to local target file as string
    #### Returns:
    - *dict* > status code, status message
    """

    ### function init --------------------------------------------------------------------------------------------------

    ### invalid content list > returning error payload
    if (
        not isinstance(content_list, list)
        or not all(isinstance(line, str) for line in content_list)
    ):
        return {"status": -1, "message": "Invalid Param > apply_edits(content_list)"}

    ### invalid search index > returning error payload
    if (
        not isinstance(search_index, tuple)
        or len(search_index) != 2
        or not all(isinstance(item, int) and not isinstance(item, bool) for item in search_index)
        or search_index[0] < 0
        or search_index[0] > search_index[1]
        or len(content_list) < search_index[1]
    ):
        return {"status": -1, "message": "Invalid Param > apply_edits(search_index)"}

    ### invalid replace list > returning error payload
    if (
        not isinstance(replace_list, list)
        or not all(isinstance(line, str) for line in replace_list)
    ):
        return {"status": -1, "message": "Invalid Param > apply_edits(replace_list)"}

    ### invalid target path > returning error payload
    if (
        not isinstance(target_path, str)
        or not target_path.strip()
    ):
        return {"status": -1, "message": "Invalid Param > apply_edits(target_path)"}

    ### invalid target file > returning error payload
    target_file: Path = Path(target_path)
    if not target_file.is_file():
        return {"status": -1, "message": "Invalid Param > apply_edits(target_path)"}
    
    ### function main logic --------------------------------------------------------------------------------------------

    ### copying content list | applying changes
    modified_content: list[str] = content_list[:]
    modified_content[search_index[0]:search_index[1]] = replace_list

    ### rebuilding raw file content
    raw_content: str = "\n".join(modified_content) + "\n" if modified_content else ""

    ### writing to target file | handling file write errors
    try:
        target_file.write_text(data=raw_content, encoding="utf-8", newline=None)
    except Exception as error:
        return {"status": -1, "message": f"File Write Failure > {target_path}:\n{error}"}
    
    ### function ends //////////////////////////////////////////////////////////////////////////////////////////////////

    ### returning success payload
    return {"status": 0, "message": "OK"}

### manual testing block ###############################################################################################
if __name__ == "__main__":
    print("\n[!] Diff Edit Executor > No Test Specified\n")
