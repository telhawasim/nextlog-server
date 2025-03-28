from pydantic import BaseModel
from typing import List, Optional

from modules.departments.department_response_models import GetDepartmentModel
from modules.designations.designation_response_models import GetDesignationModel


class EmployeeModel(BaseModel):
    id: str
    name: str
    email: str
    role: str
    created_at: str
    designation: Optional[GetDesignationModel]
    department: Optional[GetDepartmentModel]


class EmployeeRowModel(BaseModel):
    id: str
    name: str
    email: str
    designation: Optional[GetDesignationModel]
    avatar: str
    created_at: str


class GetAllEmployees(BaseModel):
    total_pages: int
    current_page: int
    limit: int
    total_count: int
    employees: List[EmployeeRowModel]
