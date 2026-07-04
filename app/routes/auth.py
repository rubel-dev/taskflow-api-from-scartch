from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security import create_access_token, hash_password, refresh_access_token, verify_password
from app.dependency import get_db
from app.exception.custom_exceptions import InvalidCredentialsException
from app.models.user import User
from app.schemas.auth import RefreshTokenRequest, UserCreated, UserLogin
from app.services.auth_service import refresh_access_tokens_services

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
        raise InvalidCredentialsException("Invalid Credentials")
    is_password = verify_password(
        user.password,
        db_user.password
    )
    if not is_password:
        raise InvalidCredentialsException("Invalid Credentials")
    access_token = create_access_token(
        {
            "user_id":db_user.id
        }
    )
    refresh_token = refresh_access_token(
        {
            "user_id":db_user.id
        }
    )
    
    return  {
        "acess_token": access_token,
        "refresh_token":refresh_token,
        "token_type":"bearer"
    }

@router.post('/refresh')
def refresh_token(request: RefreshTokenRequest):
    return refresh_access_tokens_services(
        request.refresh_token
    )