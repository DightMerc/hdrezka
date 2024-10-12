from pydantic import BaseModel


class RecordInfoRequestSchema(BaseModel):
    url: str


class ContentRequestSchema(BaseModel):
    url: str
    season: int
    episode: int
    translator_id: int
