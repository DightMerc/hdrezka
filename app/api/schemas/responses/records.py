from typing import Dict

from pydantic import BaseModel


class RecordInfoResponseSchema(BaseModel):
    info: Dict
