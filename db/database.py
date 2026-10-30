from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from os import getenv

DATABASE_URL = getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=True, future=True) # for production delete future and echo

SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)