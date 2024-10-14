from typing import Optional

from pydantic import BaseModel, Field


class RecordInfoRequestSchema(BaseModel):
    url: str


class ContentRequestSchema(BaseModel):
    url: str
    season: Optional[int] = Field(None)
    episode: Optional[int] = Field(None)
    translator_id: int
