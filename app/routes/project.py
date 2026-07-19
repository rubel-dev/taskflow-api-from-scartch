 
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.dependency import get_db
from app.schemas.project import ProjectCreate, ProjectResponse
from app.services import project_service

router = APIRouter(
    prefix="/projects",
    tags = ["Projects"]
)

@router.post(
    "/",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED
)
def create_project(
    project: ProjectCreate,
    db:Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return project_service.create_project_service(
        project=project,
        user_id=current_user.id,
        db = db
    )
