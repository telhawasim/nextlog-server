from fastapi import APIRouter
from modules.departments.department_request_models import AddDepartmentModel
from modules.departments.department_response_models import (
    GetDepartmentModel,
    GetAllDepartmentsModel,
)
from modules.shared.models import BaseServerModel
from .department_repository import *

router = APIRouter(tags=["Department"], prefix="/department")


# In order to get all departments
@router.get("/all", response_model=GetAllDepartmentsModel)
async def get_all_departments():
    return await get_all()


# In order to get the existing department
@router.get("/{id}", response_model=GetDepartmentModel)
async def get_department(id: str):
    return await get(id)


# In order to add new department
@router.post("/", response_model=BaseServerModel)
async def add_department(request: AddDepartmentModel):
    return await add(request=request)


# In order to delete existing department
@router.delete("/{id}", response_model=BaseServerModel)
async def delete_department(id: str):
    return await delete(id)
