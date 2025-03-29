from app.mongodb import db
from math import ceil
from pymongo import DESCENDING
from .employee_serialization import employee_serialize
from .employee_response_models import GetAllEmployees
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


async def add(
    name: str = Form(...),
    email: str = Form(...),
    emp_id: int = Form(...),
    designation: str = Form(...),
    department: str = Form(...),
    avatar: UploadFile = File(...),
):
    # Validate the request
    if not name:
        raise CustomException(status_code=404, message="Name is required")
    if not email:
        raise CustomException(status_code=404, message="Email is required")
    if not emp_id:
        raise CustomException(status_code=404, message="Employee ID is required")
    if not designation:
        raise CustomException(status_code=404, message="Designation is required")
    if not department:
        raise CustomException(status_code=404, message="Department is required")
    if not avatar:
        raise CustomException(status_code=404, message="Profile image is required")
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
        designation=ObjectId(designation),
        department=ObjectId(department),
        avatar=f"/upload/{avatar.filename}" if avatar else None,
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
    # Delete the employee from the database
    await db.employees.delete_one({"_id": ObjectId(id)})
    # Response
    return BaseServerModel(status=200, message="Employee has been deleted successfully")
