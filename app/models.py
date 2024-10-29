from pydantic import BaseModel, EmailStr
from uuid import UUID

class User(BaseModel):
    id: UUID=None
    name: str
    email: EmailStr
    role: str
    number: str
