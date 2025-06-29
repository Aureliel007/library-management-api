from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from fastapi import HTTPException

from app.database import Session
from app.models import Reader, Book, User, BookReader, ORM_OBJECT, ORM_CLS


# Base
async def add_item(session: Session, item: ORM_OBJECT) -> ORM_OBJECT:
    session.add(item)
    try:
        await session.commit()
    except IntegrityError as err:
        if err.orig.pgcode == '23505':
            raise HTTPException(
                status_code=409,
                detail='Item already exists'
            )
        raise err
    return item
    
async def get_item(session: Session, cls: ORM_CLS, item_id: int) -> ORM_OBJECT:
    orm_obj = await session.get(cls, item_id)
    if orm_obj is None:
        raise HTTPException(
            status_code=404,
            detail=f'{cls.__name__} not found'
        )
    return orm_obj

async def get_items(session: Session, cls: ORM_CLS) -> list[ORM_OBJECT]:
    query = select(cls)
    result = await session.execute(query)
    items = result.unique().scalars().all()
    return items

# Users

async def get_user_by_email(session: Session, cls: ORM_CLS, email: str):
    user_query = select(cls).where(User.email == email)
    user_model = await session.scalar(user_query)
    if user_model is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user_model

# Readers

async def get_reader_details(
        session: Session, reader_id: int, returned: bool = False
):
    reader = await get_item(session, Reader, reader_id)
    if returned:
        return reader
    return {
        "id": reader.id,
        "name": reader.name,
        "email": reader.email,
        "created_at": reader.created_at,
        "books": reader.not_returned_books
    }
    

# Borrowing

async def borrow_book(session: Session, book_id: int, reader_id: int, librarian_id: int):
    book = await get_item(session, Book, book_id)
    reader = await get_item(session, Reader, reader_id)
    if book.available_stock <= 0:
        raise HTTPException(status_code=400, detail="Book is not available")
    not_returned_books = reader.not_returned_books
    if len(not_returned_books) >= 3:
        raise HTTPException(
            status_code=400,
            detail=f"Reader {reader.name} has reached the limit of 3 books"
        )
    for user_book in not_returned_books:
        if user_book.book_id == book_id:
            raise HTTPException(status_code=400, detail="Reader already has this book")
    
    book_reader = BookReader(
        book_id=book_id,
        reader_id=reader_id,
        librarian_id=librarian_id
    )
    book.available_stock -= 1
    
    session.add(book_reader)
    await session.commit()
    return {"status": "ok"}

async def return_book(session: Session, book_id: int, reader_id: int, librarian_id: int):
    book = await get_item(session, Book, book_id)
    reader = await get_item(session, Reader, reader_id)

    query = (
    select(BookReader)
    .where(BookReader.book_id == book_id)
    .where(BookReader.reader_id == reader_id)
    .where(BookReader.returned == False)
)
    result = await session.execute(query)
    book_reader = result.scalars().first()
    if not book_reader:
        raise HTTPException(status_code=400, detail="Reader does not have this book")
    
    book.available_stock += 1
    
    book_reader.returned = True
    book_reader.return_date = datetime.now(timezone.utc)
    book_reader.librarian_id = librarian_id
    await session.commit()
    return {"status": "ok"}
