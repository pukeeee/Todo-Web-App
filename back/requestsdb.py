from sqlalchemy import select, update, delete, func
from models import async_session, User, Task
from pydantic import BaseModel, ConfigDict



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
            
        new_user = User(tgId = tgId)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user



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
        tasks = await session.scalars(select(Task).where(Task.user == userId, Task.status == False))
        
        serialized_tasks = [
            TaskSchema.model_validate(t).model_dump() for t in tasks
        ]
        
        return serialized_tasks



async def getCompletedTasksCounter(userId):
    async with async_session() as session:
        return await session.scalar(select(func.count(Task.id)).where(Task.status == True, Task.user == userId))