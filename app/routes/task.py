from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependency import get_db
from app.models.user import User
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.models.task import Task
from app.auth.dependencies import get_current_user
from app.services.task_service import create_task_service, delete_task_service, get_task_service, get_tasks_service,  update_task_service
router = APIRouter()

@router.post('/task', response_model=TaskResponse)
def create_task(
    task: TaskCreate,
    db:Session = Depends(get_db),
    cureent_user:User = Depends(get_current_user)
):
   return create_task_service(
       task= task,
       user_id=cureent_user.id,
       db = db
   )

@router.get('/tasks', response_model=list[TaskResponse])
def get_tasks(
    completed:bool|None=None,
    search:str|None = None,
    skip:int = 0,
    limit:int=10,
    db:Session = Depends(get_db),
    cureent_user:User = Depends(get_current_user)
):
    return get_tasks_service(
        completed=completed,
        search = search,
        skip = skip,
        limit = limit,
        db = db,
        user_id = cureent_user.id
    )


@router.get('/tasks/{task_id}', response_model=TaskResponse)
def get_task(
    task_id:int,
    db:Session = Depends(get_db),
    cureent_user:User = Depends(get_current_user)
):
    return get_task_service(
        task_id=task_id,
        db = db,
        user_id = cureent_user.id
    )



@router.put('/tasks/{task_id}', response_model=TaskResponse)
def update_task(
    task_id:int,
    task:TaskUpdate,
    db:Session = Depends(get_db), 
    cureent_user:User = Depends(get_current_user)
):
   return update_task_service(
       task_id=task_id,
       task= task,
       db = db,
       user_id = cureent_user.id
   )

@router.delete('/tasks/{task_id}', status_code=204)
def delete_task(
    task_id:int,
    db:Session = Depends(get_db),
    cureent_user:User = Depends(get_current_user)
):
   return delete_task_service(
      task_id = task_id,
      db = db,
      user_id = cureent_user.id
   )
    
    
