import time
import logging 
from fastapi import FastAPI, Request
from app.database import Base, engine
from app.exception.custom_exceptions import AppException
from app.exception.handlers import app_exception_handler
from app.models.task import Task
from app.models.user import User
from app.routes.task import router as task_router
from app.routes.auth import router as auth_router


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(task_router)
app.include_router(auth_router)
 
app.add_exception_handler(
    AppException,
    app_exception_handler
)
@app.middleware('http')
async def log_requests(request: Request, call_next):
    start_time = time.time()
    logger.info(f"Request Started: {request.method} {request.url.path}")
    response = await call_next(request)
    process_time = time.time() - start_time

    logger.info(
        f"Request completed: {request.method} {request.url.path} "
        f"status: {response.status_code} "
        f"Time: {process_time:.4f}s"
        )
    return response


@app.get('/')
def hello():
    return {"message":"hello I am working bro"}