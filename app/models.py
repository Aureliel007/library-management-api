from datetime import datetime, timezone

from sqlalchemy import (Column, ForeignKey, Integer, String, Table, DateTime)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


book_author = Table(
    "book_author",
    Base.metadata,
    Column("book_id", ForeignKey("books.id"), primary_key=True, index=True),
    Column("author_id", ForeignKey("authors.id"), primary_key=True, index=True),
)

book_reader = Table(
    "book_user",
    Base.metadata,
    Column("book_id", ForeignKey("books.id"), primary_key=True, index=True),
    Column("reader_id", ForeignKey("readers.id"), primary_key=True, index=True),
    Column("borrow_date", DateTime(timezone=True), default=datetime.now(timezone.utc)),
    Column("return_date", DateTime(timezone=True), nullable=True)
),

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(100), nullable=False)
    registered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(timezone.utc)
    )

    @property
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }
    
    def __str__(self):
        return f"{self.name} ({self.email})"

class Reader(Base):
    __tablename__ = "readers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(timezone.utc)
    )
    books: Mapped[list["Book"]] = relationship("Book", secondary=book_reader, lazy="selectin")

    @property
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }
    
    def __str__(self):
        return f"{self.name} ({self.email})"

class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    release_year: Mapped[int] = mapped_column(Integer, nullable=True)
    authors: Mapped[list["Author"]] = relationship(
        "Author", secondary=book_author, lazy="selectin"
    )
    isbn: Mapped[str] = mapped_column(String(13), unique=True, nullable=True)
    available_stock: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    @property
    def dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_year": self.release_year,
            "authors": self.authors,
            "ISBN": self.isbn,
            "available_stock": self.available_stock
        }
    
    def __str__(self):
        return f"{self.title} ({self.release_year})"
    
    class Author(Base):
        __tablename__ = "authors"

        id: Mapped[int] = mapped_column(Integer, primary_key=True)
        name: Mapped[str] = mapped_column(String(100), nullable=False)
        date_of_birth: Mapped[datetime.date] = mapped_column(DateTime, nullable=False)

        def __str__(self):
            return f"{self.name} ({self.date_of_birth})"