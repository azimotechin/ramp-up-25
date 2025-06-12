from typing import List, Optional, Dict
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(
    title="Book Library API",
    description="REST API for a Book Library using FastAPI, capable of performing basic CRUD operations.",
    version="1.0.0",
)

class Book(BaseModel):
    id: Optional[int] = None
    title: str
    author: str
    year: int
books_db: Dict[int, Book] = {}
next_book_id: int = 1

@app.post("/books/", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
    global next_book_id
    book.id = next_book_id
    books_db[next_book_id] = book
    next_book_id += 1
    return book

@app.get("/books/", response_model=List[Book])
async def read_books(skip: int = 0, limit: int = 100):
    return list(books_db.values())[skip : skip + limit]

@app.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: int):
    book = books_db.get(book_id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {book_id} not found")
    return book

@app.put("/books/{book_id}", response_model=Book)
async def update_book(book_id: int, updated_book: Book):
    if book_id not in books_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {book_id} not found")
    updated_book.id = book_id
    books_db[book_id] = updated_book
    return updated_book

@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    if book_id not in books_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {book_id} not found")
    del books_db[book_id]
    return