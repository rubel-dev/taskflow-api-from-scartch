
from sqlalchemy.orm import Session
from app.repository import project_repository


def create_project_service(
        project,
        user_id:int,
        db: Session
):
    return project_repository.create_project(
        project=project,
        user_id=user_id,
        db = db
    )