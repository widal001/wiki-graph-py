import httpx

from wiki_graph.requests import get_page_links, make_link_request
from wiki_graph.schemas import BasePage


def test_get_make_link_request():
    """When making a single request for a page with more than 500 links:
    - the number of links should be 500
    - the batchcomplete attribute should be None
    - the next_page attribute should NOT be None
    """
    response = make_link_request(httpx, "SQL")
    page = response.query.pages.get("29004")
    assert page is not None
    assert len(page.links) == 500
    assert response.batchcomplete is None
    assert response.next_page is not None
    assert response.next_page.plcontinue is not None


def test_get_page_links():
    """When retrieving all of the links for a page with >1000 links:
    - the number of links returned should be 1000
    - each link should be of type BasePage
    """
    results = get_page_links(httpx, "SQL", max_requests=2)
    print(len(results))
    assert len(results) == 1000
    assert isinstance(results[0], BasePage)
