########################################################################################################################
### Aider Mini > Local File Editor > Response Parser
### Path: mini/editor/response_parser.py
########################################################################################################################

import re

### response parser function ###########################################################################################
def response_parser(clipboard_lines: list[str]) -> dict[str, int | str | int | int | int]:
    """
    Parses the LLM response to locate the SEARCH/REPLACE markers.
    #### Params:
    - *clipboard_lines* > clipboard content as list of lines
    #### Returns:
    - *dict* > status code, status message, SEARCH index, DIVIDER index, REPLACE index
    """

    ### function init --------------------------------------------------------------------------------------------------

    #>> clipboard lines param is verified upstream

    ### indices init
    search_indices: list[int] = []
    divider_indices: list[int] = []
    replace_indices: list[int] = []

    ### parsing loop ---------------------------------------------------------------------------------------------------

    ### iterating clipboard list
    for index,line in enumerate(clipboard_lines):

        ## looking for search marker
        if re.match(r"^<{5,9}\sSEARCH$", line):
            search_indices.append(index)

        ## looking for divider marker
        elif re.match(r"^={5,9}$", line):
            divider_indices.append(index)

        ## looking for replace marker
        elif re.match(r"^>{5,9}\sREPLACE$", line):
            replace_indices.append(index)

        ## no markers > continue
        else:
            continue

    ### validations and returns ----------------------------------------------------------------------------------------

    ### invalid indices > returning error payload
    if (
        len(search_indices) != 1
        or len(divider_indices) != 1
        or len(replace_indices) != 1
        or divider_indices[0] < search_indices[0]
        or replace_indices[0] < divider_indices[0]
    ):
        return {
            "status": -1, "message": "Parsing Failure > SEARCH/REPLACE Marker(s) Error",
            "search": search_indices, "divider": divider_indices, "replace": replace_indices
        }

    ### valid indices > returning success payload
    else:
        return {
            "status": 0, "message": "Parsing Success",
            "search": search_indices[0], "divider": divider_indices[0], "replace": replace_indices[0]
        }

### manual testing block ###############################################################################################
if __name__ == "__main__":

    clipboard_lines: list[str] = [
        "<<<<<<< SEARCH",
        "def add(a, b):",
        "    return a + b",
        "=======",
        "def add (a, b, c):",
        "    return a + b + c",
        ">>>>>>> REPLACE",
    ]

    parser_response: dict = response_parser(clipboard_lines=clipboard_lines)

    print()
    print(parser_response)
    print()
