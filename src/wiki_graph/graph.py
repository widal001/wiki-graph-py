from typing import Callable

GetLinkFunc = Callable[[str, int], list]
PageLinkGraph = dict[str, list[str]]


def graph_page_links(
    pages: list[str],
    get_links: GetLinkFunc,
    max_requests: int = 10,
    max_rounds: int = 2,
) -> PageLinkGraph:
    """Create a graph of inbound and outbound links for a list of pages"""
    curr_round = 0
    pages_left = set(pages)
    pages_graphed = set()
    graph = {}
    while pages_left and curr_round < max_rounds:
        # copy the pages_left to a queue so we can iterate through them
        # while we remove each element from the original set
        page_queue = pages_left.copy()
        curr_round += 1
        for page in page_queue:
            # move current page from pages_left to pages_graphed
            pages_left.remove(page)
            pages_graphed.add(page)
            # get outbound links for the current page
            links = get_links(page, max_requests)
            graph[page] = links
            # add the ungraphed links to the pages_left set
            ungraphed = set(links) - pages_graphed
            pages_left.update(ungraphed)
    return graph
