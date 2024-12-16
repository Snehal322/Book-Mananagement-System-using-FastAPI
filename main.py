
# Book management system using FastAPI

from fastapi import Depends, FastAPI, HTTPException  # Import FastAPI and related modules.
from pydantic import BaseModel, EmailStr  # Import Pydantic BaseModel and Email validation type.
from typing import List  # Import List for type hinting.
from sqlalchemy import create_engine, Column, Integer, String  # SQLAlchemy utilities for ORM mapping.
from sqlalchemy.ext.declarative import declarative_base  # Base class for SQLAlchemy models.
from sqlalchemy.orm import sessionmaker, Session  # Session and sessionmaker for database operations.

# SQLAlchemy configuration
DATABASE_URL = "mysql+pymysql://root:admin%40123@localhost/book_management"  # Database connection string.


# Create SQLAlchemy engine and sessionmaker
engine = create_engine(DATABASE_URL, connect_args={"charset": "utf8mb4"})  # Create the SQLAlchemy engine with charset.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # Session factory for managing DB sessions.

# Base class for models
Base = declarative_base()  # Base class for defining SQLAlchemy models.

# Data Model for a Book (SQLAlchemy)
class Book(Base):
    """
    SQLAlchemy model representing the 'books' table in the database.
    """
    __tablename__ = "books"  # Table name in the database.
    id = Column(Integer, primary_key=True, index=True)  # Primary key column with an index.
    title = Column(String(255), nullable=False)  # Title column, cannot be null.
    author = Column(String(255), nullable=False)  # Author column, cannot be null.
    published_year = Column(Integer, nullable=False)  # Published year column, cannot be null.
    genre = Column(String(100), nullable=False)  # Genre column, cannot be null.
    isbn = Column(String(13), unique=True, nullable=False)  # ISBN column, must be unique and cannot be null.

# FastAPI instance
app = FastAPI()  # Create an instance of the FastAPI application.

# Dependency to get the DB session
def get_db():
    """
    Dependency that provides a database session for each request.
    Ensures proper session handling with context management.
    """
    db = SessionLocal()  # Create a new session.
    try:
        yield db  # Yield the session to the endpoint function.
    finally:
        db.close()  # Ensure the session is closed after the request.

# Data model for a Book (Pydantic) for validation
class BookCreate(BaseModel):
    """
    Pydantic schema for validating input data when creating or updating books.
    """
    title: str  # Title field.
    author: str  # Author field.
    published_year: int  # Published year field.
    genre: str  # Genre field.
    isbn: str  # ISBN field.

class BookOut(BookCreate):
    """
    Pydantic schema for output data when returning book information.
    Includes the book ID.
    """
    id: int  # Book ID field.

    class Config:
        orm_mode = True  # Enable automatic conversion of ORM objects to dict.

# Initialize the database (create tables if they don't exist)
Base.metadata.create_all(bind=engine)  # Automatically create the 'books' table in the database.

# Routes

@app.get("/books", response_model=List[BookOut])
def get_books(db: Session = Depends(get_db)):
    """
    Endpoint to retrieve all books.
    - Queries the database for all books and returns them as a list.
    """
    books = db.query(Book).all()  # Fetch all books from the database.
    return books  # Return the list of books.

@app.get("/books/{book_id}", response_model=BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to retrieve a specific book by ID.
    - Queries the database for the book with the given ID.
    - Raises a 404 error if the book is not found.
    """
    book = db.query(Book).filter(Book.id == book_id).first()  # Query the book by ID.
    if not book:  # If no book is found, raise a 404 error.
        raise HTTPException(status_code=404, detail="Book not found")
    return book  # Return the book data.

@app.post("/books", response_model=BookOut)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    """
    Endpoint to create a new book.
    - Accepts book data as input.
    - Adds the book to the database and returns the created book.
    """
    db_book = Book(
        title=book.title,  # Set the book's title.
        author=book.author,  # Set the book's author.
        published_year=book.published_year,  # Set the book's published year.
        genre=book.genre,  # Set the book's genre.
        isbn=book.isbn,  # Set the book's ISBN.
    )
    db.add(db_book)  # Add the new book to the session.
    db.commit()  # Commit the session to save the book to the database.
    db.refresh(db_book)  # Refresh the instance to get the updated data.
    return db_book  # Return the created book.

@app.put("/books/{book_id}", response_model=BookOut)
def update_book(book_id: int, updated_book: BookCreate, db: Session = Depends(get_db)):
    """
    Endpoint to update an existing book.
    - Queries the database for the book by ID.
    - Updates the book's details if it exists.
    - Raises a 404 error if the book is not found.
    """
    db_book = db.query(Book).filter(Book.id == book_id).first()  # Query the book by ID.
    if not db_book:  # If no book is found, raise a 404 error.
        raise HTTPException(status_code=404, detail="Book not found")
    
    db_book.title = updated_book.title  # Update the book's title.
    db_book.author = updated_book.author  # Update the book's author.
    db_book.published_year = updated_book.published_year  # Update the book's published year.
    db_book.genre = updated_book.genre  # Update the book's genre.
    db_book.isbn = updated_book.isbn  # Update the book's ISBN.
    
    db.commit()  # Commit the session to save the changes.
    db.refresh(db_book)  # Refresh the instance to get the updated data.
    return db_book  # Return the updated book.

@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to delete a book by ID.
    - Queries the database for the book by ID.
    - Deletes the book if it exists.
    - Raises a 404 error if the book is not found.
    """
    db_book = db.query(Book).filter(Book.id == book_id).first()  # Query the book by ID.
    if not db_book:  # If no book is found, raise a 404 error.
        raise HTTPException(status_code=404, detail="Book not found")
    
    db.delete(db_book)  # Delete the book from the session.
    db.commit()  # Commit the session to apply the deletion.
    return {"message": f"Book with ID {book_id} deleted"}  # Return a success message.
