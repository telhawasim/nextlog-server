from pydantic import BaseModel
from typing import List


class GetDepartmentModel(BaseModel):
    id: str
    name: str


class GetAllDepartmentsModel(BaseModel):
    departments: List[GetDepartmentModel]
