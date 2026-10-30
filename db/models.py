from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, func, BigInteger

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

class Jokes(Base):
    __tablename__ = "jokes"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    joke_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True,
        unique=True
    )

    joke_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    joke: Mapped[str] = mapped_column(
        String(1000),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )