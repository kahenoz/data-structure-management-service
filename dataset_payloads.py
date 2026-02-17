datasets_payload = [
    {
        "name": "customers",
        "description": "Customer data",
        "constraints": {"primary_key": ["id"], "unique": ["email"]},
        "indexes": []
    },
    {
        "name": "orders",
        "description": "Orders data",
        "constraints": {"primary_key": ["order_id"], "unique": []},
        "indexes": []
    },
    {
        "name": "products",
        "description": "Products data",
        "constraints": {"primary_key": ["product_id"], "unique": []},
        "indexes": []
    },
    {
        "name": "ordersXproducts",
        "description": "Order items linking orders and products",
        "constraints": {"primary_key": ["order_id", "product_id"], "unique": []},
        "indexes": []
    }
]

elements_payload = {
    "customers": [
        {"name": "id",    "data_type": "integer", "not_null": "True"},
        {"name": "name",  "data_type": "string",  "not_null": "True"},
        {"name": "email", "data_type": "string",  "not_null": "True",  "is_pii": "True"}
    ],
    "orders": [
        {"name": "order_id",    "data_type": "integer",  "not_null": "True"},
        {"name": "customer_id", "data_type": "integer",  "foreign_key": {"table": "customers", "column": "id"}, "not_null": "True"},
        {"name": "order_date",  "data_type": "timestamp", "not_null": "True"}
    ],
    "products": [
        {"name": "product_id", "data_type": "integer","not_null": "True"},
        {"name": "product_name", "data_type": "string", "not_null": "True"},
        {"name": "price", "data_type": "decimal", "not_null": "True"}
    ],
    "ordersXproducts": [
        {"name": "order_id", "data_type": "integer", "foreign_key": {"table": "orders", "column": "order_id"}, "not_null": "True"},
        {"name": "product_id", "data_type": "integer", "foreign_key": {"table": "products", "column": "product_id"}, "not_null": "True"},
        {"name": "quantity", "data_type": "integer", "not_null": "True", "default": "1"}
    ]
}
