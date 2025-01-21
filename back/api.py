from contextlib import asynccontextmanager
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from models import init_db
import requestsdb as rq


class AddTask(BaseModel):
    tgId: int
    text: str


class CompleteTask(BaseModel):
    id: int


@asynccontextmanager
async def lifespan(app_: FastAPI):
    await init_db()
    print("Bot is ready")
    yield


app = FastAPI(title = "ToDo App", lifespan = lifespan)

app.mount("/images", StaticFiles(directory="images"), name="images")


app.add_middleware(
    CORSMiddleware, # Безопасность
    allow_origins = ["*"], # url адресс отправленных запросов
    allow_credentials = True, 
    allow_methods = ["*"],
    allow_headers = ["*"]
)



@app.get("/")
def read_root():
    return {"message": "Welcome to the Task Tracker API"}


@app.get("/api/tasks/{tgId}")
async def getTasks(tgId: int):
    user = await rq.setUser(tgId)
    return await rq.getTask(user.id)


@app.get("/api/profile/{tgId}")
async def getProfile(tgId: int):
    # Убедимся, что пользователь существует
    user = await rq.setUser(tgId)
    # Получаем или создаём профиль
    profile = await rq.getProfile(user.id)
    image_path = f"images/{profile.race}/{profile.sex}/{profile.clas}/{profile.avatar}"
    # Возвращаем профиль в формате JSON
    return {
        "user_name": profile.user_name,
        "race": profile.race,
        "sex": profile.sex,
        "clas": profile.clas,
        "image_path": image_path
    }


@app.post("/api/add")
async def addTask(task: AddTask):
    user = await rq.setUser(task.tgId)
    await rq.addTask(user.id, task.text)
    return {"status": "ok"}


@app.patch("/api/completed")
async def markAsCompleted(task: CompleteTask):
    await rq.markAsCompleted(task.id)
    return {"status": "ok"}