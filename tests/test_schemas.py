from copy import deepcopy

from wiki_graph.schemas import Response
from tests import data


def test_response_with_next_page():
    """Response schema should deserialize the test data correctly"""
    # validation - response deserialized correctly
    response = Response(**data.RESPONSE)
    assert len(response.query.pages) == 1
    assert response.next_page is not None
    # validation - page deserialized correctly
    page = response.query.pages["123"]
    assert len(page.links) == 2
    assert page.links[0].title == "Eminent domain"


def test_response_without_next_page():
    """Response.next_page should be None if there is no 'continue' attribute"""
    # setup - remove "continue" attribute from json data
    input_data = deepcopy(data.RESPONSE)
    input_data.pop("continue")
    # execution
    response = Response(**input_data)
    # validation
    assert response.next_page is None
