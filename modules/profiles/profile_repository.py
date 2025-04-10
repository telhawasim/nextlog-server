from json import tool
from profile import Profile
from bson import ObjectId
from app.exception import CustomException
from helper.convert_object_id_to_str import convert_object_id_to_str
from app.mongodb import db
from modules.profiles.profile_response_models import (
    ProfileDetailEmployeeModel,
    ProfileDetailResponseModel,
)
from .profile import Profile
from modules.profiles.profile_request_models import (
    AddBasicInformation,
    AddExperienceRequest,
    AddProfile,
    AddQualificationRequest,
    AddSkillRequest,
)
from modules.shared.models import BaseServerModel


async def get_detail(id: str):
    profile_cursor = db.profiles.aggregate(
        [
            {"$match": {"_id": ObjectId(id)}},
            {
                "$lookup": {
                    "from": "employees",
                    "localField": "employee_id",
                    "foreignField": "_id",
                    "as": "employee_data",
                }
            },
            {
                "$unwind": {
                    "path": "$employee_data",
                    "preserveNullAndEmptyArrays": True,
                }
            },
            {
                "$addFields": {
                    "employee": {
                        "id": "$employee_data._id",
                        "name": "$employee_data.name",
                        "avatar": "$employee_data.avatar",
                    }
                }
            },
            # Lookup for basic_information.designation
            {
                "$lookup": {
                    "from": "designations",
                    "localField": "basic_information.designation",
                    "foreignField": "_id",
                    "as": "basic_info_designation",
                }
            },
            {
                "$unwind": {
                    "path": "$basic_info_designation",
                    "preserveNullAndEmptyArrays": True,
                }
            },
            {
                "$addFields": {
                    "basic_information.designation": "$basic_info_designation"
                }
            },
            # Lookup for current_experience.designation
            {
                "$lookup": {
                    "from": "designations",
                    "localField": "experience.current_experience.designation",
                    "foreignField": "_id",
                    "as": "current_experience_designation",
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
            # Ensure previous_experience exists and is an array or null
            {
                "$addFields": {
                    "experience.previous_experience": {
                        "$cond": {
                            "if": {
                                "$gt": [
                                    {
                                        "$size": {
                                            "$ifNull": [
                                                "$experience.previous_experience",
                                                [],
                                            ]
                                        }
                                    },
                                    0,
                                ]
                            },
                            "then": "$experience.previous_experience",
                            "else": None,
                        }
                    }
                }
            },
            # Unwind previous_experience (if not None) to allow lookup
            {
                "$unwind": {
                    "path": "$experience.previous_experience",
                    "preserveNullAndEmptyArrays": True,
                }
            },
            {
                "$addFields": {
                    "qualification": {
                        "$cond": {
                            "if": {
                                "$gt": [
                                    {"$size": {"$ifNull": ["$qualification", []]}},
                                    0,
                                ]
                            },
                            "then": "$qualification",
                            "else": None,
                        }
                    }
                }
            },
            {
                "$addFields": {
                    "certification": {
                        "$cond": {
                            "if": {
                                "$gt": [
                                    {"$size": {"$ifNull": ["$certification", []]}},
                                    0,
                                ]
                            },
                            "then": "$certification",
                            "else": None,
                        }
                    }
                }
            },
            {
                "$addFields": {
                    "skill.technical_skills": {
                        "$cond": {
                            "if": {
                                "$gt": [
                                    {
                                        "$size": {
                                            "$ifNull": [
                                                "$skill.technical_skills",
                                                [],
                                            ]
                                        }
                                    },
                                    0,
                                ]
                            },
                            "then": "$skill.technical_skills",
                            "else": None,
                        }
                    }
                }
            },
            {
                "$addFields": {
                    "skill.non_technical_skills": {
                        "$cond": {
                            "if": {
                                "$gt": [
                                    {
                                        "$size": {
                                            "$ifNull": [
                                                "$skill.non_technical_skills",
                                                [],
                                            ]
                                        }
                                    },
                                    0,
                                ]
                            },
                            "then": "$skill.non_technical_skills",
                            "else": None,
                        }
                    }
                }
            },
            {
                "$addFields": {
                    "tool": {
                        "$cond": {
                            "if": {
                                "$gt": [
                                    {"$size": {"$ifNull": ["$tool", []]}},
                                    0,
                                ]
                            },
                            "then": "$tool",
                            "else": None,
                        }
                    }
                }
            },
            # Lookup for previous_experience.designation
            {
                "$lookup": {
                    "from": "designations",
                    "localField": "experience.previous_experience.designation",
                    "foreignField": "_id",
                    "as": "previous_experience_designation",
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
            # Regroup previous_experience into an array (or None)
            {
                "$group": {
                    "_id": "$_id",
                    "doc": {"$first": "$$ROOT"},
                    "previous_experience": {"$push": "$experience.previous_experience"},
                }
            },
            {
                "$addFields": {
                    "doc.experience.previous_experience": {
                        "$cond": {
                            "if": {
                                "$eq": [
                                    {
                                        "$filter": {
                                            "input": "$previous_experience",
                                            "as": "exp",
                                            "cond": {"$ne": ["$$exp", {}]},
                                        }
                                    },
                                    [],
                                ]
                            },
                            "then": None,
                            "else": {
                                "$filter": {
                                    "input": "$previous_experience",
                                    "as": "exp",
                                    "cond": {"$ne": ["$$exp", {}]},
                                }
                            },
                        }
                    }
                }
            },
            {"$replaceRoot": {"newRoot": "$doc"}},
            {
                "$project": {
                    "employee_data": 0,
                    "basic_info_designation": 0,
                    "current_experience_designation": 0,
                    "previous_experience_designation": 0,
                }
            },
        ]
    )

    result = await profile_cursor.to_list(length=1)

    if not result:
        raise CustomException(status_code=404, message="Profile not found")

    profile = result[0]

    if not profile.get("basic_information"):
        profile["basic_information"] = None
    if not profile.get("experience", {}).get("current_experience"):
        profile["experience"]["current_experience"] = None
    if "experience" in profile and "previous_experience" not in profile["experience"]:
        profile["experience"]["previous_experience"] = None
    # Converting '_id' to 'id'
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


async def add_qualifications(id: str, request: AddQualificationRequest):
    # Check if the profile exists
    profile = await db.profiles.find_one({"_id": ObjectId(id)})
    # Throw exception if profile doesn't exist
    if not profile:
        raise CustomException(status_code=404, message="Profile not found")
    # Handle the qualification data according to the database
    qualification_data = [
        {
            "degree": qualification.degree,
            "institution": qualification.institution,
            "start_date": qualification.start_date,
            "end_date": qualification.end_date,
        }
        for qualification in request.qualification
    ]
    # Check if the certificate exists in the request
    certifications = request.certification or []
    # Handle the certification data according to the database
    certification_data = [
        {
            "course_name": certification.course_name,
            "institution": certification.institution,
            "start_date": certification.start_date,
            "end_date": certification.end_date,
        }
        for certification in certifications
    ]
    # Add the qualification data to the profile
    await db.profiles.update_one(
        {"_id": ObjectId(id)},
        {
            "$set": {
                "qualification": qualification_data,
                "certification": certification_data,
            }
        },
    )
    # Response
    return BaseServerModel(status=200, message="Experience added successfully")


async def add_skills(id: str, request: AddSkillRequest):
    # Check if the profile exists
    profile = await db.profiles.find_one({"_id": ObjectId(id)})
    # Throw exception if profile doesn't exist
    if not profile:
        raise CustomException(status_code=404, message="Profile not found")
    # Handle the technical skills according to the request
    technical_skills = request.technical_skills or []
    # Handle the non technical skills according to the request
    non_technical_skills = request.non_technical_skills or []
    # Handle the tootsl according to the request
    tools = request.tools or []
    # Handle the skills data according to the database
    skills_data = {
        "technical_skills": [
            {"name": technical_skill.name} for technical_skill in technical_skills
        ],
        "non_technical_skills": [
            {"name": non_technical_skill.name}
            for non_technical_skill in non_technical_skills
        ],
    }
    # Handle the tools data according to the database
    tools_data = [{"name": tool.name} for tool in tools]
    # Add the skills data to the profile
    await db.profiles.update_one(
        {"_id": ObjectId(id)},
        {
            "$set": {
                "skill": skills_data,
                "tool": tools_data,
            }
        },
    )
    # Response
    return BaseServerModel(status=200, message="Experience added successfully")
