from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from fastapi import Form


class CreateTodoSchema(BaseModel):
    title: Optional[str]
    description: Optional[str]

    @classmethod
    def as_form(cls, title: Optional[str] = Form(None), description: Optional[str] = Form(None)):
        return cls(title=title, description=description)


class ImageSchema(BaseModel):
    id: int
    photo_url: str
    todo_id: int

    class Config:
        orm_mode = True


class LinkSchema(BaseModel):
    id: int
    url: str
    todo_id: int

    class Config:
        orm_mode = True


class TodoSchema(CreateTodoSchema):
    id: int
    user_id: int
    images: list[ImageSchema]
    links: list[LinkSchema]
    created: datetime

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda x: x.strftime('%d-%m-%Y %H:%M')
        }
