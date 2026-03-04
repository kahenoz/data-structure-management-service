from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_create_data_elements():
    # Create dataset first
    dataset_payload = {
        "name": "customers_elements",
        "description": "Customer dataset",
        "constraints": None,
        "indexes": []
    }

    dataset_res = client.post("/api/v1/datasets", json=dataset_payload)
    assert dataset_res.status_code == 200

    dataset_id = dataset_res.json()["id"]

    payload = [
        {
            "name": "email",
            "data_type": "string",
            "foreign_key": None,
            "not_null": True,
            "default": None,
            "is_pii": True
        },
        {
            "name": "created_at",
            "data_type": "timestamp",
            "foreign_key": None,
            "not_null": True,
            "default": None,
            "is_pii": False
        }
    ]

    response = client.post(
        f"/api/v1/datasets/{dataset_id}/elements",
        json=payload
    )

    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "email"
    assert data[1]["name"] == "created_at"

def test_create_elements_dataset_not_found():
    payload = [
        {
            "name": "email",
            "data_type": "string",
            "foreign_key": None,
            "not_null": True,
            "default": None,
            "is_pii": True
        }
    ]

    response = client.post("/api/v1/datasets/999999/elements", json=payload)

    assert response.status_code == 404
    assert response.json()["detail"] == "Dataset not found"

def test_create_duplicate_data_element():
    # Create dataset
    dataset_payload = {
        "name": "orders_elements",
        "description": "Orders dataset",
        "constraints": None,
        "indexes": []
    }

    dataset_res = client.post("/api/v1/datasets", json=dataset_payload)
    assert dataset_res.status_code == 200

    dataset_id = dataset_res.json()["id"]

    element_payload = [
        {
            "name": "order_id",
            "data_type": "integer",
            "foreign_key": None,
            "not_null": True,
            "default": None,
            "is_pii": False
        }
    ]

    # First creation
    res1 = client.post(
        f"/api/v1/datasets/{dataset_id}/elements",
        json=element_payload
    )
    assert res1.status_code == 200

    # Second creation (duplicate)
    res2 = client.post(
        f"/api/v1/datasets/{dataset_id}/elements",
        json=element_payload
    )

    assert res2.status_code == 400
    assert res2.json()["detail"] == "Data element 'order_id' already exists in dataset"
