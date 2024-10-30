import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from app import main
from unittest.mock import patch
import uuid

client = TestClient(main.app)

@pytest.fixture
def sample_user_data():
    return {
        "name": "Test User",
        "email": f"user{uuid.uuid4()}@example.com",
        "password": "TestPassword123",
        "role": "user",
        "number": "1234567890"
    }

# @pytest.mark.asyncio
# async def test_create_user_success(sample_user_data):
#     async with AsyncClient(app=main.app, base_url="http://test") as ac:
#         response = await ac.post("/users", json=sample_user_data)
#     assert response.status_code == 201
#     response_data = response.json()
#     assert response_data["name"] == sample_user_data["name"]
#     assert response_data["email"] == sample_user_data["email"]
#     assert response_data["role"] == sample_user_data["role"]

# @pytest.mark.asyncio
# async def test_create_user_duplicate_email(sample_user_data):
#     async with AsyncClient(app=main.app, base_url="http://test") as ac:
#         # First create the user
#         await ac.post("/users", json=sample_user_data)
#         # Try to create the same user again
#         response = await ac.post("/users", json=sample_user_data)
#     assert response.status_code == 409
#     assert response.json()["detail"] == "User with this email already exists."

# @pytest.mark.asyncio
# async def test_create_user_missing_field():
#     data = {
#         "name": "Test User",
#         "password": "TestPassword123",
#         "role": "user",
#         "number": "1234567890"
#     }  # Email is missing
#     async with AsyncClient(app=main.app, base_url="http://test") as ac:
#         response = await ac.post("/users", json=data)
#     assert response.status_code == 422
#     assert "Validation error occurred." in response.json()["detail"]

 # Assuming `app` is defined in main.py

@pytest.mark.asyncio
async def test_create_user_success(sample_user_data):
    async with AsyncClient(app=main.app, base_url="http://test") as ac:
        response = await ac.post("/users", json=sample_user_data)
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["username"] == sample_user_data["username"]
    assert response_data["email"] == sample_user_data["email"]

@pytest.mark.asyncio
async def test_create_user_duplicate_email(sample_user_data):
    async with AsyncClient(app=main.app, base_url="http://test") as ac:
        # First create the user
        await ac.post("/users", json=sample_user_data)
        # Try to create the same user again
        response = await ac.post("/users", json=sample_user_data)
    assert response.status_code == 409  # Status code for "Conflict"
    assert response.json()["detail"] == "User with this email already exists"

@pytest.mark.asyncio
async def test_create_user_missing_email():
    data = {
        "name": "Test User",
        "password": "TestPassword123",
        "role": "user",
        "number": "1234567890"
    }  # Email is missing
    async with AsyncClient(app=main.app, base_url="http://test") as ac:
        response = await ac.post("/users", json=data)
    assert response.status_code == 422  # Status code for "Unprocessable Entity"
    assert response.json()["detail"] == "User data validation failed: Missing required fields"

@pytest.mark.asyncio
async def test_create_user_missing_name():
    data = {
        "email": "testuser@example.com",
        "password": "TestPassword123",
        "role": "user",
        "number": "1234567890"
    }  # Name is missing
    async with AsyncClient(app=main.app, base_url="http://test") as ac:
        response = await ac.post("/users", json=data)
    assert response.status_code == 422  # Status code for "Unprocessable Entity"
    assert response.json()["detail"] == "User data validation failed: Missing required fields"


# @pytest.mark.asyncio
# async def test_read_user_success(sample_user_data):
#     async with AsyncClient(app=main.app, base_url="http://test") as ac:
#         # First, create the user
#         response = await ac.post("/users", json=sample_user_data)
#         user_id = response.json()["id"]
#         # Then, read the user
#         response = await ac.get(f"/users/{user_id}")
#     assert response.status_code == 200
#     response_data = response.json()
#     assert response_data["id"] == user_id
#     assert response_data["name"] == sample_user_data["name"]

# @pytest.mark.asyncio
# async def test_read_user_not_found():
#     user_id = str(uuid.uuid4())
#     async with AsyncClient(app=main.app, base_url="http://test") as ac:
#         response = await ac.get(f"/users/{user_id}")
#     assert response.status_code == 404
#     assert response.json()["detail"] == f"User with ID {user_id} not found."



@pytest.mark.asyncio
async def test_read_user_success(sample_user_data):
    async with AsyncClient(app=main.app, base_url="http://test") as ac:
        # First, create the user
        response = await ac.post("/users", json=sample_user_data)
        user_id = response.json()["id"]
        # Then, read the user
        response = await ac.get(f"/users/{user_id}")
    
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == user_id
    assert response_data["name"] == sample_user_data["name"]

@pytest.mark.asyncio
async def test_read_user_not_found():
    user_id = str(uuid.uuid4())
    async with AsyncClient(app=main.app, base_url="http://test") as ac:
        response = await ac.get(f"/users/{user_id}")
    
    assert response.status_code == 404  # Status code for "Not Found"
    assert response.json()["detail"] == "User not found"  # Expected message from the exception


# @pytest.mark.asyncio
# async def test_update_user_success(sample_user_data):
#     async with AsyncClient(app=main.app, base_url="http://test") as ac:
#         # First, create the user
#         response = await ac.post("/users", json=sample_user_data)
#         user_id = response.json()["id"]
#         # Then, update the user's name and role
#         update_data = {"name": "Updated Name", "role": "admin"}
#         response = await ac.put(f"/users/{user_id}", json=update_data)
#     assert response.status_code == 200
#     assert response.json()["name"] == "Updated Name"
#     assert response.json()["role"] == "admin"

