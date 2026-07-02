

from app.models.task import Task

def create_task(
        task,
        user_id,
        db
):
    new_task = Task(
        title=task.title,
        description=task.description,
        user_id=user_id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


def get_task_by_id_and_user(
    task_id,
    user_id,
    db
):
    task = db.query(Task).filter(Task.id == task_id , Task.user_id == user_id).first()
    return task

def get_task_by_user(
        completed,
        search,
        skip,
        limit,
        db,
        user_id
):
    task = db.query(Task).filter(Task.user_id == user_id)
    if completed is not None:
        task = task.filter(Task.completed==completed)
    if search:
        task = task.filter(Task.title.ilike(f"%{search}%"))
    task = task.offset(skip).limit(limit).all() 
    return task

def update_task(
    task,
    task_db,
    db
):
    task_db.title = task.title
    task_db.description = task.description
    task_db.completed = task.completed
    db.commit()
    db.refresh(task_db)
    return task_db

def delete_task(
    task,
    db
):
    db.delete(task)
    db.commit()