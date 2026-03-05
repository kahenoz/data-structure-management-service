from sqlalchemy.exc import SQLAlchemyError
from src.models.data_elements import DataElement
from src.schemas.data_elements import DataElementCreate, DataElementResponse, DatasetElementsResponse
from sqlalchemy.orm import Session
from src.database.get_db import get_db_session
from fastapi import APIRouter, Depends

from src.utils.helper import check_dataset_exists_by_id, check_data_element_exists, return_data_element_by_id

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

    #check if dataset already exists    
    check_dataset_exists_by_id(db, dataset_id)

    for item in payload:
        #check if element already exists in the dataset
        check_data_element_exists(db, dataset_id, item.name)

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

    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise

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
    dataset = check_dataset_exists_by_id(db, dataset_id)

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
    check_dataset_exists_by_id(db, dataset_id)

    data_element = return_data_element_by_id(db, dataset_id, payload.name)

    #Overwrite the element of the dataset with the new values
    data_element.name = payload.name
    data_element.data_type = payload.data_type
    data_element.foreign_key = payload.foreign_key.model_dump() if payload.foreign_key else None
    data_element.not_null = payload.not_null
    data_element.default = payload.default
    data_element.is_pii = payload.is_pii

    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise

    db.refresh(data_element)
    return data_element


@router.get("/all-elements")
def get_all_elements(
    db: Session = Depends(get_db_session)
):
    """
    Get all data elements across all datasets.
    """
    return db.query(DataElement).all()
