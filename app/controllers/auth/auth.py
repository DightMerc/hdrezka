from starlette.requests import Request

from app.api.schemas.requests.auth import AuthRequestSchema
from app.clients.hdrezka import AJAX
from app.controllers import BaseController


class AuthController(BaseController):
    def __init__(self, request: Request):
        super(AuthController, self).__init__(request=request, schema=AuthRequestSchema)

    async def _call(self):
        await self._parse_request_data()
        self.request_data: AuthRequestSchema
        auth_result = await self.auth(username=self.request_data.login, password=self.request_data.password)
        return dict(dle_user_id=auth_result['dle_user_id'], dle_password=auth_result['dle_password'])

    async def auth(self, username: str, password: str):
        result = await AJAX().auth(username=username, password=password)
        return dict(result.cookies)