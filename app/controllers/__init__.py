import logging
from typing import Dict, Optional

from fastapi import HTTPException
from fastapi.responses import ORJSONResponse
from starlette import status
from starlette.requests import Request


class BaseController(object):
    def __init__(self, request: Request, schema=None):
        self.logger = logging.getLogger()
        self.request = request
        # self.session = create_session_maker()
        self.schema = schema
        self.user_id = None
        self.user_password = None

    def _call(self):
        raise NotImplementedError

    async def _parse_request_data(self):
        if not self.schema:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Schema is not specified",
            )
        self.request_data = self.schema(**(await self.request.json()))

    async def _verify_user(self):
        auth_data: str = self.request.headers.get("Authorization")
        if not auth_data:
            raise HTTPException(status_code=404, detail="Authorization header required")
        if "Bearer" not in auth_data:
            raise HTTPException(status_code=404, detail="Authorization type incorrect")
        auth_data = auth_data.replace("Bearer", "")
        if len(auth_data.split("|")) != 2:
            raise HTTPException(
                status_code=404, detail="Authorization header incorrect"
            )
        user_id = auth_data.split("|")[0]
        user_password = auth_data.split("|")[1]
        self.user_id = user_id
        self.user_password = user_password

    def _get_logger(self) -> logging.Logger:
        logger: logging.Logger = logging.getLogger("app")
        logger.setLevel(logging.DEBUG)
        return logger

    async def _clear_sensitive_data(self, data: Dict):
        sensitive_fields = ("password",)
        return {key: data[key] for key in data.keys() if key not in sensitive_fields}

    async def call(self):
        return ORJSONResponse(await self._call())
