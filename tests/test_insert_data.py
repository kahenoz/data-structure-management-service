from fastapi.testclient import TestClient
from app import app
from dataset_payloads import datasets_payload, elements_payload

client = TestClient(app)

dataset_ids = {}

# Create datasets
for ds in datasets_payload:
    res = client.post("/api/v1/datasets", json=ds)
    assert res.status_code == 200, f"Failed to create dataset {ds['name']}"
    dataset_id = res.json()["id"]
    dataset_ids[ds["name"]] = dataset_id

# Add elements for each dataset
for ds_name, elements in elements_payload.items():
    ds_id = dataset_ids[ds_name]
    res = client.post(f"/api/v1/datasets/{ds_id}/elements", json=elements)
    assert res.status_code == 200, f"Failed to create elements for dataset {ds_name}"
    print(f"Created {len(elements)} elements for dataset {ds_name}")