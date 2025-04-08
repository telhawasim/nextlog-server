from datetime import datetime
from pydantic import TypeAdapter, parse_obj_as
import pydantic
from app.mongodb import db
from math import ceil
from .employee_serialization import employee_serialize
from .employee_response_models import (
    EmployeeDetail,
    EmployeeDetailResponse,
    GetAllEmployees,
)
from app.exception import CustomException
from .employee import Employee
from modules.shared.models import BaseServerModel
from bson import ObjectId
from fastapi import File, UploadFile, Form
import shutil
import os

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


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
            {
                "$lookup": {
                    "from": "departments",  # Collection name
                    "localField": "department",  # FK in employees
                    "foreignField": "_id",  # PK in designations
                    "as": "department",
                }
            },
            {"$unwind": {"path": "$department", "preserveNullAndEmptyArrays": True}},
            {
                "$lookup": {
                    "from": "profiles",
                    "localField": "profiles",
                    "foreignField": "_id",
                    "as": "profiles",
                }
            },
        ],
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


async def detail(id):
    # Extract the employee from the database
    employee = await db.employees.find_one({"_id": ObjectId(id)})
    # Throw exception if there is not employee
    if not employee:
        raise CustomException(status_code=404, message="Employee doesn't exist")
    # Aggregate the employee object
    employee_cursor = db.employees.aggregate(
        [
            {"$match": {"_id": ObjectId(id)}},
            {
                "$lookup": {
                    "from": "designations",
                    "localField": "designation",
                    "foreignField": "_id",
                    "as": "designation",
                }
            },
            {"$unwind": {"path": "$designation", "preserveNullAndEmptyArrays": True}},
            {
                "$lookup": {
                    "from": "departments",
                    "localField": "department",
                    "foreignField": "_id",
                    "as": "department",
                }
            },
            {"$unwind": {"path": "$department", "preserveNullAndEmptyArrays": True}},
            {
                "$lookup": {
                    "from": "profiles",
                    "let": {"profile_ids": "$profiles"},
                    "pipeline": [
                        {"$match": {"$expr": {"$in": ["$_id", "$$profile_ids"]}}},
                        {
                            "$sort": {"created_at": -1}
                        },  # Sort profiles by created_at (descending)
                    ],
                    "as": "profiles",
                }
            },
        ]
    )
    # Extract the Employee data after aggregation
    employee_data = await employee_cursor.to_list(length=1)
    # Throw exception if there is not data for employee
    if not employee_data:
        raise CustomException(status_code=404, message="There is no employee data")
    # Get the employee
    employee = employee_data[0]
    # Serialize the employee
    serialized_employee = employee_serialize(employee)
    # Create a TypeAdapter for EmployeeDetail
    employee_detail_adapter = TypeAdapter(EmployeeDetail)
    # Parse the data according to the model
    employee_detail = employee_detail_adapter.validate_python(serialized_employee)
    # Response
    return EmployeeDetailResponse(
        message="Success", status=200, employee=employee_detail
    )


async def add(
    name: str = Form(...),
    email: str = Form(...),
    emp_id: int = Form(...),
    phone: str = Form(...),
    designation: str = Form(...),
    department: str = Form(...),
    avatar: UploadFile = File(...),
    dob: str = Form(...),
    date_of_joining: str = Form(...),
):
    # Validate the request
    if not name:
        raise CustomException(status_code=404, message="Name is required")
    if not email:
        raise CustomException(status_code=404, message="Email is required")
    if not emp_id:
        raise CustomException(status_code=404, message="Employee ID is required")
    if not phone:
        raise CustomException(status_code=404, message="Phone is required")
    if not designation:
        raise CustomException(status_code=404, message="Designation is required")
    if not department:
        raise CustomException(status_code=404, message="Department is required")
    if not avatar:
        raise CustomException(status_code=404, message="Profile image is required")
    if not dob:
        raise CustomException(status_code=404, message="Date of birth is required")
    if not date_of_joining:
        raise CustomException(status_code=404, message="Date of joining is required")
    # Extract the employee from the database
    existing_employee = await db.employees.find_one({"email": email})
    # Throw exception if employee with this email already exists
    if existing_employee:
        raise CustomException(
            status_code=404, message="Employee with this email already exists"
        )
    # Extract the existing designation from database
    existing_designation = db.designations.find_one({"_id": ObjectId(designation)})
    # Throw exception if there is no designation with the provided ID
    if not existing_designation:
        raise CustomException("Designation ID is invalid")
    # Extract the existing department from database
    existing_department = db.departments.find_one({"_id": ObjectId(department)})
    # Throw exception if there is no department with the provided ID
    if not existing_department:
        raise CustomException(status_code=404, message="Department ID is invalid")
    image_url = None
    file_location = f"{UPLOAD_DIR}/{avatar.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(avatar.file, buffer)
    image_url = f"/{UPLOAD_DIR}/{avatar.filename}"
    # Make new object of Employee which needs to be added in database
    new_employee = Employee(
        name=name,
        email=email,
        emp_id=emp_id,
        phone=phone,
        designation=ObjectId(designation),
        department=ObjectId(department),
        avatar=f"/upload/{avatar.filename}" if avatar else None,
        dob=dob,
        date_of_joining=date_of_joining,
    )
    # Insert the employee into the database
    await db.employees.insert_one(new_employee.model_dump())
    # Response
    return BaseServerModel(status=200, message="Employee has been added successfully")


async def delete(id: str):
    # Find employee in database
    employee = await db.employees.find_one({"_id": ObjectId(id)})
    if not employee:
        raise CustomException(status_code=404, message="Employee not found")
    # Get the avatar path
    avatar_path = employee.get("avatar")
    if avatar_path:
        file_path = os.path.join(UPLOAD_DIR, os.path.basename(avatar_path))
        # Remove the file if it exists
        if os.path.exists(file_path):
            os.remove(file_path)
    # Delete the profiles associated with the employee
    await db.profiles.delete_many({"employee_id": ObjectId(id)})
    # Delete the employee from the database
    await db.employees.delete_one({"_id": ObjectId(id)})
    # Response
    return BaseServerModel(status=200, message="Employee has been deleted successfully")
