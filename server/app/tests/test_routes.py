import pytest
import uuid
from app import create_app
from flask_jwt_extended import decode_token

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def generate_unique_user():
    unique_str = str(uuid.uuid4())[:8]
    return {
        "username": f"testuser_{unique_str}",
        "email": f"testuser_{unique_str}@example.com",
        "password": "password123"
    }

global_token = {}
global_user = {}

def test_signup(client):
    user_data = generate_unique_user()
    response = client.post("/auth/signup", json=user_data)
    assert response.status_code == 201
    data = response.get_json()
    assert "user_id" in data or "message" in data
    global_user["user_id"] = data.get("user_id") or data.get("id")
    global_user["email"] = user_data["email"]

def test_login(client):
    login_data = {
        "email": global_user["email"],
        "password": "password123"
    }
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    data = response.get_json()
    assert "token" in data
    assert "user_id" in data
    global_token["token"] = data["token"]
    global_token["user_id"] = data["user_id"]

def auth_header():
    return {"Authorization": f"Bearer {global_token['token']}"}

def test_get_user_by_id(client):
    response = client.get(f"/users/{global_token['user_id']}", headers=auth_header())
    assert response.status_code == 200
    assert "username" in response.get_json()

def test_update_user(client):
    response = client.put(f"/users/{global_token['user_id']}", headers=auth_header(), json={
        "username": "updateduser"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Utilisateur mis à jour avec succès"

def test_delete_user(client):
    response = client.delete(f"/users/{global_token['user_id']}", headers=auth_header())
    assert response.status_code == 200
    assert response.get_json()["message"] == "Utilisateur supprimé avec succès"
