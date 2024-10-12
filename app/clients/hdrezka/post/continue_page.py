"""Any HDRezka page"""

from dataclasses import dataclass
from typing import Iterable, TypeVar, Dict

from bs4 import BeautifulSoup

from ._bs4 import _BUILDER
from ..api.http import get_response
from ..errors import EmptyPage
from ..stream.player import *

__all__ = ("Page", "PageNumber", "InlineItem")

T = TypeVar("T")
PageNumber = TypeVar("PageNumber", int, slice, Iterable[int])


def _range_from_slice(obj: slice | T) -> range | T:
    if isinstance(obj, slice):
        return range(*[i for i in (obj.start, obj.stop, obj.step) if i is not None])
    return obj


@dataclass
class ContinueListItem:
    """Content Inline Item view"""

    url: str
    name: str
    info: str
    date: str
    poster: str

    @property
    async def player(self):
        """Return a Player Instance"""
        return await Player(self.url)


class ContinuePage:
    """AJAX class for HDRezka search"""

    __slots__ = ("_page", "_page_format", "__yields", "__yields_page")

    def __init__(self, url: str = "https://rezka.ag/"):
        self.__yields: list[InlineItem] = []
        self.__yields_page = 0
        self.page = url

    @property
    def page(self) -> str:
        return self._page

    @page.setter
    def page(self, value):
        """Cast value to str and sets"""
        if not isinstance(value, str):
            value = str(value)
        # noinspection HttpUrlsUsage
        if not (value.startswith("https://") or value.startswith("http://")):
            value = f"https://{value}"
        self._page = value

    @staticmethod
    def _concat_paginator(url: str) -> str:
        return f"{url}/page/{{0}}"

    def __aiter__(self):
        """Async iterator by pages"""
        self.__yields_page = 0
        self.__yields.clear()
        return self

    async def __anext__(self) -> ContinueListItem:
        """Returns `InlineItem` object for every title in page"""
        if not self.__yields:
            try:
                self.__yields_page += 1
                self.__yields += await self.get_page(self.__yields_page)
            except EmptyPage:
                raise StopAsyncIteration
        return self.__yields.pop(0)

    async def get_page(self, cookies: Dict) -> list[ContinueListItem]:
        """
        Get items from pages range.
        None for all elements of all pages
        """
        response = await get_response("GET", url=self._page, cookies=cookies)
        items = BeautifulSoup(
            response.text,
            builder=_BUILDER,
        ).find_all(class_="b-videosaves__list_item")
        if not items:
            raise EmptyPage()
        return [
            ContinueListItem(
                date=item.find(class_="td date").text,
                name=str(item.find(class_="td title").text).strip(),
                url=item.find(class_="td title").find("a")["href"],
                info=str(item.find(class_="td info").text).strip(),
                poster=item.find(class_="td title").find("a")["data-cover_url"],
            )
            for item in items[1:]
        ]

    def __repr__(self):
        return f"{self.__class__.__qualname__}({self.page!r})"
