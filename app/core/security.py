from passlib.context import CryptContext
from datetime import datetime, timedelta, UTC
from app.core.setting import (
    ACCESS_SECRET_KEY,
    ALGORITHM,
    REFRESH_SECRET_KEY
)
from jose import JWTError, jwt


def create_token(
        data: dict,
        secret_key: str,
        expire_minuts: int
):
    to_encdoe = data.copy()
    expire = datetime.now(UTC) + timedelta(
        minutes= expire_minuts
    )
    to_encdoe.update({"exp":expire})

    return jwt.encode(
        to_encdoe,
        secret_key,
        algorithm=ALGORITHM
    )
ACCESS_TOKEN_EXPIRE_MINUTES = 30
def create_access_token(data: dict):
    return create_token(
        data= data,
        secret_key= ACCESS_SECRET_KEY,
        expire_minuts= ACCESS_TOKEN_EXPIRE_MINUTES
    )

REFRESH_TOKEN_EXPIRE_DAYS = 30
def refresh_access_token(data: dict):
    return create_token(
        data= data,
        secret_key= REFRESH_SECRET_KEY,
        expire_minuts= REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60
    )


# def create_access_token(data: dict):
#     to_encode = data.copy()
#     expire = datetime.now(UTC)+timedelta(hours = 1)
#     to_encode.update({"exp":expire})

#     encoded_jwt = jwt.encode(
#         to_encode,
#         SECRET_KEY,
#         ALGORITHM
#     )
#     return encoded_jwt

pwd_context = CryptContext(
    schemes=['bcrypt'],
    deprecated = "auto"
)

def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(
        plain_password,
        hashed_password
):
    return pwd_context.verify(plain_password, hashed_password)

 
def verify_refresh_token(token:str):
    try:
        payload = jwt.decode(
            token,
            REFRESH_SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        user_id = payload.get('user_id')
        if user_id is None:
            return None
        return user_id
    except JWTError:
        return None