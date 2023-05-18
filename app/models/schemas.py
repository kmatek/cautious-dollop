from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from bson.objectid import ObjectId


class Link(BaseModel):
    id: Optional[ObjectId] = Field(None, alias='_id')
    url: str
    date_added: datetime = Field(default_factory=datetime.utcnow)
    added_by: str

    class Config:
        arbitrary_types_allowed = True
