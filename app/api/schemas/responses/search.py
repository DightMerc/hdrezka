from typing import List

from pydantic import BaseModel

from app.api.schemas.models import SearchResultItem


class SearchResponseSchema(BaseModel):
    items: List[SearchResultItem]
