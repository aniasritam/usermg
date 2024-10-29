from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    role: str
    number: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: str
    number: str
