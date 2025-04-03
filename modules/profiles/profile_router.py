from os import name
from bson import ObjectId
from fastapi import APIRouter
from app.mongodb import db
from app.exception import CustomException
from modules.profiles.profile import Profile
from modules.shared.models import BaseServerModel
from .profile_request_models import AddProfile

router = APIRouter(tags=["Profile"], prefix="/profile")


# In order to add new profile against an employee
@router.post("/add")
async def add_profile(request: AddProfile):
    # Check whether the employee exists
    employee = await db.employees.find_one({"_id": ObjectId(request.id)})
    # Throw exception if employee doesn't exist
    if not employee:
        return CustomException(status_code=404, message="Employee not found")
    # Make a new object of Profile
    new_profile = Profile(employee_id=ObjectId(request.id), title=request.name)
    # Insert the object in the database
    profile_insert = await db.profiles.insert_one(new_profile.model_dump())
    # Update the employee model
    await db.employees.update_one(
        {"_id": ObjectId(request.id)},
        {"$push": {"profiles": profile_insert.inserted_id}},
    )
    return BaseServerModel(status=200, message="Profile has been created successfully")


# In order to delete the existing profile against an employee
@router.delete("/delete{id}")
async def delete_profile(id):
    # Extract the profile from the database
    profile = await db.profiles.find_one({"_id": ObjectId(id)})
    # Throw exception if there is no ID in the database
    if not profile:
        raise CustomException(status_code=404, message="Profile doesn't exist")
    # Update the database for the employee
    result = await db.employees.update_one(
        {"profiles": ObjectId(id)}, {"$pull": {"profiles": ObjectId(id)}}
    )
    # If there are no modification throw exception
    if result.modified_count == 0:
        raise CustomException(
            status_code=404, message="Profile was not linked to any employee"
        )
    # Delete the profile object from the database
    await db.profiles.delete_one({"_id": ObjectId(id)})
    # Response
    return BaseServerModel(
        status=200,
        message="Profile deleted successfully",
    )
