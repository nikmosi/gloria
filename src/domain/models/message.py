from datetime import datetime

from pydantic import BaseModel


class RawMessage(BaseModel):
    text: str
    date: datetime
