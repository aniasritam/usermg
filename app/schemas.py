from pydantic import BaseModel, EmailStr, Field
from typing import Optional

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

