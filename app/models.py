from datetime import datetime, timezone

from sqlalchemy import (
    Column, ForeignKey, Integer, String, Table, DateTime, Boolean
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


# book_reader = Table(
#     "book_user",
#     Base.metadata,
#     Column("book_id", ForeignKey("books.id"), primary_key=True, index=True),
#     Column("reader_id", ForeignKey("readers.id"), primary_key=True, index=True),
#     Column("borrow_date", DateTime(timezone=True), default=datetime.now(timezone.utc)),
#     Column("returned", Boolean, default=False),
#     Column("return_date", DateTime(timezone=True), nullable=True)
# ),

class BookReader(Base):
    __tablename__ = "book_reader"
    
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), primary_key=True)
    reader_id: Mapped[int] = mapped_column(ForeignKey("readers.id"), primary_key=True)
    borrow_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(timezone.utc)
    )
    returned: Mapped[bool] = mapped_column(Boolean, default=False)
    return_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    librarian_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    
    book: Mapped["Book"] = relationship("Book", back_populates="readers", lazy="selectin")
    reader: Mapped["Reader"] = relationship("Reader", back_populates="books", lazy="selectin")

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
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
    books: Mapped[list["BookReader"]] = relationship(
        "BookReader", 
        back_populates="reader", 
        lazy="joined",
        cascade="all, delete-orphan"
    )

    @property
    def not_returned_books(self):
        return [book for book in self.books if not book.returned]
    
    def __str__(self):
        return f"{self.name} ({self.email})"

class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    release_year: Mapped[int] = mapped_column(Integer, nullable=True)
    authors: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    isbn: Mapped[str] = mapped_column(String(13), unique=True, nullable=True)
    available_stock: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    readers: Mapped[list["BookReader"]] = relationship(
        "BookReader", 
        back_populates="book",
        lazy="selectin"
    )

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

ORM_OBJECT = Reader | Book | User
ORM_CLS = type[Reader] | type[Book] | type[User]
