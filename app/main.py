from fastapi import FastAPI
from app.database import Base, engine
from app.exception.custom_exceptions import AppException
from app.exception.handlers import app_exception_handler
from app.models.task import Task
from app.models.user import User
from app.routes.task import router as task_router
from app.routes.auth import router as auth_router
app = FastAPI()

app.include_router(task_router)
app.include_router(auth_router)
 
app.add_exception_handler(
    AppException,
    app_exception_handler
)
@app.get('/')
def hello():
    return {"message":"hello I am working bro"}