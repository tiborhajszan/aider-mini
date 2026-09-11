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

    ### payload helpers ------------------------------------------------------------------------------------------------

    ### error payload
    def make_error(message: str) -> dict[str,int|str|list[str]|list[str]]:
        return {"status": -1, "message": message, "search": [], "replace": []}

    ### function init --------------------------------------------------------------------------------------------------

    ### invalid clipboard list > returning error payload
    if (
        not isinstance(clipboard_list, list)
        or not all(isinstance(line, str) for line in clipboard_list)
        or any("\n" in line for line in clipboard_list)
    ):
        return make_error(message="Invalid Param: parse_edit_blocks(clipboard_list)")

    ### function main logic --------------------------------------------------------------------------------------------

    ### insufficient length of clipboard list > returning error payload
    if len(clipboard_list) <= 3:
        return make_error(message="Parsing Failure: Insufficient clipboard content")

    ### loop init
    parsing_status: int = 1
    search_list: list[str] = []
    replace_list: list[str] = []

    ### iterating clipboard list
    for line in clipboard_list:

        #>> discarding lines until search marker found
        if parsing_status == 1:
            if re.match(r"^<{5,9}\sSEARCH$", line): parsing_status = 2
            continue

        #>> recording search block content until divider marker found
        if parsing_status == 2:
            if re.match(r"^={5,9}$", line): parsing_status = 3; continue
            search_list.append(line); continue

        #>> recording replace block content until replace marker found
        if parsing_status == 3:
            if re.match(r"^>{5,9}\sREPLACE$", line): parsing_status = 4; break
            replace_list.append(line); continue

    ### function ends //////////////////////////////////////////////////////////////////////////////////////////////////

    ### handling parsing status
    match parsing_status:

        #>> handling parsing error
        case 1: return make_error(message="Parsing Failure: SEARCH/REPLACE block not found")
        case 2: return make_error(message="Parsing Failure: DIVIDER marker not found")
        case 3: return make_error(message="Parsing Failure: REPLACE marker not found")

        #>> handling parsing success
        case 4: return {
            "status": 0,
            "message": "OK",
            "search": search_list,
            "replace": replace_list,
        }

        #>> handling status error
        case default_val: return make_error(message=f"Parsing Failure: parsing state = {default_val} (unknown)")
        
### manual testing block ###############################################################################################
if __name__ == "__main__":

    print("\n[!] Running in Test Mode...\n")

    clipboard_list: list[str] = [
        "```python",
        "src/utils/calculator.py",
        "<<<<<<< SEARCH",
        "def add(a: int, b: int) -> int:",
        "=======",
        "def add(a: int, b: int) -> int:",
        "    return a + b",
        ">>>>>>> REPLACE",
        "```"
    ]

    return_dict = parse_edit_blocks(clipboard_list=clipboard_list)

    print("Status:")
    print(return_dict["status"], return_dict["message"])
    print()

    print("SEARCH block:")
    for line in return_dict["search"]: print(line)
    print()

    print("REPLACE block:")
    for line in return_dict["replace"]: print(line)
    print()
