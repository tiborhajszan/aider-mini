########################################################################################################################
### Aider Mini > File Editor Module > Search Block Matching
### Path: aider-mini/mini/editor/search.py
########################################################################################################################

### match search block function ########################################################################################
def match_search_block(
    content_list: list[str],
    search_list: list[str],
) -> dict[str, int | str | tuple[int, int]]:
    """
    Identifies SEARCH lines to be replaced in the local file.
    #### Params:
    - *content_list* > local file content as list of lines
    - *search_list* > SEARCH block content as list of lines
    #### Returns:
    - *dict* > status code, status message, slice indices
    """

    ### function init --------------------------------------------------------------------------------------------------

    #># param validation is handled upstream

    ### function main logic --------------------------------------------------------------------------------------------

    ### search list empty > returning success (0, 0) payload
    if not search_list:
        return {"status": 0, "message": "OK", "indices": (0, 0)}
    
    ### search list too long > returning error payload
    if len(content_list) < len(search_list):
        return {"status": -1, "message": "Matching Failure > SEARCH Block Overflow", "indices": (-1, -1)}

    ### sliding window matching > returning success (start, end) payload
    for content_index in range(len(content_list) - len(search_list) + 1):
        if all(
            content_list[content_index + search_index].strip() == search_list[search_index].strip()
            for search_index in range(len(search_list))
        ):
            return {"status": 0, "message": "OK", "indices": (content_index, content_index + len(search_list))}
        
    ### function ends //////////////////////////////////////////////////////////////////////////////////////////////////

    ### no match > returning error payload
    return {"status": -1, "message": "Matching Failure > SEARCH Block Not Found", "indices": (-1, -1)}

### test execution block ###############################################################################################
if __name__ == "__main__":
    result = match_search_block(content_list=["1", "         2", "3          ", " 4  "], search_list=["2", "3", "4"])
    print("\n", result, "\n")
