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
        "ns": 0,
    }
    # if next_result is set, add it to the query params as 'plcontinue'
    # that param tells the wikipedia API the next result to retrieve
    if next_result:
        query_params["plcontinue"] = next_result
    # make the API call and check that it was successful
    response = client.get(BASE_URL, params=query_params)
    if response.status_code != 200:
        raise ValueError
    # deserialize the API response
    return schemas.Response(**response.json())


def get_all_outbound_links_for_a_page(
    page_title: str,
    max_requests: int = 10,
    client=httpx,
) -> list[str]:
    """Get all of the outbound links from a given wikipedia page, up to a max number of requests"""
    next_result = None
    request_count = 0
    results = []
    while request_count < max_requests:
        request_count += 1
        print(f"Request #{request_count} for {page_title}")
        response = call_outbound_links_api(client, page_title, next_result)
        page_links = response.extract_links()
        if page_links:
            results.extend(page_links)
        if response.next_result:
            # if there are more results to retrieve
            # set the next_result param and continue
            print(f"Requesting the next result for {page_title}")
            next_result = response.next_result.plcontinue
        else:
            # otherwise return the results
            print(f"Retrieved all links for {page_title}")
            return results
