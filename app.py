from fastapi import FastAPI
from src.database.get_db import Base, engine

# IMPORT MODELS BEFORE create_all()
from src.models.dataset import Dataset
from src.models.data_elements import DataElement

Base.metadata.create_all(bind=engine)

from src.controllers.datasets_controller import router as dataset 
from src.controllers.data_elements_controller import router as data_elements
from src.controllers.delete_dataset_controller import router as delete_dataset

app = FastAPI()

app.include_router(dataset, prefix="/api/v1")
app.include_router(data_elements, prefix="/api/v1")
app.include_router(delete_dataset, prefix="/api/v1")


@app.get("/", include_in_schema=False)
def root():
    return {"running": True}
