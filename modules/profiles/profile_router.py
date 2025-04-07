from os import name
from bson import ObjectId
from fastapi import APIRouter
from app.mongodb import db
from app.exception import CustomException
from helper.convert_object_id_to_str import convert_object_id_to_str
from modules.profiles.profile import Profile
from modules.shared.models import BaseServerModel
from .profile_request_models import AddBasicInformation, AddProfile

router = APIRouter(tags=["Profile"], prefix="/profile")


# In order to get the details of a profile
@router.get("/detail/{id}")
async def get_profile_detail(id: str):
    profile_cursor = db.profiles.aggregate(
        [
            {"$match": {"_id": ObjectId(id)}},
            {
                "$lookup": {
                    "from": "designations",
                    "localField": "basic_information.designation",
                    "foreignField": "_id",
                    "as": "designation_detail",
                }
            },
            {
                "$unwind": {
                    "path": "$designation_detail",
                    "preserveNullAndEmptyArrays": True,
                }
            },
            {"$addFields": {"basic_information.designation": "$designation_detail"}},
            {"$project": {"designation_detail": 0}},
        ]
    )

    result = await profile_cursor.to_list(length=1)
    if not result:
        raise CustomException(status_code=404, message="Profile not found")
    cleaned_result = convert_object_id_to_str(result[0])
    return cleaned_result


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


# In order to add basic information against a profile
@router.put("/{id}/basic-information")
async def add_basic_information(id: str, request: AddBasicInformation):
    # Check if the profile exists
    profile = await db.profiles.find_one({"_id": ObjectId(id)})
    # Throw exception if profiles doesn't exists
    if not profile:
        raise CustomException(status_code=404, message="Profile not found")
    # Check if the designation exists
    designation_id = await db.designations.find_one(
        {"_id": ObjectId(request.designation)}
    )
    # Throw exception if designation doesn't exists
    if not designation_id:
        raise CustomException(status_code=400, message="Invalid designation ID")
    # Convert the designation ID to ObjectID
    designation_id_in_objectID = ObjectId(request.designation)
    # Convert the request model to a dictionary
    basic_info_dict = request.model_dump()
    # Set the designation ID in the dictionary
    basic_info_dict["designation"] = designation_id_in_objectID
    # Update the basic information for the profile
    await db.profiles.update_one(
        {"_id": ObjectId(id)}, {"$set": {"basic_information": basic_info_dict}}
    )
    return BaseServerModel(status=200, message="Basic information updated successfully")
