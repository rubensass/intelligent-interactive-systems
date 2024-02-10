from pydantic import BaseModel


class BookItem(BaseModel):
    url: str
    title: str
    availability: str
    book_rating: str
    category: str
    description: str
    price: str
