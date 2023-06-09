from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, HttpUrl


class ObjectIdStr(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        # Convert ObjectOd into str
        return str(v)


class LinkIn(BaseModel):
    url: HttpUrl
    added_by: str = None

    class Config:
        schema_extra = {
            "example": {
                "url": "https://example.com/"
            }
        }


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


class UserModel(BaseModel):
    id: Optional[ObjectIdStr] = Field(None, alias='_id')
    email: EmailStr = None
    username: str
    is_admin: bool = False
    date_added: datetime = None
    disabled: bool = False

    class Config:
        arbitrary_types_allowed = True


class DBUser(UserModel):
    password: str

    class Config:
        schema_extra = {
            "example": {
                "username": "string",
                "password": "string",
                "email": "example@email.com"
            }
        }


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenIn(BaseModel):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "example@email.com",
                "password": "string"
            }
        }


class PasswordUpdate(BaseModel):
    old_password: str
    new_password: str

    class Config:
        schema_extra = {
            "example": {
                "old_password": "password",
                "new_password": "password"
            }
        }
