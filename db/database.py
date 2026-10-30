from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from os import getenv

DATABASE_URL = getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is missing")

engine = create_async_engine(DATABASE_URL, echo=False, pool_pre_ping=True) # for production delete future and echo

SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)