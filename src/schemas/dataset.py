from pydantic import BaseModel

class Index(BaseModel):
    name: str          # The name of the index
    columns: list[str] # Singular or composite index on one or more columns (e.g., ["first_name"] for single column index or ["first_name", "last_name"] for composite index)

class Constraints(BaseModel):
    primary_key: list[str] | None = None # e.g., ["id"] or ["first_name", "last_name"] for composite primary key
    unique: list[str] | None = None      # e.g., ["email"] to enforce unique email addresses

# Main dataset models
class DatasetCreate(BaseModel):
    name: str
    description: str | None = None
    constraints: Constraints | None = None
    indexes: list[Index] | None = None

class DatasetResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    constraints: Constraints | None = None
    indexes: list[Index] | None = None

    class ConfigDict:
        from_attributes = True