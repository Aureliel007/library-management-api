from sqlalchemy.ext.asyncio import (
    async_sessionmaker, create_async_engine, AsyncAttrs, AsyncSession
)
from sqlalchemy.orm import DeclarativeBase

from .config import settings

PG_DSN=settings.pg_dsn

engine = create_async_engine(PG_DSN)
Session = async_sessionmaker(
    bind=engine, 
    expire_on_commit=False,
    class_=AsyncSession,
    autoflush=False
)

class Base(AsyncAttrs, DeclarativeBase):
    pass
