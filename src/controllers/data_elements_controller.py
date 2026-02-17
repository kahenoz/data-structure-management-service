from src.models.data_elements import DataElement
from src.schemas.data_elements import DataElementCreate, DataElementResponse, DatasetElementsResponse
from src.models.dataset import Dataset
from sqlalchemy.orm import Session
from src.database.get_db import get_db_session
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()

@router.post(
    "/datasets/{dataset_id}/elements",
    response_model=list[DataElementResponse])
def create_data_elements(
    dataset_id: int,
    payload: list[DataElementCreate],
    db: Session = Depends(get_db_session)
):
    """
    Create new data elements for a dataset.
    """
    elements = []

    for item in payload:
        existing_dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
        if not existing_dataset:
            raise HTTPException(status_code=404, detail="Dataset not found")

        existing = (
            db.query(DataElement)
            .filter(
                DataElement.dataset_id == dataset_id,
                DataElement.name == item.name
            )
            .first()
        )
        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"Data element '{item.name}' already exists in dataset"
            )

        element = DataElement(
            dataset_id=dataset_id,
            name=item.name,
            data_type=item.data_type,
            foreign_key=item.foreign_key.model_dump() if item.foreign_key else None,
            not_null=item.not_null,
            default=item.default,
            is_pii=item.is_pii
        )

        db.add(element)
        elements.append(element)

    db.commit()

    for e in elements:
        db.refresh(e)

    return elements


@router.get(
    "/datasets/{dataset_id}/elements",
    response_model=DatasetElementsResponse,
    response_model_exclude_none=True
)
def list_data_elements(
    dataset_id: int,
    db: Session = Depends(get_db_session)
):
    """
    List all data elements for a dataset.
    """
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    return {
        "dataset": {
            "id": dataset.id,
            "name": dataset.name,
            "description": dataset.description,
            "constraints": dataset.constraints,
            "indexes": dataset.indexes
        },
        "data_elements": dataset.data_elements
    }

@router.put("/datasets/{dataset_id}/element", response_model=DataElementResponse)
def update_data_element(
    dataset_id: int,
    payload: DataElementCreate,
    db: Session = Depends(get_db_session)
):
    """
    Update an existing data element in a dataset.
    """
    #Check if dataset already exists
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")    

    #Overwrite the element of the dataset with the new values
    data_element = db.query(DataElement).filter(
        DataElement.dataset_id == dataset_id,
        DataElement.name == payload.name
    ).first()

    if not data_element:
        raise HTTPException(status_code=404, detail="Data element not found in dataset")

    data_element.name = payload.name
    data_element.data_type = payload.data_type
    data_element.foreign_key = payload.foreign_key
    data_element.not_null = payload.not_null
    data_element.default = payload.default

    db.commit()
    db.refresh(data_element)

    return data_element


@router.get("/all-elements")
def get_all_elements(
    db: Session = Depends(get_db_session)
):
    """
    Get all data elements across all datasets.
    """
    elements = db.query(DataElement).all()
    return elements