from app.mongodb import db
from math import ceil
from pymongo import DESCENDING
from .employee_serialization import employee_serialize
from .employee_response_models import GetAllEmployees
from .employee_request_models import AddEmployeeRequest
from app.exception import CustomException
from .employee import Employee
from modules.shared.models import BaseServerModel
from bson import ObjectId


async def get_all(page: int, limit: int):
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
    employees_cursor = db.employees.aggregate(
        [
            {"$sort": {"created_at": -1}},
            {"$skip": skip},
            {"$limit": limit},
            {
                "$lookup": {
                    "from": "designations",  # Collection name
                    "localField": "designation",  # FK in employees
                    "foreignField": "_id",  # PK in designations
                    "as": "designation",
                }
            },
            {"$unwind": {"path": "$designation", "preserveNullAndEmptyArrays": True}},
        ]
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


async def add(request: AddEmployeeRequest):
    # Validate the request
    request.validate_add_employee()
    # Extract the employee from the database
    existing_employee = await db.employees.find_one({"email": request.email})
    # Throw exception if employee with this email already exists
    if existing_employee:
        raise CustomException(
            status_code=404, message="Employee with this email already exists"
        )
    # Extract the existing designation from database
    existing_designation = db.designations.find_one(
        {"_id": ObjectId(request.designation)}
    )
    # Throw exception if there is no designation with the provided ID
    if not existing_designation:
        raise CustomException("Designation ID is invalid")
    # Make new object of Employee which needs to be added in database
    new_employee = Employee(
        name=request.name,
        email=request.email,
        designation=ObjectId(request.designation),
    )
    # Insert the employee into the database
    await db.employees.insert_one(new_employee.model_dump())
    # Response
    return BaseServerModel(status=200, message="Employee has been added successfully")
