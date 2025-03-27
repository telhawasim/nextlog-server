from fastapi import APIRouter, Query
from math import ceil
from pymongo import DESCENDING
from app.mongodb import db
from app.exception import CustomException
from .employee import Employee
from .employee_request_models import AddEmployeeRequest
from .employee_response_models import GetAllEmployees
from modules.shared.models import BaseServerModel
from .employee_serialization import employee_serialize

router = APIRouter(tags=["Employee"], prefix="/employee")


# In order to get all the employees
@router.get("/all")
async def get_all_employees(
    page: int = Query(1, gt=0),  # Default 1, must be >= 1
    limit: int = Query(10, gt=0, le=100),  # Default 10, max 100
):
    # Get total number of employees in database
    total_count = await db.employees.count_documents({})
    # Calculate the total pages
    total_pages = ceil(total_count / limit)
    # Ensure page is not out of range
    if page > total_pages and total_pages > 0:
        page = total_pages
    # Calculate the number of documents to skip
    skip = (page - 1) * limit
    # Extract the employees from the database
    employees_cursor = (
        db.employees.find().sort("created_at", DESCENDING).skip(skip).limit(limit)
    )
    # Convert the employees into list
    employees = await employees_cursor.to_list(length=limit)
    # Serialize the list according to requirement
    serialized_employees = [employee_serialize(employee) for employee in employees]
    # Response
    return GetAllEmployees(
        total_count=total_count,
        total_pages=total_pages,
        current_page=page,
        limit=limit,
        employees=serialized_employees,
    )


@router.post("/add")
async def add_employee(request: AddEmployeeRequest):
    # Validate the request
    request.validate_add_employee()
    # Extract the employee from the database
    existing_employee = await db.employees.find_one({"email": request.email})
    # Throw exception if employee with this email already exists
    if existing_employee:
        raise CustomException(
            status_code=404, message="Employee with this email already exists"
        )
    # Make new object of Employee which needs to be added in database
    new_employee = Employee(name=request.name, email=request.email)
    # Insert the employee into the database
    await db.employees.insert_one(new_employee.model_dump())
    # Response
    return BaseServerModel(status=200, message="Employee has been added successfully")
