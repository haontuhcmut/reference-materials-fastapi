from pydantic import BaseModel 
from fastapi import UploadFile, File
from typing import Annotated

class UploadSDSModel(BaseModel):
    file: Annotated[UploadFile, File(..., description= "Safety Data Sheet.pdf")]

