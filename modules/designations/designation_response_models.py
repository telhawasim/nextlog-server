from pydantic import BaseModel
from typing import List


class GetDesignationModel(BaseModel):
    id: str
    name: str


class GetAllDesignationsModel(BaseModel):
    designations: List[GetDesignationModel]
