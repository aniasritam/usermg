import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models import User
from app.schemas import UserCreate, UserResponse
from app.services import UserService

client = TestClient(app)

@pytest.fixture
def user_data():
    return {
        "id":"1",
        "email": "test@example.com",
        "name": "Test User",
        "password": "password123"
    }

def test_create_user(user_data, mocker):
    mocker.patch.object(UserService, 'create_user', return_value=User(**user_data))
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    assert response.json() == user_data

def test_read_user(user_data, mocker):
    user_id = user_data["email"]
    mocker.patch.object(UserService, 'get_user', return_value=User(**user_data))
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json() == user_data

def test_update_user(user_data, mocker):
    user_id = user_data["email"]
    updated_data = user_data.copy()
    updated_data["name"] = "Updated User"
    mocker.patch.object(UserService, 'update_user', return_value=User(**updated_data))
    response = client.put(f"/users/{user_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json() == updated_data

def test_delete_user(user_data, mocker):
    user_id = user_data["email"]
    mocker.patch.object(UserService, 'delete_user', return_value=None)
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json() == {"detail": "User deleted"}


def test_create_user_no_data():
    response = client.post("/users/", json={})
    assert response.status_code == 422  # Unprocessable Entity
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "user_create"],
                "msg": "field required",
                "type": "value_error.missing"
            }
        ]
    }

def test_update_user_no_data(user_data):
    user_id = user_data["email"]
    response = client.put(f"/users/{user_id}", json={})
    assert response.status_code == 422  # Unprocessable Entity
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "user_create"],
                "msg": "field required",
                "type": "value_error.missing"
            }
        ]
    }

def test_create_user(user_data, mocker):
    mocker.patch.object(UserService, 'create_user', return_value=User(**user_data))
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    assert response.json() == user_data

def test_create_user_existing_email(user_data, mocker):
    mocker.patch.object(UserService, 'create_user', side_effect=Exception("User already exists"))
    response = client.post("/users/", json=user_data)
    assert response.status_code == 400
    assert response.json() == {"detail": "User already exists"}

def test_read_user(user_data, mocker):
    user_id = user_data["email"]
    mocker.patch.object(UserService, 'get_user', return_value=User(**user_data))
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json() == user_data

def test_read_user_not_found(user_data, mocker):
    user_id = user_data["email"]
    mocker.patch.object(UserService, 'get_user', side_effect=Exception("User not found"))
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}