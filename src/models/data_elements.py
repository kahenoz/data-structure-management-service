from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, UniqueConstraint, JSON
from sqlalchemy.orm import relationship
from src.database.get_db import Base

class DataElement(Base):
    __tablename__ = "data_elements"
    __table_args__ = (
        UniqueConstraint("dataset_id", "name", name="uq_dataset_element_name"),
    )
    # Composite primary key consisting of dataset_id and name
    # One to many relationship with Dataset (one dataset can have many data elements)
    # One element with the same name cannot exist within the same dataset, but can exist across different datasets

    dataset_id = Column(
        Integer,
        ForeignKey("datasets.id", ondelete="CASCADE"),
        primary_key=True
    )
    name = Column(String, primary_key=True)
    data_type = Column(String, nullable=False)
    foreign_key = Column(JSON, nullable=True)  # Stores the foreign key as a JSON object
    not_null = Column(Boolean, default=None)
    default = Column(String, nullable=True)
    is_pii = Column(Boolean, default=None)

    dataset = relationship(
        "Dataset",
        back_populates="data_elements"
    )