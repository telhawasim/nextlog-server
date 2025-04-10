from bson import ObjectId
from fastapi import APIRouter
from app.mongodb import db
from app.exception import CustomException
from helper.convert_object_id_to_str import convert_object_id_to_str
from modules.profiles.profile import Profile
from modules.shared.models import BaseServerModel
from .profile_request_models import (
    AddBasicInformation,
    AddExperienceRequest,
    AddProfile,
    AddQualificationRequest,
)
from .profile_repository import *

router = APIRouter(tags=["Profile"], prefix="/profile")


# In order to get the details of a profile
@router.get("/detail/{id}")
async def get_profile_detail(id: str):
    return await get_detail(id=id)


# In order to add new profile against an employee
@router.post("/add")
async def add_profile(request: AddProfile):
    return await add(request=request)


# In order to delete the existing profile against an employee
@router.delete("/delete/{id}")
async def delete_profile(id):
    return await delete(id=id)


# In order to add basic information against a profile
@router.put("/{id}/basic-information")
async def add_basic_information(id: str, request: AddBasicInformation):
    return await add_information(id=id, request=request)


# In order to add experience against a profile
@router.put("/{id}/experience")
async def add_experience(id: str, request: AddExperienceRequest):
    return await add_experiences(id=id, request=request)


@router.put("/{id}/qualification")
async def add_qualification(id: str, request: AddQualificationRequest):
    return await add_qualifications(id=id, request=request)


@router.put("/{id}/skill")
async def add_skill(id: str, request: AddSkillRequest):
    return await add_skills(id=id, request=request)
