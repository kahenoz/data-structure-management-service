from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from src.database.get_db import get_db_session
from fastapi import APIRouter, Depends
from src.utils.helper import check_dataset_exists_by_id

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
    existing_dataset = check_dataset_exists_by_id(db, dataset_id)    
    db.delete(existing_dataset)

    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise

    return {"detail": f"Dataset {existing_dataset.name} and associated data elements deleted successfully"}