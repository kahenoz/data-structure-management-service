from src.models.dataset import Dataset
from sqlalchemy.orm import Session
from src.database.get_db import get_db_session
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()

@router.delete(
    "/datasets/{dataset_id}")
def delete_dataset(
    dataset_id: int,
    db: Session = Depends(get_db_session)
):
    """
    Delete a dataset and all its associated data elements.
    """
    existing_dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not existing_dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    db.delete(existing_dataset)
    db.commit()

    return {"detail": f"Dataset {existing_dataset.name} and associated data elements deleted successfully"}