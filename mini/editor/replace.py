########################################################################################################################
### Aider Mini > File Editor Module > Replace Executor
### Path: mini/editor/replace.py
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
    Replaces SEARCH lines with REPLACE lines in the local file.
    #### Params:
    - *content_list* > local file content as list of lines
    - *search_index* > SEARCH block slice indices as tuple
    - *replace_list* > REPLACE block content as list of lines
    - *target_path* > path to local file as string
    #### Returns:
    - *dict* > status code, status message
    """

    ### function init --------------------------------------------------------------------------------------------------

    #>> content list is verified upstream
    #>> search index is verified upstream
    #>> replace list is verified upstream
    #>> target path is verified upstream

    ### converting target path str >>> path
    target_file: Path = Path(target_path)
    
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
