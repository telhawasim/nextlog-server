from pydantic import BaseModel
from typing import List
from .employee import Employee


class EmployeeModel(BaseModel):
    id: str
    name: str
    email: str
    role: str
    created_at: str


class GetAllEmployees(BaseModel):
    total_pages: int
    current_page: int
    limit: int
    total_count: int
    employees: List[EmployeeModel]
