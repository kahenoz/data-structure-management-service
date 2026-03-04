from sqlalchemy.exc import IntegrityError
from src.models.dataset import Dataset
from src.schemas.dataset import DatasetCreate, DatasetResponse
from sqlalchemy.orm import Session
from src.database.get_db import get_db_session
from fastapi import APIRouter, Depends, HTTPException
from src.utils.helper import check_dataset_exists_by_id, check_dataset_exists_by_name

router = APIRouter()

@router.post("/datasets", response_model=DatasetResponse)
def create_dataset(
    payload: DatasetCreate,
    db: Session = Depends(get_db_session)
):
    """
    Create a new dataset.
    """
    # Check if dataset already exists
    check_dataset_exists_by_name(db, payload.name)

    dataset = Dataset(
        name=payload.name,
        description=payload.description,
        constraints=payload.constraints.model_dump() if payload.constraints else None,
        indexes=[idx.model_dump() for idx in payload.indexes] if payload.indexes else None
    )

    db.add(dataset)
    
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Dataset with this name already exists"
        )

    db.refresh(dataset)
    return dataset

@router.get("/datasets", response_model=list[DatasetResponse],
             response_model_exclude_none=True)
def list_datasets(db: Session = Depends(get_db_session)):
    """
    List all datasets.
    """
    return db.query(Dataset).all()

@router.get("/datasets/{dataset_id}", response_model=DatasetResponse,
            response_model_exclude_none=True)
def get_dataset(dataset_id: int, db: Session = Depends(get_db_session)):
    """
    Retrieve a dataset by its ID.
    """
    return check_dataset_exists_by_id(db, dataset_id)
