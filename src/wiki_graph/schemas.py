from typing import Optional

from pydantic import BaseModel, Field


class BasePage(BaseModel):
    ns: int
    title: str


class Page(BasePage):
    pageid: Optional[int] = None
    links: Optional[list[BasePage]] = None


class Query(BaseModel):
    pages: dict[str, Page]


class NextResult(BaseModel):
    plcontinue: str


class Response(BaseModel):
    next_result: Optional[NextResult] = Field(validation_alias="continue", default=None)
    query: Query

    def extract_links(self) -> Optional[list[str]]:
        """Isolate a list of pages from the query result"""
        # get the first page from the list of pages
        page = next(iter(self.query.pages.values()), None)
        if not page:
            raise ValueError
        if page.links:
            return [link.title for link in page.links]
