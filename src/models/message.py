from datetime import datetime

from pydantic import BaseModel


class Message(BaseModel):
    text: str
    date: datetime
