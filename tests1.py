import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from app import main
from unittest.mock import patch
import uuid
import pytest
from httpx import AsyncClient
from fastapi import FastAPI

client = TestClient(main.app)

@pytest.fixture
def sample_user_data():
    return {
        "name": "Test User",
        "email": f"user{uuid.uuid4()}@example.com",
        "role": "user",
        "number": "1234567890"
    }

@pytest.fixture
def duplicate_email():
    return{
        "name": "Test User",
        "email":"aniruddh@gmail.com",
        "role":"sde",
        "number":"3787878787"
    }

@pytest.mark.asyncio
async def test_create_user_success(sample_user_data):
    async with AsyncClient(app=main.app, base_url="http://test") as ac:
        response = await ac.post("/users", json=sample_user_data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["name"] == sample_user_data["name"]
    assert response_data["email"] == sample_user_data["email"]

@pytest.mark.asyncio
async def test_create_user_duplicate_email(duplicate_email):
    async with AsyncClient(app=main.app, base_url="http://test") as ac:
    
        response = await ac.post("/users", json=duplicate_email)
    assert response.status_code == 400 
   

@pytest.mark.asyncio
async def test_create_user_missing_email():
    data = {
        "name": "Test User",
    
        "role": "user",
        "number": "1234567890"
    }  # Email is missing
    async with AsyncClient(app=main.app, base_url="http://test") as ac:
        response = await ac.post("/users", json=data)
    assert response.status_code == 422  # Status code for "Unprocessable Entity"
   

@pytest.mark.asyncio
async def test_create_user_missing_name():
    data = {
        "email": "testuser@example.com",
        
        "role": "user",
        "number": "1234567890"
    }  # Name is missing
    async with AsyncClient(app=main.app, base_url="http://test") as ac:
        response = await ac.post("/users", json=data)
    assert response.status_code == 422  # Status code for "Unprocessable Entity"
   




@pytest.mark.asyncio
async def test_read_user_success(sample_user_data):
    async with AsyncClient(app=main.app, base_url="http://test") as ac:
        # First, create the user
        response = await ac.post("/users", json=sample_user_data)
        email = response.json()["email"]
        # Then, read the user
        response = await ac.get(f"/users/{email}")
    
    assert response.status_code == 200
 

@pytest.mark.asyncio
async def test_read_user_not_found():
    email=f"user{uuid.uuid4()}@example.com"
    async with AsyncClient(app=main.app, base_url="http://test") as ac:
        response = await ac.get(f"/users/{email}")
    
    assert response.status_code == 404  





@pytest.mark.asyncio
async def test_update_user_not_found():
    email ="4576566@gmail.com" # Generate a random UUID
    update_data = {"name": "Update Test",
                   "role": "admin",
                   "number": "123456789"}
    async with AsyncClient(app=main.app, base_url="http://test") as ac:
        response = await ac.put(f"/users/{email}", json=update_data)
    assert response.status_code == 404
   


@pytest.mark.asyncio
async def test_update_user_invalid_email(sample_user_data):
    async with AsyncClient(app=main.app, base_url="http://test") as ac:
        # First, create the user
        response = await ac.post("/users", json=sample_user_data)
        email = response.json()["email"]
        # Attempt to update with invalid email format
        update_data = {"email": "invalid-email"}
        response = await ac.put(f"/users/{email}", json=update_data)
    assert response.status_code == 422
   


@pytest.mark.asyncio
async def test_update_user_success(sample_user_data):
    async with AsyncClient(app=main.app, base_url="http://test") as ac:
        # First, create the user
        response = await ac.post("/users", json=sample_user_data)
        email = response.json()["email"]

        # Attempt to update the user with valid data
        update_data = {
            "name": "Updated Name",
        
            "role": "admin",
            "number": "0987654321"
        }
        response = await ac.put(f"/users/{email}", json=update_data)

        assert response.status_code == 200
        


@pytest.mark.asyncio
async def test_update_user_no_fields(sample_user_data):
    async with AsyncClient(app=main.app, base_url="http://test") as ac:
        # First, create the user
        response = await ac.post("/users", json=sample_user_data)
        email= response.json()["email"]

        # Attempt to update with no fields provided
        update_data = {}  # No fields at all
        response = await ac.put(f"/users/{email}", json=update_data)

        assert response.status_code == 422
        





@pytest.mark.asyncio
async def test_delete_user_not_found():
    email="jskakajdkajk@gmail.com"
    async with AsyncClient(app=main.app, base_url="http://test") as ac:
        response = await ac.delete(f"/users/{email}")
    assert response.status_code == 404
    

@pytest.mark.asyncio
async def test_delete_user_success(sample_user_data):
    async with AsyncClient(app=main.app, base_url="http://test") as ac:
        # First, create the user
        response = await ac.post("/users", json=sample_user_data)
        email= response.json()["email"]
        
        # Now, delete the user
        response = await ac.delete(f"/users/{email}")
        
        # Check if deletion was successful
        assert response.status_code == 200
       

