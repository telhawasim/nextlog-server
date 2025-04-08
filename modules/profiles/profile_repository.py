from profile import Profile
from bson import ObjectId
from app.exception import CustomException
from helper.convert_object_id_to_str import convert_object_id_to_str
from app.mongodb import db
from .profile import Profile
from modules.profiles.profile_request_models import (
    AddBasicInformation,
    AddExperienceRequest,
    AddProfile,
)
from modules.shared.models import BaseServerModel


async def get_detail(id: str):
    # Extract the profile from the database
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
            {
                "$lookup": {
                    "from": "designations",
                    "localField": "experience.current_experience.designation",  # Path to current_experience.designation
                    "foreignField": "_id",
                    "as": "current_experience_designation",  # Alias for the result
                }
            },
            {
                "$unwind": {
                    "path": "$current_experience_designation",
                    "preserveNullAndEmptyArrays": True,
                }
            },
            {
                "$addFields": {
                    "experience.current_experience.designation": "$current_experience_designation"
                }
            },
            # Lookup to get designation for previous_experience (if any)
            {
                "$unwind": {
                    "path": "$experience.previous_experience",
                    "preserveNullAndEmptyArrays": True,
                }
            },
            {
                "$lookup": {
                    "from": "designations",
                    "localField": "experience.previous_experience.designation",  # Path to previous_experience.designation
                    "foreignField": "_id",
                    "as": "previous_experience_designation",  # Alias for the result
                }
            },
            {
                "$unwind": {
                    "path": "$previous_experience_designation",
                    "preserveNullAndEmptyArrays": True,
                }
            },
            {
                "$addFields": {
                    "experience.previous_experience.designation": "$previous_experience_designation"
                }
            },
            {
                "$project": {
                    "basic_information": 1,
                    "experience": 1,
                    "_id": 1,
                    "employee_id": 1,
                    "title": 1,
                    "created_at": 1,
                }
            },
        ]
    )
    # Extract the results from the cursor
    result = await profile_cursor.to_list(length=1)
    # Throw exception if result doesn't exist
    if not result:
        raise CustomException(status_code=404, message="Profile not found")
    # Convert the received result into a profile object
    profile = result[0]
    # Check if the profile has basic information
    if not profile.get("basic_information"):
        profile["basic_information"] = None
    # Convert the ObjectId to string
    cleaned_result = convert_object_id_to_str(profile)
    # Response
    return cleaned_result


async def add(request: AddProfile):
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


async def delete(id: str):
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


async def add_information(id: str, request: AddBasicInformation):
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


async def add_experiences(id: str, request: AddExperienceRequest):
    # Check if the profile exists
    profile = await db.profiles.find_one({"_id": ObjectId(id)})
    # Throw exception if profile doesn't exist
    if not profile:
        raise CustomException(status_code=404, message="Profile not found")
    # Check if the previous experience exists in the request
    previous_experience = request.previous_experience or []
    # Handle the request data according to the database
    experience_data = {
        "current_experience": {
            "company": request.current_experience.company_name,
            "designation": ObjectId(request.current_experience.designation),
            "start_date": request.current_experience.start_date,
            "end_date": request.current_experience.end_date,
            "description": request.current_experience.description,
        },
        "previous_experience": [
            {
                "company": exp.company_name,
                "designation": ObjectId(exp.designation),
                "start_date": exp.start_date,
                "end_date": exp.end_date,
                "description": exp.description,
            }
            for exp in previous_experience
        ],
    }
    # Add the experience data to the profile
    await db.profiles.update_one(
        {"_id": ObjectId(id)}, {"$set": {"experience": experience_data}}
    )
    # Response
    return BaseServerModel(status=200, message="Experience added successfully")
