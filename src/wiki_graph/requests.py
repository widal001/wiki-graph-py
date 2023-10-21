from typing import Optional

import httpx

from wiki_graph import schemas

BASE_URL = "https://en.wikipedia.org/w/api.php"


def call_outbound_links_api(
    client,
    page_title: str,
    next_result: Optional[str] = None,
) -> schemas.Response:
    """Query the wikipedia API to get a list of outbound links for a page"""
    query_params = {
        "action": "query",
        "prop": "links",
        "titles": page_title,
        "pllimit": "max",
        "format": "json",
    }
    if next_result:
        query_params["plcontinue"] = next_result
    response = client.get(BASE_URL, params=query_params)
    if response.status_code != 200:
        raise ValueError
    data = response.json()
    return schemas.Response(**data)


def get_all_outbound_links_for_a_page(
    page_title: str,
    max_requests: int = 25,
    client=httpx,
) -> list[schemas.BasePage]:
    """Get all of the outbound links from a given wikipedia page, up to a max number of requests"""
    complete = None
    request_count = 0
    results: list[schemas.BasePage] = []
    try:
        while not complete and request_count < max_requests:
            request_count += 1
            response = call_outbound_links_api(client, page_title)
            complete = response.batchcomplete
            page_links = response.extract_links()
            if page_links:
                results.extend(page_links)
    except ValueError as err:
        print(err)
    return results
