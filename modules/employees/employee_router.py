from datetime import datetime
from fastapi import APIRouter, Depends, Query, Form, File, UploadFile

from app.jwt_token import verify_token
from .employee_repository import *

router = APIRouter(tags=["Employee"], prefix="/employee")


# In order to get all the employees
@router.get(
    "/all",
    response_model=GetAllEmployees,
)
async def get_all_employees(
    page: int = Query(1, gt=0),  # Default 1, must be >= 1
    limit: int = Query(10, gt=0, le=100),
    user: dict = Depends(verify_token),  # Default 10, max 100
):
    return await get_all(page=page, limit=limit)


# In order to get the detail of the employee
@router.get("/detail/{id}", response_model=EmployeeDetailResponse)
async def get_detail(id, user: dict = Depends(verify_token)):
    return await detail(id)


# In order to add new employee
@router.post("/add")
async def add_employee(
    name: str = Form(...),
    email: str = Form(...),
    emp_id: int = Form(...),
    phone: str = Form(...),
    designation: str = Form(...),
    department: str = Form(...),
    avatar: UploadFile = File(...),
    dob: str = Form(...),
    date_of_joining: str = Form(...),
    user: dict = Depends(verify_token),
):
    return await add(
        name,
        email,
        emp_id,
        phone,
        designation,
        department,
        avatar,
        dob,
        date_of_joining,
    )


# In order to delete the employee
@router.delete("/delete/{id}")
async def delete_employee(id, user: dict = Depends(verify_token)):
    return await delete(id=id)
