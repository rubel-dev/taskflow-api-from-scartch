from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependency import get_db
from app.auth.dependencies import require_admin
from app.models.user import User
from app.models.task import Task
from app.exception.custom_exceptions import NotFoundException

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/users")
def get_all_users(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    return db.query(User).all()


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise NotFoundException("User not found")

    db.delete(user)
    db.commit()
    return


@router.patch("/users/{user_id}/promote")
def promote_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise NotFoundException("User not found")

    user.role = "admin"
    db.commit()
    db.refresh(user)

    return user


@router.patch("/users/{user_id}/demote")
def demote_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise NotFoundException("User not found")

    user.role = "user"
    db.commit()
    db.refresh(user)

    return user


@router.get("/tasks")
def get_all_tasks(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    return db.query(Task).all()


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_any_task(
    task_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise NotFoundException("Task not found")

    db.delete(task)
    db.commit()
    return