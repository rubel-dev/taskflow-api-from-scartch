from sqlalchemy.orm import Session
from app.models.project import Project

def create_project(project, user_id: int, db: Session):
    new_project = Project(
        name = project.name,
        description = project.description,
        user_id = user_id
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project