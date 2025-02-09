from sqlalchemy import select, update, delete, func
from models import async_session, User, Task, Profile
from pydantic import BaseModel, ConfigDict
import time



class TaskSchema(BaseModel):
    id: int
    user: int
    text: str
    status: bool
    
    model_config = ConfigDict(from_attributes = True)



async def setUser(tgId):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tgId == tgId))
        if user:
            return user
            
        unix_time = int(time.time())
        session.add(User(tgId = tgId, start_date = unix_time))
        await session.commit()
        return user



async def addTask(userId, text):
    async with async_session() as session:
        new_task = Task(
            text = text,
            user = userId
        )
        session.add(new_task)
        await session.commit()


async def markAsCompleted(taskId):
    async with async_session() as session:
        await session.execute(update(Task).where(Task.id == taskId).values(status = True))
        await session.commit()



async def getTask(userId):
    async with async_session() as session:
        tasks = await session.scalars(select(Task).where(Task.user == userId))
        
        serialized_tasks = [
            TaskSchema.model_validate(t).model_dump() for t in tasks
        ]
        
        return serialized_tasks



async def deleteTask(taskId: int, tgId: int) -> int:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tgId == tgId))
        if not user:
            return 0
        
        result = await session.execute(delete(Task).where(Task.id == taskId, Task.user == user.id)
                                        .returning(Task.id))
        deletedTaskId = result.scalar()
        await session.commit()
        
        return deletedTaskId if deletedTaskId else 0




async def getProfile(userId):
    async with async_session() as session:
        profile = await session.scalar(select(Profile).where(Profile.user == userId))
        if not profile:
            # Создаём новый профиль, если его нет
            new_profile = Profile(
                user=userId,  # Используем userId
                user_name="Guest",
                race="Human",
                sex="",
                clas="Exile"
            )
            session.add(new_profile)
            await session.commit()
            return new_profile  # Возвращаем созданный профиль
        
        return profile  # Возвращаем найденный профиль



async def updateTask(taskId: int, tgId: int, text: str):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tgId == tgId))
        if not user:
            return 0

        result = await session.execute(update(Task).where(Task.id == taskId, Task.user == user.id)
                                        .values(text = text)
                                        .returning(Task.id))
        updatedTaskId = result.scalar()
        await session.commit()
        
        return updatedTaskId if updatedTaskId else 0