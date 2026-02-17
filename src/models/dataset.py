from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.database.get_db import Base
class Dataset(Base):
    __tablename__ = "datasets"
    # Singular primary key (id) for the dataset
    # One to many relationship with DataElement (one dataset can have many data elements)
    # The name of the dataset must be unique and not null across all datasets
    # If a dataset is deleted, all associated data elements should also be deleted (cascade delete)

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    
    constraints = Column(JSON, nullable=True)  # Stores the entire constraints object
    indexes = Column(JSON, nullable=True)       # Stores the indexes array
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    data_elements = relationship(
        "DataElement",
        back_populates="dataset",
        cascade="all, delete-orphan"
    )