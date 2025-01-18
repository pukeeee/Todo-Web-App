from sqlalchemy import select, update, delete, func
from models import async_session, User, Task
from pydantic import BaseModel, ConfigDict
from typing import List



class TaskSchema(BaseModel):
    id: int
    user: int
    title: str
    status: bool
    
    model_config = ConfigDict(from_attributes = True)



async def setUser(tgId):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tgId == tgId))
        
        if not user:
            new_user = User(tgId = tgId)
            session.add(new_user)
            await session.comit()
            await session.refresh(new_user)
            return new_user
        
        return user


async def addTask(tgId):
    async with async_session() as session:
        pass



async def getTask(userId):
    async with async_session() as session:
        tasks = await session.scalars(select(Task).where(Task.user == userId, Task.status == False))
        
        serialized_tasks = [
            TaskSchema.model_validate(t).model_dump() for t in tasks
        ]
        
        return serialized_tasks



async def getCompletedTasksCounter(userId):
    async with async_session() as session:
        return await session.scalar(select(func.count(Task.id)).where(Task.status == True, Task.user == userId))
        
        