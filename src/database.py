import uuid
from typing import Any, AsyncGenerator
from sqlalchemy import (
    Column,
    CursorResult,
    DateTime,
    ForeignKey,
    Insert,
    Integer,
    MetaData,
    Select,
    String,
    Update,
    NullPool,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from src.config import DATABASE_URL


Base = declarative_base()
metadata = MetaData()


engine = create_async_engine(DATABASE_URL, pool_pre_ping=True, poolclass=NullPool)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


class Role(Base):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    metadata = metadata


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    license_key = Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=False)
    license_time = Column(DateTime, nullable=True)
    user_info = Column(String, nullable=True)
    role_id = Column(Integer, ForeignKey('role.id'), nullable=False, default=3)
    metadata = metadata


async def fetch_one(select_query: Select | Insert | Update) -> dict[str, Any] | None:
    async with engine.begin() as conn:
        cursor: CursorResult = await conn.execute(select_query)
        return cursor.first()._asdict() if cursor.rowcount > 0 else None


async def fetch_all(select_query: Select | Insert | Update) -> list[dict[str, Any]]:
    async with engine.begin() as conn:
        cursor: CursorResult = await conn.execute(select_query)
        return [r._asdict() for r in cursor.all()]


async def execute(select_query: Insert | Update) -> None:
    async with engine.begin() as conn:
        await conn.execute(select_query)
