from pydantic import BaseModel
from typing import List, Optional

class Index(BaseModel):
    name: str # The name of the index
    columns: List[str] # Singular or composite index on one or more columns (e.g., ["first_name"] for single column index or ["first_name", "last_name"] for composite index)

class Constraints(BaseModel):
    primary_key: Optional[List[str]] = None # e.g., ["id"] or ["first_name", "last_name"] for composite primary key
    unique: Optional[List[str]] = None # e.g., ["email"] to enforce unique email addresses

# Main dataset models
class DatasetCreate(BaseModel):
    name: str
    description: Optional[str] = None
    constraints: Optional[Constraints] = None
    indexes: Optional[List[Index]] = None

class DatasetResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    constraints: Optional[Constraints] = None
    indexes: Optional[List[Index]] = None

    class ConfigDict:
        from_attributes = True