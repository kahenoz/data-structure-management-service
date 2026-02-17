## Data Model & Design Decisions
I implemented a one-to-many relationship where each Dataset can contain multiple unique DataElements. Key design decisions include:

## Uniqueness enforcement: 
Datasets are unique by both name and ID to enable retrieval by either identifier. DataElements are unique within a dataset to prevent schema ambiguity.

## Trade-off: 
This prevents duplicate columns in a dataset but requires clients to manage naming.

## Graceful error handling: 
Rather than failing silently, invalid operations (duplicate dataset, orphaned element, etc.) return descriptive error messages.

## Rich schema definition: 
The service support constraints (primary keys, unique columns) and indexes at dataset creation, plus metadata like is_pii and foreign_key at element level.

## Please run the commands on your terminal sequantially. 
## Prerequisites Python 3.12 installed on your local machine

$python3.12 --version 

$python -m venv venv

$source venv/bin/activate

$export PYTHONPATH=$PYTHONPATH:.

$pip install -r requirements.txt

$uvicorn app:app --reload


## For API docs you may visit http://127.0.0.1:8000/docs
## All the APIs have the prefix of /api/v1

## Example requests

POST http://localhost:8000/api/v1/datasets -->> Create a dataset

    {
        "name": "ordersXproducts",
        "description": "Order items linking orders and products",
        "constraints": {"primary_key": ["order_id", "product_id"], "unique": []},
        "indexes": []
    }

GET http://localhost:8000/api/v1/datasets -->> Retrieves all the datasets

GET http://localhost:8000/api/v1/datasets/{dataset_id} -->> Retrieves a dataset by id


POST http://127.0.0.1:8000/api/v1/datasets/{dataset_id}/elements -->> Create an element/elements for a dataset

    [
        {
            "name": "order_id", 
            "data_type": "integer", 
            "foreign_key": {"table": "orders", "column": "order_id"}, 
            "not_null": "True"
        },
        {
            "name": "product_id", 
            "data_type": "integer", 
            "foreign_key": {"table": "products", "column": "product_id"}, 
            "not_null": "True"
        },
        {
            "name": "quantity", 
            "data_type": "integer", 
            "not_null": "True", 
            "default": "1"
        }
    ]

GET http://localhost:8000/api/v1/all-elements -->> Retrieves all the elements

GET http://localhost:8000/api/v1/datasets/{dataset_id}/elements -->> Retrieves the dataset and its elements


## TESTS
## Run all tests:
pytest
## Note: Some tests may fail if run multiple times because creating the same dataset twice is not allowed.


## Docker
$sudo docker build --no-cache -t myfastapiapp .

$sudo docker run -d -p 8000:80 --name myfastapiapp_container myfastapiapp

$sudo docker ps

http://localhost:8000/docs





