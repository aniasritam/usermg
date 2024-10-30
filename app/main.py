from fastapi import FastAPI, HTTPException
from app.models import User
from app.schemas import UserCreate, UserResponse
from app.services import UserService

app = FastAPI()

@app.post("/users", response_model=UserResponse)
def create_user(user_create: UserCreate):
    user = User(id=user_create.email, **user_create.dict())  # Use email as a unique id
    return UserService.create_user(user)

@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: str):
    try:
        return UserService.get_user(user_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: str, user_create: UserCreate):
    user = User(id=user_id, **user_create.dict())  # Maintain the user_id as the unique id
    try:
        return UserService.update_user(user_id, user)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.delete("/users/{user_id}")
def delete_user(user_id: str):
    try:
        UserService.delete_user(user_id)
        return {"detail": "User deleted"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
