import httpx

from wiki_graph.requests import (
    call_outbound_links_api,
    get_all_outbound_links_for_a_page,
)
from wiki_graph.schemas import BasePage


def test_call_outbound_links_api():
    """When making a single request for a page with more than 500 links:
    - the number of links should be 500
    - the batchcomplete attribute should be None
    - the next_result attribute should NOT be None
    """
    response = call_outbound_links_api(httpx, "SQL")
    page = response.query.pages.get("29004")
    assert page is not None
    assert len(page.links) == 500
    assert response.next_result is not None
    assert response.next_result.plcontinue is not None


def test_get_all_outbound_links_for_a_page():
    """When retrieving all of the links for a page with > 500 links:
    - the number of links returned should be greater than 500
    - each link should be of type BasePage
    """
    results = get_all_outbound_links_for_a_page(
        page_title="SQL",
        max_requests=5,
        client=httpx,
    )
    print(len(results))
    assert len(results) > 500
    assert len(set(page.title for page in results)) == len(results)
    assert isinstance(results[0], str)
