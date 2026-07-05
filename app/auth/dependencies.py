


from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from app.core.security import ALGORITHM
from jose import JWTError, jwt

from app.core.setting import ACCESS_SECRET_KEY
from app.dependency import get_db
from app.exception.custom_exceptions import ForbiddenException, UnauthorizedException
from app.models.user import User

security = HTTPBearer()
def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db:Session = Depends(get_db)
):
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            ACCESS_SECRET_KEY,
            algorithms = [ALGORITHM]
        )
        user_id = payload.get('user_id')
        if user_id is None:
            raise UnauthorizedException("Invalid token")
        user = db.query(User).filter(
            User.id == user_id
        ).first()
        if not user:
            raise UnauthorizedException("user not found")
        return user
    except JWTError:
        raise UnauthorizedException("Invalid token")


def require_admin(
        current_user: User = Depends(get_current_user)
):
    if current_user.role != 'admin':
        raise ForbiddenException("Admin access required")
    return current_user