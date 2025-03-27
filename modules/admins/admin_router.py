from fastapi import APIRouter
from .admin_response_models import GetAllAdminResponesModel
from .admin_request_models import AddAdminRequest, DeleteAdminRequest
from .admin_repository import *

router = APIRouter(tags=["Admin"], prefix="/admin")


# In order to get all admins
@router.get("/all", response_model=GetAllAdminResponesModel)
async def get_all_designations():
    return await get_all()


# In order to add new admin
@router.post("/add")
async def add_admin(request: AddAdminRequest):
    return await add(request=request)


# In order to delete new admin
@router.delete("/delete")
async def delete_admin(request: DeleteAdminRequest):
    return await delete(request=request)
