from typing import Annotated
from fastapi import Depends

from .database import Session


async def get_session():
    async with Session() as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
