from fastapi import APIRouter, Query
from .employee_request_models import AddEmployeeRequest
from .employee_repository import *

router = APIRouter(tags=["Employee"], prefix="/employee")


# In order to get all the employees
@router.get("/all")
async def get_all_employees(
    page: int = Query(1, gt=0),  # Default 1, must be >= 1
    limit: int = Query(10, gt=0, le=100),  # Default 10, max 100
):
    return await get_all(page=page, limit=limit)


@router.post("/add")
async def add_employee(request: AddEmployeeRequest):
    return await add(request=request)
