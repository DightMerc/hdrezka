"""Sending AJAX requests"""

from typing import SupportsInt

from httpx import Response

from .http import get_response
from ..api.types import APIResponse
from ..errors import AJAXFail

__all__ = ("AJAX",)


class AJAX:
    """Class with methods for sending AJAX requests to the API"""

    __slots__ = ()

    @classmethod
    async def _send_data(cls, action: str, data: dict[str, SupportsInt | str]):
        answer = (
            await get_response("POST", f"https://rezka.ag/ajax/{action}/", data=data)
        ).json()
        if not answer.get("success", True):
            raise AJAXFail(answer.get("message", answer))
        return answer

    @classmethod
    async def _send_data_modified(
        cls, action: str, data: dict[str, SupportsInt | str]
    ) -> Response:
        answer = await get_response(
            "POST", f"https://rezka.ag/ajax/{action}/", data=data
        )
        if not answer.json().get("success", True):
            raise AJAXFail(answer.get("message", answer))
        return answer

    @classmethod
    async def get_cdn_series(cls, data: dict[str, SupportsInt | str]):
        """Request series for one translation"""
        return await cls._send_data("get_cdn_series", data)

    @classmethod
    async def get_episodes(
        cls, id: SupportsInt | str, translator_id: SupportsInt | str
    ):
        """Request episodes"""
        return await cls.get_cdn_series(
            {"action": "get_episodes", "id": id, "translator_id": translator_id}
        )

    @classmethod
    async def get_stream(
        cls,
        id: SupportsInt | str,
        translator_id: SupportsInt | str,
        season: SupportsInt | str,
        episode: SupportsInt | str,
    ) -> APIResponse:
        """Request stream urls"""
        return await cls.get_cdn_series(
            {
                "action": "get_stream",
                "id": id,
                "translator_id": translator_id,
                "season": season,
                "episode": episode,
            }
        )

    @classmethod
    async def get_movie(cls, id: SupportsInt | str, translator_id: SupportsInt | str):
        """Request movie urls"""
        return await cls.get_cdn_series(
            {"action": "get_movie", "id": id, "translator_id": translator_id}
        )

    @classmethod
    async def auth(cls, username: str, password: str) -> Response:
        return await cls._send_data_modified(
            action="login",
            data={
                "login_name": username,
                "login_password": password,
                "login_not_save": 0,
            },
        )
