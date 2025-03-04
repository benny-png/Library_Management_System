from typing import List
from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError

from src.database.models import Book
from src.schemas.book import BookCreate, BookUpdate, BookResponse

books_router = APIRouter()


@books_router.post("/books/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate):
    """Create a new book"""
    try:
        db_book = Book(**book.model_dump())
        return db_book.save()
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="ISBN already exists"
        )


@books_router.get("/books/", response_model=List[BookResponse])
async def get_books():
    """Get all books"""
    return Book.get_all()


@books_router.get("/books/{book_id}", response_model=BookResponse)
async def get_book(book_id: int):
    """Get a specific book by ID"""
    if book := Book.get_by_id(book_id):
        return book
    raise HTTPException(
        status_code=404,
        detail="Book not found"
    )


@books_router.put("/books/{book_id}", response_model=BookResponse)
async def update_book(book_id: int, book_update: BookUpdate):
    """Update a book"""
    if book := Book.get_by_id(book_id):
        try:
            return book.update(**book_update.model_dump(exclude_unset=True))
        except IntegrityError:
            raise HTTPException(
                status_code=400,
                detail="ISBN already exists"
            )
    raise HTTPException(
        status_code=404,
        detail="Book not found"
    )


@books_router.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    """Delete a book"""
    if book := Book.get_by_id(book_id):
        book.delete()
        return
    raise HTTPException(
        status_code=404,
        detail="Book not found"
    ) 