from contextlib import asynccontextmanager
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.models import init_db
import database.requests as rq


@asynccontextmanager
async def lifespan(app_: FastAPI):
    await init_db()
    print("Bot is ready")
    yield


app = FastAPI(title = "ToDo App", lifespan = lifespan)


app.add_middleware(
    CORSMiddleware, # Безопасность
    allow_origins = ["*"], # url адресс отправленных запросов
    allow_credentials = True, 
    allow_methods = ["*"],
    allow_headers = ["*"]
)


@app.get("/api/tasks/{tgId}")
async def getTasks(tgId: int):
    user = await rq.setUser(tgId)
    return await rq.getTask(user.id)


@app.get("api/profile/{tgId}")
async def getProfile(tgId: int):
    user = await rq.setUser(tgId)
    completedTasksCounter = await rq.getCompletedTasksCounter(user.id)
    return {"completedTasksCounter": completedTasksCounter}
