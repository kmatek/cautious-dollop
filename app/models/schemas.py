from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ObjectIdStr(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        # Convert ObjectOd into str
        return str(v)


class LinkIn(BaseModel):
    url: str
    added_by: str


class Link(LinkIn):
    id: Optional[ObjectIdStr] = Field(None, alias='_id')
    date_added: datetime = None

    class Config:
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "_id": "6467c9dabb951c55083fadb2",
                "url": "https://example.com/",
                "date_added": "2023-05-19T19:11:22.651000",
                "added_by": "Someone"
            }
        }
