from __future__ import annotations
from typing import Callable

import networkx as nx

GetLinkFunc = Callable[[str, int], list]


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
    graph = PageLinkGraph()
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
            graph.add_outbound_links(src_page=page, links=links)
            # add the ungraphed links to the pages_left set
            ungraphed = set(links) - pages_graphed
            pages_left.update(ungraphed)
    return graph


class PageLinkGraph:
    """Represents a directed graph of Wikipedia pages

    In this graph, pages are nodes and edges represent hyperlinks between pages
    with the direction representing an outbound link
    """

    def __init__(self) -> None:
        """Initiate the graph"""
        self.graph = nx.DiGraph()

    def add_outbound_links(self, src_page: str, links: list[str]):
        """Add an outbound link from a source page to a list of target pages"""
        page_links = [(src_page, tgt_page) for tgt_page in links]
        self.graph.add_edges_from(page_links)

    @property
    def pages(self) -> list:
        """Returns a list of pages in the graph"""
        return list(self.graph.nodes)

    @property
    def outbound_links(self) -> list:
        """Returns a list of outbound links between the pages in the graph"""
        return list(self.graph.edges)
