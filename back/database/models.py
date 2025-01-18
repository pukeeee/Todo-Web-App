from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_async_engine(DATABASE_URL, echo = True)

async_session = async_sessionmaker(bind = engine, expire_on_commit = False)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key = True)
    tgId = mapped_column(BigInteger)

class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key = True)
    user: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete = "CASCADE"))
    text: Mapped[str] = mapped_column(String(100))
    status: Mapped[bool] = mapped_column(default = False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
