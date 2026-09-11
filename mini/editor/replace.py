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
    local_path: str
) -> dict[str, int | str]:
    """
    Replaces SEARCH lines with REPLACE lines in the local file.
    #### Params:
    - *content_list* > local file content as list of lines
    - *search_index* > SEARCH block slice indices as tuple
    - *replace_list* > REPLACE block content as list of lines
    - *local_path* > path to local file as string
    #### Returns:
    - *dict* > status code, status message
    """

    ### function init --------------------------------------------------------------------------------------------------

    #>> content list is verified upstream
    #>> search index is verified upstream
    #>> replace list is verified upstream
    #>> local path is verified upstream

    ### converting local path str >>> path
    local_file: Path = Path(local_path)
    
    ### function main logic --------------------------------------------------------------------------------------------

    ### copying content list | executing lines replace
    modified_content: list[str] = content_list[:]
    modified_content[search_index[0]:search_index[1]] = replace_list

    ### rebuilding raw file content
    raw_content: str = "\n".join(modified_content) + "\n" if modified_content else ""

    ### writing local file | handling file writing errors
    try:
        local_file.write_text(data=raw_content, encoding="utf-8", newline=None)
    except Exception as error:
        return {"status": -1, "message": f"File Writing Failure > {local_path}:\n{error}"}
    
    ### function ends //////////////////////////////////////////////////////////////////////////////////////////////////

    ### returning success payload
    return {"status": 0, "message": "OK"}

### manual testing block ###############################################################################################
if __name__ == "__main__":
    print("\n[!] Replace Executor > No Test Specified\n")
