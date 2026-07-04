


from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.security import ALGORITHM
from jose import JWTError, jwt

from app.core.setting import ACCESS_SECRET_KEY

security = HTTPBearer()
def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security)
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
            raise HTTPException(
                status_code=401,
                detail='Invalid token'
            )
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail='Invalid token'
        )