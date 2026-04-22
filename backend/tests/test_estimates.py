from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def get_token():
    response = client.post("/login", json={"username": "admin", "password": "Admin123"})
    return response.json()["access_token"]

def test_login():
    response = client.post("/login", json={"username": "admin", "password": "Admin123"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_create_estimate():
    token = get_token()
    response = client.post("/estimates", 
        json={
            "customer_name": "Juan Perez",
            "vehicle_model": "Toyota Corolla",
            "vehicle_year": 2015,
            "vehicle_mileage": 60000,
            "repair_description": "Brake replacement",
            "estimated_cost": 300.0
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["customer_name"] == "Juan Perez"
    assert response.json()["status"] == "pending"

def test_list_estimates():
    token = get_token()
    response = client.get("/estimates", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)