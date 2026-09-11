########################################################################################################################
### Aider Mini > Local File Editor > Response Parser
### Path: mini/editor/response_parser.py
########################################################################################################################

import re

### response parser function ###########################################################################################
def response_parser(clipboard_list: list[str]) -> dict[str, int | str | list[str] | list[str]]:
    """
    Parses the LLM response to isolate the SEARCH/REPLACE block.
    #### Params:
    - *clipboard_list* > clipboard content as list of lines
    #### Returns:
    - *dict* > status code, status message, SEARCH block content, REPLACE block content
    """

    ### function init --------------------------------------------------------------------------------------------------

    #>> clipboard list is verified upstream

    ### error payload helper
    def error_payload(message: str) -> dict[str, int | str | list[str] | list[str]]:
        return {"status": -1, "message": message, "search": [], "replace": []}

    ### parsing loop ---------------------------------------------------------------------------------------------------

    ### loop init
    parsing_state: int = 1
    search_list: list[str] = []
    replace_list: list[str] = []

    ### iterating clipboard list
    for line in clipboard_list:

        ## discarding lines until search marker found
        if parsing_state == 1:
            if re.match(r"^<{5,9}\sSEARCH$", line):
                parsing_state = 2
                continue
            else:
                continue

        ## recording search block content until divider marker found
        if parsing_state == 2:
            if re.match(r"^={5,9}$", line):
                parsing_state = 3
                continue
            else:
                search_list.append(line)
                continue

        ## recording replace block content until replace marker found
        if parsing_state == 3:
            if re.match(r"^>{5,9}\sREPLACE$", line):
                parsing_state = 4
                break
            else:
                replace_list.append(line)
                continue

    ### parsing outcome returns ----------------------------------------------------------------------------------------

    ### matching parsing state
    match parsing_state:

        ## returning parsing errors
        case 1:
            return error_payload(message="Parsing Failure > SEARCH/REPLACE Block Not Found")
        case 2:
            return error_payload(message="Parsing Failure > DIVIDER Marker Not Found")
        case 3:
            return error_payload(message="Parsing Failure > REPLACE Marker Not Found")

        ## returning parsing success
        case 4:
            return {"status": 0, "message": "OK", "search": search_list, "replace": replace_list}

        ## returning state error
        case default_val:
            return error_payload(message=f"Parsing Failure > Unknown Parsing State > {default_val}")
        
### manual testing block ###############################################################################################
if __name__ == "__main__":
    print("\n[!] Response Parser > No Test Specified\n")
