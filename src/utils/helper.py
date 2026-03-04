from src.models.data_elements import DataElement
from src.models.dataset import Dataset
from sqlalchemy.orm import Session
from fastapi import HTTPException


def check_dataset_exists_by_name(db: Session, dataset_name: str) -> bool:
    """
    Check if dataset exists by name, if it does, raise an HTTPException
    """
    existing_dataset = db.query(Dataset).filter(Dataset.name == dataset_name).first()
    if existing_dataset:
        raise HTTPException(
            status_code=400,
            detail="Dataset with this name already exists"
        )


def check_dataset_exists_by_id(db: Session, dataset_id: int) -> bool:
    """
    Check if dataset exists by ID, if it does, return the dataset, otherwise raise an HTTPException
    """
    existing_dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not existing_dataset:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found"
        )
    return existing_dataset


def check_data_element_exists(db: Session, dataset_id: int, element_name: str) -> bool:
    """
    Check if data element exists by ID
    """
    existing_element = (
        db.query(DataElement).filter(DataElement.dataset_id == dataset_id,
                                    DataElement.name == element_name).first())
    if existing_element:
        raise HTTPException(
            status_code=400,
            detail=f"Data element '{element_name}' already exists in dataset"
        )
    
def return_data_element_by_id(db: Session, dataset_id: int, element_name: int) -> DataElement:
    """
    Return data element by ID
    """
    existing_element = (
        db.query(DataElement).filter(DataElement.dataset_id == dataset_id,
                                    DataElement.name == element_name).first())
    if not existing_element:
        raise HTTPException(
            status_code=404,
            detail="Data element not found"
        )
    return existing_element
