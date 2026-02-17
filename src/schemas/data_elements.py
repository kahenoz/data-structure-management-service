from pydantic import BaseModel
from src.schemas.dataset import DatasetResponse

class ForeignKey(BaseModel):
    table: str # The name of the table this foreign key references
    column: str # The name of the column this foreign key references

class DataElementCreate(BaseModel):
    name: str # The name of the data element
    data_type: str # The data type of the data element (e.g., "string", "integer", "boolean", etc.)
    foreign_key: ForeignKey | None = None # Optional foreign key reference to another table
    not_null: bool | None = None # Optional flag indicating whether the data element cannot be null
    default: str | None = None # Optional default value for the data element (e.g., "N/A", "0", etc.)
    is_pii: bool | None = None # Optional flag indicating whether the data element contains personally identifiable information

class DataElementResponse(BaseModel):
    name: str
    data_type: str
    foreign_key: ForeignKey | None = None
    not_null: bool | None = None
    default: str | None = None
    is_pii: bool | None = None

    class ConfigDict:
        from_attributes = True

class DatasetElementsResponse(BaseModel):
    dataset: DatasetResponse
    data_elements: list[DataElementResponse]

    class ConfigDict:
        from_attributes = True