from pydantic import BaseModel


class Book(BaseModel):
    id: int
    title: str
    author: str
    description: str | None = ""
    year: int
    publisher: str
    category: str
    theme: str | None = "Общая"
    status: str
    favorite: bool
    cover_url: str | None = None
    created_at: str
    updated_at: str
