from urllib.parse import urlparse

from starlette.requests import Request

from app.api.schemas.models import SearchResultItem
from app.clients.hdrezka.post.page import Page
from app.controllers import BaseController


class AllContentController(BaseController):
    def __init__(self, request: Request):
        super(AllContentController, self).__init__(request=request)

    async def _call(self):
        page = self.request.query_params.get("page", 1)
        result = await Page().get_page(page=page)
        for inline_item in result:
            inline_item.url = urlparse(url=inline_item.url).path
        return dict(
            items=[
                SearchResultItem(**inline_item.__dict__).model_dump()
                for inline_item in result
            ]
        )
