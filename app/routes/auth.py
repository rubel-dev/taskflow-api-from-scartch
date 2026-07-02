from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security import create_access_token, hash_password, verify_password
from app.dependency import get_db
from app.models.user import User
from app.schemas.auth import UserCreated, UserLogin

router = APIRouter()


@router.post('/register')
def register(
    user: UserCreated,
    db:Session = Depends(get_db)
):
    new_user = User(
        username = user.username,
        email = user.email,
        password = hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post('/login')
def login(
    user: UserLogin,
    db:Session = Depends(get_db) 
):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        raise HTTPException(
            status_code=400,
            message= 'Invalid Credentials'
        )
    is_password = verify_password(
        user.password,
        db_user.password
    )
    if not is_password:
        raise HTTPException(
            status_code=400,
            message= 'Invalid Credentials'
        )
    token = create_access_token(
        {
            "user_id":db_user.id
        }
    )
    
    return {"Bearar":token}

    