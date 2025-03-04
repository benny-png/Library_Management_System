from typing import Optional
from pydantic import BaseModel, constr


class BookBase(BaseModel):
    title: str
    author: str
    published_year: Optional[int] = None
    isbn: Optional[constr(max_length=13)] = None


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    title: Optional[str] = None
    author: Optional[str] = None


class BookResponse(BookBase):
    id: int

    class Config:
        from_attributes = True 