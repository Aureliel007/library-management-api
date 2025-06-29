from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, field_validator, Field


class ItemId(BaseModel):
    id: int

class StatusResponse(BaseModel):
    status: Literal["ok", "deleted"]

class BaseUser(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if len(value) > 32:
            raise ValueError("Password must not exceed 32 characters.")
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one digit.")
        if not any(char.isalpha() for char in value):
            raise ValueError("Password must contain at least one letter.")
        return value

class CreateUser(BaseUser):
    name: str

class GetUser(BaseModel):
    id: int
    name: str
    email: EmailStr
    registered_at: datetime

class UpdateUser(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None

    @field_validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if len(value) > 32:
            raise ValueError("Password must not exceed 32 characters.")
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one digit.")
        if not any(char.isalpha() for char in value):
            raise ValueError("Password must contain at least one letter.")
        return value

class BaseBook(BaseModel):
    title: str
    release_year: int
    authors: str
    isbn: str
    available_stock: int

class GetBook(BaseBook):
    id: int

class UpdateBook(BaseModel):
    title: str | None = None
    release_year: int | None = None
    authors: str | None = None
    isbn: str | None = None
    available_stock: int | None = None

class BorrowedBookInfo(BaseModel):
    book: GetBook
    borrow_date: datetime
    return_date: datetime | None = None

class BaseReader(BaseModel):
    name: str
    email: EmailStr

class ReadersList(BaseReader):
    id: int

class GetReader(BaseReader):
    id: int
    created_at: datetime
    books: list[BorrowedBookInfo]

class UpdateReader(BaseModel):
    name: str | None = None
    email: EmailStr | None = None