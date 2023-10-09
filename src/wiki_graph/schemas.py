from typing import Optional

from pydantic import BaseModel, Field


class BasePage(BaseModel):
    ns: int
    title: str


class Page(BasePage):
    pageid: int
    links: Optional[list[BasePage]] = None


class Query(BaseModel):
    pages: dict[str, Page]


class NextPage(BaseModel):
    plcontinue: str


class Response(BaseModel):
    batchcomplete: Optional[str] = None
    next_page: Optional[NextPage] = Field(validation_alias="continue", default=None)
    query: Query

    def extract_links(self) -> Optional[list[BasePage]]:
        """Isolate a list of pages from the query result"""
        # get the first page from the list of pages
        page = next(iter(self.query.pages.values()), None)
        if not page:
            raise ValueError
        return page.links
