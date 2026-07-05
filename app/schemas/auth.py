from pydantic import BaseModel

class UserCreated(BaseModel):
    username:str
    email:str
    password:str

class UserLogin(BaseModel):
    email:str
    password:str
class RefreshTokenRequest(BaseModel):
    refresh_token: str

class UserResponse(BaseModel):
    id:int
    username:str
    email:str
    role:str
    class Config:
        from_attributes = True