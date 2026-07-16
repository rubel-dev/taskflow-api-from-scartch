
from fastapi import HTTPException

from app.exception.custom_exceptions import NotFoundException
from app.models.project import Project
from app.models.task import Task
from app.repository import task_repository


def create_task_service(
        task,
        user_id,
        db
): 
    project= db.query(Project).filter(
        Project.id == task.project_id,
        Project.user_id == user_id
    ).first()
    if not project:
        raise NotFoundException("Project Not Found")
    
    return task_repository.create_task(task, user_id, db) 

def get_tasks_service(
        completed,
        search,
        skip,
        limit,
        db,
        user_id
):  
    return task_repository.get_task_by_user(
        completed,
        search,
        skip,
        limit,
        db,
        user_id
    ) 

def get_task_service(
        task_id,
        db,
        user_id
):
    task = task_repository.get_task_by_id_and_user(
        task_id,
        user_id,
        db
    )
    if not task:
        raise NotFoundException("Task Not Found") 
    return task


def update_task_service(
        task_id,
        task,
        db,
        user_id
):
    task_db = task_repository.get_task_by_id_and_user(task_id, user_id, db) 
    if not task_db:
        raise NotFoundException("Task Not Found") 
    return task_repository.update_task(
        task,
        task_db,
        db
    )  

def delete_task_service(
        task_id,
        db,
        user_id
):
    task = task_repository.get_task_by_id_and_user(task_id, user_id, db) 
    if not task:
        raise NotFoundException("Task Not Found")
        
    task_repository.delete_task(task, db)