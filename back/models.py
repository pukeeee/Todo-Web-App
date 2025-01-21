from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from config import DATABASE_URL
import os

# load_dotenv()
# DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_async_engine(DATABASE_URL, echo = True)

async_session = async_sessionmaker(bind = engine, expire_on_commit = False)

class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key = True)
    tgId = mapped_column(BigInteger)
    experience: Mapped[int] = mapped_column(BigInteger, default = 0)
    all_tasks_count: Mapped[int] = mapped_column(Integer, default=0)
    all_habits_count: Mapped[int] = mapped_column(Integer, default=0)
    start_date: Mapped[int] = mapped_column(Integer)


class Profile(Base):
    __tablename__ = "profiles"
    id: Mapped[int] = mapped_column(primary_key = True)
    user: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user_name: Mapped[str] = mapped_column(String(25), default = "")
    avatar: Mapped[str] = mapped_column(String(30), default = "")
    race: Mapped[str] = mapped_column(String(30), default = "")
    sex: Mapped[str] = mapped_column(String(30), default = "")
    clas: Mapped[str] = mapped_column(String(30), default = "")


class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key = True)
    text: Mapped[str] = mapped_column(String(100))
    user: Mapped[int] = mapped_column(ForeignKey("users.id"))
    status: Mapped[bool] = mapped_column(Boolean, default = False)
    done_date: Mapped[int] = mapped_column(Integer, default = 0)


class Habit(Base):
    __tablename__ = "habits"
    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[int] = mapped_column(ForeignKey('users.id'))
    name: Mapped[str] = mapped_column(String(100), nullable = False)
    days_of_week: Mapped[str] = mapped_column(String(7), nullable = False)
    status: Mapped[bool] = mapped_column(Boolean, default = False)
    created_date: Mapped[int] = mapped_column(Integer)
    experience_points: Mapped[int] = mapped_column(Integer, default = 10) 



async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
