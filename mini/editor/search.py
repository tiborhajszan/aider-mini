### Aider Mini > Editor Module > Search Engine
### Path: mini/editor/search.py

### match search block function ########################################################################################
def match_search_block(
    content_list: list[str],
    search_list: list[str],
) -> dict[str,int|str|tuple[int,int]]:
    """
    ### Search Block Matching Engine
    Matches SEARCH block contents to local target file.
    #### Params:
    - *content_list* > target file content as list of lines
    - *search_list* > SEARCH block content as list of lines
    #### Returns:
    - *dict* > status code, status message, slice indices
    """

    ### payload helpers ------------------------------------------------------------------------------------------------

    ### error payload
    def make_error(message: str) -> dict[str,int|str|tuple[int, int]]:
        return {"status": -1, "message": message, "indices": (-1, -1),}

    ### success payload
    def make_success(indices: tuple[int,int]) -> dict[str,int|str|tuple[int,int]]:
        return {"status": 0, "message": "OK", "indices": indices,}

    ### function init --------------------------------------------------------------------------------------------------

    ### invalid content list >> returning error payload
    if (
        not isinstance(content_list, list)
        or not all(isinstance(line, str) for line in content_list)
        or any("\n" in line for line in content_list)
    ):
        return make_error(message="Invalid Param: match_search_block(content_list)")
    
    ### invalid search list >> returning error payload
    if (
        not isinstance(search_list, list)
        or not all(isinstance(line, str) for line in search_list)
        or any("\n" in line for line in search_list)
    ):
        return make_error(message="Invalid Param: match_search_block(search_list)")
    
    ### function main logic --------------------------------------------------------------------------------------------

    ### search block is longer than target content >> returning error payload
    if len(content_list) < len(search_list):
        return make_error(message="Matching Failure: SEARCH block is longer than target content")

    ### empty search_list >> returning success (0, 0) payload
    if not search_list:
        return make_success(indices=(0, 0))
    
    ### sliding window matching algorithm >> returning success (start, end) payload
    for content_index in range(len(content_list) - len(search_list) + 1):
        if all(
            content_list[content_index + search_index].strip() == search_list[search_index].strip()
            for search_index in range(len(search_list))
        ):
            return make_success(indices=(content_index, content_index + len(search_list)))
        
    ### function ends //////////////////////////////////////////////////////////////////////////////////////////////////

    ### returning error payload
    return make_error(message="Matching Failure: SEARCH block is not in target content")

### test execution block ###############################################################################################
if __name__ == "__main__":
    result = match_search_block(content_list=["1", "         2", "3          ", " 4  "], search_list=["2", "3", "4"])
    print("\n", result, "\n")
