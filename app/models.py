from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from typing import Optional

class User(BaseModel):
    name: str=Field(...,description="Name is required")
    email: EmailStr=Field(...,description="Email is required")
    role: str
    number: str

class UserUpdate(BaseModel):
    name: Optional[str]
    role: Optional[str]
    number: Optional[str]

