from fastapi import APIRouter, HTTPException

from app.dependencies import SessionDep
from app.models import User, Reader, Book
from app.schemas import (
    ItemId,
    StatusResponse,
    BaseUser,
    CreateUser,
    GetUser,
    UpdateUser,
    BaseReader,
    GetReader,
    ReadersList,
    UpdateReader,
    BaseBook,
    GetBook,
    UpdateBook

)
from app.auth import TokenDependency, hash_password, check_password, create_token
import app.crud as crud


router = APIRouter(
    prefix="/api/v1",
)

# Authorization

@router.post("/register", response_model=ItemId, tags=["auth"])
async def register_user(user_data: CreateUser, session: SessionDep):
    user = User(**user_data.model_dump())
    user.password = hash_password(user.password)
    user_db = await crud.add_item(session, user)
    return {"id": user_db.id}

@router.post("/login", response_model=str, tags=["auth"])
async def login_user(user_data: BaseUser, session: SessionDep):
    user_db = await crud.get_user_by_email(session, User, user_data.email)
    if not check_password(user_data.password, user_db.password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    user_data = {"id": user_db.id}
    return create_token(user_data)

@router.get("/my_profile", response_model=GetUser, tags=["auth"])
async def get_user(user_info: TokenDependency, session: SessionDep):
    user_id = user_info.get("id")
    user = await crud.get_item(session, User, user_id)
    return user

@router.patch("/my_profile", response_model=GetUser, tags=["auth"])
async def update_user(user_info: TokenDependency, user_data: UpdateUser, session: SessionDep):
    user_id = user_info.get("id")
    user = await crud.get_item(session, User, user_id)
    for field, value in user_data.model_dump(exclude_unset=True).items():
        if field == "password":
            value = hash_password(value)
        setattr(user, field, value)
    user = await crud.add_item(session, user)
    return user

# Readers

@router.get("/readers", response_model=list[ReadersList], tags=["readers"])
async def get_readers(session: SessionDep, jwt_required: TokenDependency):
    return await crud.get_items(session, Reader)

@router.get("/readers/{reader_id}", response_model=GetReader, tags=["readers"])
async def get_reader(
    reader_id: int,
    session: SessionDep, 
    jwt_required: TokenDependency,
    with_history: bool = False
):
    return await crud.get_reader_details(session, reader_id, with_history)


@router.post("/readers", response_model=ItemId, tags=["readers"])
async def add_reader(reader_data: BaseReader, session: SessionDep):
    reader = Reader(**reader_data.model_dump())
    reader_db = await crud.add_item(session, reader)
    return {"id": reader_db.id}

@router.patch("/readers/{reader_id}", response_model=GetReader, tags=["readers"])
async def update_reader(
    reader_id: int, 
    reader_data: UpdateReader, 
    session: SessionDep, 
    jwt_required: TokenDependency
):
    reader = await crud.get_item(session, Reader, reader_id)
    for field, value in reader_data.model_dump(exclude_unset=True).items():
        setattr(reader, field, value)
    reader = await crud.add_item(session, reader)
    return reader

@router.delete("/readers/{reader_id}", response_model=StatusResponse, tags=["readers"])
async def delete_reader(reader_id: int, session: SessionDep, jwt_required: TokenDependency):
    reader = await crud.get_item(session, Reader, reader_id)
    if reader.not_returned_books:
        raise HTTPException(status_code=400, detail="Cannot delete reader with books")
    
    await session.delete(reader)
    await session.commit()
    return {"status": "deleted"}

# Books

@router.get("/books", response_model=list[GetBook], tags=["books"])
async def get_books(session: SessionDep, jwt_required: TokenDependency):
    return await crud.get_items(session, Book)

@router.get("/books/{book_id}", response_model=GetBook, tags=["books"])
async def get_book(
    book_id: int, 
    session: SessionDep, 
    jwt_required: TokenDependency
):
    return await crud.get_item(session, Book, book_id)

@router.post("/books", response_model=ItemId, tags=["books"])
async def add_book(
    book_data: BaseBook, 
    session: SessionDep, 
    jwt_required: TokenDependency
):
    book = Book(**book_data.model_dump())
    book_db = await crud.add_item(session, book)
    return {"id": book_db.id}

@router.patch("/books/{book_id}", response_model=GetBook, tags=["books"])
async def update_book(
    book_id: int, 
    book_data: UpdateBook, 
    session: SessionDep, 
    jwt_required: TokenDependency
):
    book = await crud.get_item(session, Book, book_id)
    for field, value in book_data.model_dump(exclude_unset=True).items():
        setattr(book, field, value)
    book = await crud.add_item(session, book)
    return book

@router.delete("/books/{book_id}", response_model=StatusResponse, tags=["books"])
async def delete_book(
    book_id: int, 
    session: SessionDep, 
    jwt_required: TokenDependency
):
    book = await crud.get_item(session, Book, book_id)
    try:
        await session.delete(book)
        await session.commit()
    except AssertionError as err:
        raise HTTPException(
            status_code=400, detail=str("You cannot delete book with borrowed copies")
        )
    return {"status": "deleted"}

# Borrowing

@router.post("/borrow", response_model=StatusResponse, tags=["borrowing"])
async def borrow_book(
    book_id: int, 
    reader_id: int, 
    session: SessionDep, 
    user: TokenDependency
):
    return await crud.borrow_book(session, book_id, reader_id, user.get("id"))

@router.post("/return", response_model=StatusResponse, tags=["borrowing"])
async def return_book(
    book_id: int, 
    reader_id: int, 
    session: SessionDep, 
    user: TokenDependency
):
    return await crud.return_book(session, book_id, reader_id, user.get("id"))
