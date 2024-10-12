from pydantic import BaseModel


class SearchResultItem(BaseModel):
    url: str
    name: str
    info: str
    poster: str


class ContinueResultItem(BaseModel):
    url: str
    name: str
    info: str
    date: str
    poster: str
