from passlib.context import CryptContext
from datetime import datetime, timedelta, UTC
from app.core.setting import SECRET_KEY, ALGORITHM
from jose import jwt

 

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(UTC)+timedelta(hours = 1)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        ALGORITHM
    )
    return encoded_jwt

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