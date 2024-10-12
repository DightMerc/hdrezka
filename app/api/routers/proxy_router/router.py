from typing import Annotated, Union

from fastapi import APIRouter, Query
from fastapi.responses import ORJSONResponse
from starlette.requests import Request

from app.api.schemas.requests.auth import AuthRequestSchema
from app.api.schemas.requests.records import (
    RecordInfoRequestSchema,
    ContentRequestSchema,
)
from app.api.schemas.responses.records import RecordInfoResponseSchema
from app.api.schemas.responses.search import SearchResponseSchema
from app.controllers.auth.auth import AuthController
from app.controllers.content.content import ContentController
from app.controllers.content.info import RecordInfoController
from app.controllers.content.all_content import AllContentController
from app.controllers.content.my_list import MyListController
from app.controllers.content.search import SearchController

router = APIRouter(tags=["proxy"])


@router.post("/auth", response_model=AuthRequestSchema)
async def auth(request: Request, schema: AuthRequestSchema) -> ORJSONResponse:
    return await AuthController(request=request).call()


@router.get("/all", response_model=SearchResponseSchema)
async def all(
    request: Request,
    page: Annotated[Union[str, None], Query(description="Page number")] = None,
) -> ORJSONResponse:
    return await AllContentController(request=request).call()


@router.get("/search", response_model=SearchResponseSchema)
async def search(
    request: Request,
    query: Annotated[Union[str, None], Query(description="Search text")] = None,
) -> ORJSONResponse:
    return await SearchController(request=request).call()


@router.post("/info", response_model=RecordInfoResponseSchema)
async def info(request: Request, schema: RecordInfoRequestSchema) -> ORJSONResponse:
    return await RecordInfoController(request=request).call()


@router.post("/content", response_model=RecordInfoResponseSchema)
async def content(request: Request, schema: ContentRequestSchema) -> ORJSONResponse:
    return await ContentController(request=request).call()


@router.get("/my_list", response_model=SearchResponseSchema)
async def my_list(
    request: Request,
) -> ORJSONResponse:
    return await MyListController(request=request).call()
