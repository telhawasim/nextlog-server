from bson import ObjectId
from app.exception import CustomException
from app.mongodb import db
from .department_serialization import department_serialize
from .department_response_models import GetAllDepartmentsModel, GetDepartmentModel
from .department_request_models import AddDepartmentModel
from .department import Department
from modules.shared.models import BaseServerModel


async def get_all():
    # Extract all the departments
    departments_cursor = db.departments.find()
    # Make them as a list
    departments = await departments_cursor.to_list(length=None)
    # Seralize the response according to requirement
    serialzied_departments = [
        department_serialize(department) for department in departments
    ]
    # Response
    return GetAllDepartmentsModel(departments=serialzied_departments)


async def get(id):
    # Validate the ID
    if not ObjectId.is_valid(id):
        raise CustomException(status_code=400, message="Invalid ID")
    # Extract department if it already exists in database
    department = await db.departments.find_one({"_id": ObjectId(id)})
    # Throw exception if there is no department with respect to ID
    if not department:
        raise CustomException(status_code=404, message="Department doesn't exist")
    return GetDepartmentModel(id=str(department["_id"]), name=department["name"])


async def add(request: AddDepartmentModel):
    # Validate the request
    request.add_department_validation()
    # Extract department if it is already available in database
    department = await db.departments.find_one({"name": request.name})
    # Throw exception if department with same name already exists
    if department:
        raise CustomException(status_code=404, message="Department already exists")
    # Add new object for the department
    new_department = Department(name=request.name)
    # Insert the object in the database
    await db.departments.insert_one(new_department.model_dump())
    # Response
    return BaseServerModel(status=200, message="Department has been added successfully")


async def delete(id):
    # Validate the ID
    if not ObjectId.is_valid(id):
        raise CustomException(status_code=400, message="Invalid ID")
    # Extract department if it already available in database
    department = await db.departments.find_one_and_delete({"_id": ObjectId(id)})
    # Throw exception if there is no department with respect to ID
    if not department:
        raise CustomException(status_code=404, message="Department doesn't exist")
    # Response
    return BaseServerModel(
        status=200, message="Department has been deleted successfully"
    )
