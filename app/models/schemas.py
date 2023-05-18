from datetime import datetime
from pydantic import BaseModel, Field


class Link(BaseModel):
    link: str
    date_added: datetime = Field(default_factory=datetime.utcnow)
    added_by: str
