from fastapi import APIRouter
from modules.designatons.designation_request_models import AddDesignationModel
from modules.designatons.designation_response_models import (
    GetDesignationModel,
    GetAllDesignationsModel,
)
from modules.shared.models import BaseServerModel
from .designation_repository import *

router = APIRouter(tags=["Designation"], prefix="/designation")


# In order to get all designations
@router.get("/all", response_model=GetAllDesignationsModel)
async def get_all_designations():
    return await get_all()


# In order to get the existing designation
@router.get("/{id}", response_model=GetDesignationModel)
async def get_designation(id: str):
    return await get(id)


# In order to add new designation
@router.post("/", response_model=BaseServerModel)
async def add_designation(request: AddDesignationModel):
    return await add(request=request)


# In order to delete existing designation
@router.delete("/{id}", response_model=BaseServerModel)
async def delete_desigation(id: str):
    return await delete(id)
