from fastapi import HTTPException
from starlette.requests import Request

from app.api.schemas.models import ContinueResultItem
from app.clients.hdrezka.errors import EmptyPage
from app.clients.hdrezka.post.continue_page import ContinuePage
from app.controllers import BaseController


class MyListController(BaseController):
    def __init__(self, request: Request):
        super(MyListController, self).__init__(request=request)

    async def _call(self):
        try:
            continue_result = await ContinuePage(
                url="https://hdrezka.ag/continue/"
            ).get_page(
                cookies=dict(
                    dle_user_id="1655756",
                    dle_password="5701b8fd135843a24917b30c2ff15b7a",
                )
            )
        except EmptyPage:
            raise HTTPException(status_code=404, detail="Not found")
        return dict(
            items=[
                ContinueResultItem(**inline_item.__dict__).model_dump()
                for inline_item in continue_result
            ]
        )