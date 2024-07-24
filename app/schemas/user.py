from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    hashed_password: str

class UserResponse(UserCreate):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