# @pytest.mark.asyncio
# async def test_update_user_not_found():
#     user_id = str(uuid.uuid4())
#     update_data = {"name": "Updated Name"}
#     async with AsyncClient(app=main.app, base_url="http://test") as ac:
#         response = await ac.put(f"/users/{user_id}", json=update_data)
#     assert response.status_code == 404
#     assert response.json()["detail"] == f"User with ID {user_id} not found."

# @pytest.mark.asyncio
# async def test_update_user_invalid_email(sample_user_data):
#     async with AsyncClient(app=main.app, base_url="http://test") as ac:
#         # First, create the user
#         response = await ac.post("/users", json=sample_user_data)
#         user_id = response.json()["id"]
#         # Attempt to update with invalid email format
#         update_data = {"email": "invalid-email"}
#         response = await ac.put(f"/users/{user_id}", json=update_data)
#     assert response.status_code == 422
#     assert "Validation error occurred." in response.json()["detail"]

# @pytest.mark.asyncio
# async def test_delete_user_success(sample_user_data):
#     async with AsyncClient(app=main.app, base_url="http://test") as ac:
#         # First, create the user
#         response = await ac.post("/users", json=sample_user_data)
#         user_id = response.json()["id"]
#         # Then, delete the user
#         response = await ac.delete(f"/users/{user_id}")
#     assert response.status_code == 204

import uuid
import pytest
from httpx import AsyncClient
from fastapi import FastAPI

# Assume main is the FastAPI app with appropriate routes

@pytest.mark.asyncio
async def test_update_user_not_found():
    user_id = str(uuid.uuid4())  # Generate a random UUID
    update_data = {"name": "Updated Name"}
    async with AsyncClient(app=main.app, base_url="http://test") as ac:
        response = await ac.put(f"/users/{user_id}", json=update_data)
    assert response.status_code == 404
    assert response.json()["detail"] == f"User with ID {user_id} not found."


@pytest.mark.asyncio
async def test_update_user_invalid_email(sample_user_data):
    async with AsyncClient(app=main.app, base_url="http://test") as ac:
        # First, create the user
        response = await ac.post("/users", json=sample_user_data)
        user_id = response.json()["id"]
        # Attempt to update with invalid email format
        update_data = {"email": "invalid-email"}
        response = await ac.put(f"/users/{user_id}", json=update_data)
    assert response.status_code == 422
    assert "Validation error occurred." in response.json()["detail"]


@pytest.mark.asyncio
async def test_update_user_success(sample_user_data):
    async with AsyncClient(app=main.app, base_url="http://test") as ac:
        # First, create the user
        response = await ac.post("/users", json=sample_user_data)
        user_id = response.json()["id"]

        # Attempt to update the user with valid data
        update_data = {
            "name": "Updated Name",
            "email": "updated_email@example.com",
            "role": "admin",
            "number": "0987654321"
        }
        response = await ac.put(f"/users/{user_id}", json=update_data)

        assert response.status_code == 200
        updated_user = response.json()
        assert updated_user["id"] == user_id
        assert updated_user["name"] == update_data["name"]
        assert updated_user["email"] == update_data["email"]


@pytest.mark.asyncio
async def test_update_user_no_fields(sample_user_data):
    async with AsyncClient(app=main.app, base_url="http://test") as ac:
        # First, create the user
        response = await ac.post("/users", json=sample_user_data)
        user_id = response.json()["id"]

        # Attempt to update with no fields provided
        update_data = {}  # No fields at all
        response = await ac.put(f"/users/{user_id}", json=update_data)

        assert response.status_code == 422
        assert "Validation error occurred." in response.json()["detail"]



# @pytest.mark.asyncio
# async def test_delete_user_not_found():
#     user_id = str(uuid.uuid4())
#     async with AsyncClient(app=main.app, base_url="http://test") as ac:
#         response = await ac.delete(f"/users/{user_id}")
#     assert response.status_code == 404
#     assert response.json()["detail"] == f"User with ID {user_id} not found."

@pytest.mark.asyncio
async def test_delete_user_not_found():
    user_id = str(uuid.uuid4())
    async with AsyncClient(app=main.app, base_url="http://test") as ac:
        response = await ac.delete(f"/users/{user_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == f"User with ID {user_id} not found."

@pytest.mark.asyncio
async def test_delete_user_success(sample_user_data):
    async with AsyncClient(app=main.app, base_url="http://test") as ac:
        # First, create the user
        response = await ac.post("/users", json=sample_user_data)
        user_id = response.json()["id"]
        
        # Now, delete the user
        response = await ac.delete(f"/users/{user_id}")
        
        # Check if deletion was successful
        assert response.status_code == 200
        assert response.json()["detail"] == f"User with ID {user_id} deleted successfully."

@pytest.mark.asyncio
async def test_delete_user_invalid_id():
    user_id = "1234"
    async with AsyncClient(app=main.app, base_url="http://test") as ac:
        response = await ac.delete(f"/users/{user_id}")
    assert response.status_code == 400  # Assuming you return 400 for bad request
    assert response.json()["detail"] == "Invalid user ID format."
