from urllib.parse import urlparse

from fastapi import HTTPException
from starlette.requests import Request

from app.api.schemas.models import SearchResultItem
from app.clients.hdrezka import Search
from app.clients.hdrezka.errors import EmptyPage
from app.controllers import BaseController


class SearchController(BaseController):
    def __init__(self, request: Request):
        super(SearchController, self).__init__(request=request)

    async def _call(self):
        query = self.request.query_params.get("query")
        if not query:
            raise HTTPException(status_code=404, detail="Not found")
        try:
            search_result = await Search(query=query).get_page(page=1)
        except EmptyPage:
            raise HTTPException(status_code=404, detail="Not found")
        for inline_item in search_result:
            inline_item.url = urlparse(url=inline_item.url).path
        return dict(
            items=[
                SearchResultItem(**inline_item.__dict__).model_dump()
                for inline_item in search_result
            ]
        )
