from fastapi import FastAPI, HTTPException
from app.models import User,UserUpdate
from app.schemas import UserCreate, UserResponse
from app.services import UserService

app = FastAPI()

@app.post("/users", response_model=UserResponse)
def create_user(user_create: UserCreate):
    user = User(id=user_create.email, **user_create.dict())  # Use email as a unique id
    return UserService.create_user(user)

@app.get("/users/{email}", response_model=User)
def read_user(email: str):
    try:
        return UserService.get_user(email)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.put("/users/{email}", response_model=UserUpdate)
def update_user(email: str, user_create: UserUpdate):
    user = User(email=email, **user_create.dict())  # Maintain the user_id as the unique id
    try:
        return UserService.update_user(email, user)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.delete("/users/{email}")
def delete_user(email: str):
    try:
        UserService.delete_user(email)
        return {"detail": "User deleted"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
