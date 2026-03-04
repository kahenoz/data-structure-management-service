from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_create_dataset():
    payload = {
        "name": "customers_test",
        "description": "Customer dataset",
        "constraints": {"primary_key": ["id", "name"], "unique": ["email"]},
        "indexes": []
    }

    response = client.post("/api/v1/datasets", json=payload)

    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "customers_test"
    assert data["description"] == "Customer dataset"
    assert data["constraints"] == {"primary_key": ["id", "name"], "unique": ["email"]}
    assert data["indexes"] == None


def test_create_duplicate_dataset():
    payload = {
        "name": "orders_test",
        "description": "Orders dataset",
        "constraints": None,
        "indexes": []
    }

    # First creation — should succeed
    response1 = client.post("/api/v1/datasets", json=payload)
    assert response1.status_code == 200

    # Second creation — should fail
    response2 = client.post("/api/v1/datasets", json=payload)

    assert response2.status_code == 400

    data = response2.json()
    assert data["detail"] == "Dataset with this name already exists"