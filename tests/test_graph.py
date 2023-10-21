from pprint import pprint

from wiki_graph.graph import graph_page_links, PageLinkGraph
from tests import data


def get_page_links(page: str, max_requests: int = 1) -> list[str]:
    """Mock get_link() function that raises an error if a page is requested twice

    This helps us check that the function that invokes it won't make multiple
    requests for the same page if it appears in the list of links for two pages
    """
    input_graph = data.INPUT_GRAPH
    assert max_requests > 0
    if page not in input_graph:
        raise KeyError
    return input_graph.pop(page)


class TestGraphPageLinks:
    """Tests the graph_page_links() function"""

    def test_one_page_left_with_three_rounds(self):
        """3 rounds of mapping links should leave only the 'g' page ungraphed"""
        # setup and execution
        page = ["a"]
        graph = graph_page_links(page, get_page_links, max_rounds=3)
        # print the output and input graphs to debug
        print("~~~~~~~~~~~~ Output ~~~~~~~~~~~~~~")
        pprint(graph.graph)
        print("~~~~~~~~~~~~ Input ~~~~~~~~~~~~~~~")
        pprint(data.INPUT_GRAPH)
        # check that only the "g" page is left in the input graph
        assert "g" in data.INPUT_GRAPH
        assert len(data.INPUT_GRAPH)
        # check that all of the other pages are in the output graph
        for page in "abcdef":
            assert page in graph.pages


class TestPageLinkGraph:
    """Tests the PageLinkGraph class"""

    def test_add_outbound_link(self):
        """Tests the PageLinkGraph.add_outbound_link() method"""
        # setup
        graph = PageLinkGraph()
        # execution
        graph.add_outbound_links(src_page="a", links=["b", "c"])
        # validation
        assert "a" in graph.pages
        assert "b" in graph.pages
        assert "c" in graph.pages
        assert "d" not in graph.pages
        assert ("a", "b") in graph.outbound_links
        assert ("a", "c") in graph.outbound_links
        assert ("b", "a") not in graph.outbound_links  # links should only go from a
        assert ("b", "c") not in graph.outbound_links  # links shouldn't exist between
