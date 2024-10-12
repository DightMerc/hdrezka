from pydantic import BaseModel


class AuthRequestSchema(BaseModel):
    login: str
    password: str
