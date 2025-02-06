from contextlib import asynccontextmanager
from pydantic import BaseModel
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from models import init_db
import requestsdb as rq


class AddTask(BaseModel):
    tgId: int
    text: str


class CompleteTask(BaseModel):
    id: int

class DeleteTask(BaseModel):
    tgId: int


class UpdateTask(BaseModel):
    tgId: int
    text: str


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
    allow_headers = ["*"],
    expose_headers=["Content-Type"]
)

@app.middleware("http")
async def add_csp_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["Content-Security-Policy"] = "default-src 'self'; img-src 'self' data:;"
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Referrer-Policy"] = "no-referrer"
    return response



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
    
    # Возвращаем профиль в формате JSON
    return {
        "user_name": profile.user_name,
        "race": profile.race,
        "clas": profile.clas
    }



@app.delete("/api/tasks/delete/{taskId}")
async def deleteTask(taskId: int, body: DeleteTask):
    deletedTaskId = await rq.deleteTask(taskId, body.tgId)
    print(f"Received taskId: {taskId}, tgId: {body.tgId}")
    if deletedTaskId:
        return {"status": "Task deleted successfully"}
    else:
        raise HTTPException(status_code = 404, detail = f"Task {deletedTaskId} not found")



@app.post("/api/task/add")
async def addTask(task: AddTask):
    user = await rq.setUser(task.tgId)
    await rq.addTask(user.id, task.text)
    return {"status": "ok"}


@app.patch("/api/completed")
async def markAsCompleted(task: CompleteTask):
    await rq.markAsCompleted(task.id)
    return {"status": "ok"}



@app.patch("/api/tasks/update/{taskId}")
async def updateTask(taskId: int, body: UpdateTask):
    await rq.updateTask(taskId, body.tgId, body.text)
    return {"status": "ok"}