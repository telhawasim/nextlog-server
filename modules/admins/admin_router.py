from fastapi import APIRouter
from app.mongodb import db
from bson import ObjectId
from .admin_serialization import admin_serialize
from .admin_response_models import GetAdminResponseModel, GetAllAdminResponesModel
from .admin_request_models import AddAdminRequest
from .admin import Admin
from modules.shared.models import BaseServerModel
from app.exception import CustomException

router = APIRouter(tags=["Admin"], prefix="/admin")


# In order to get all admins
@router.get("/all", response_model=GetAllAdminResponesModel)
async def get_all_designations():
    # Extract all the admins
    admins_cursor = db.admins.find()
    # Make them as a list
    admins = await admins_cursor.to_list(length=None)
    # Serialize the response according to requirement
    serialzied_admins = [admin_serialize(admin) for admin in admins]
    # Response
    return GetAllAdminResponesModel(admins=serialzied_admins)


@router.post("/add")
async def add_admin(request: AddAdminRequest):
    # Request validation
    request.add_admin_validation()
    # Extract the existing admin with same email
    existing_admin = await db.admins.find_one({"email": request.email})
    # Throw exception in case admin already exists
    if existing_admin:
        raise CustomException(status_code=400, message="Admin already exists")
    # Hash the password
    request.hash_password()

    new_admin = Admin(email=request.email, password=request.password)
    await db.admins.insert_one(new_admin.model_dump())

    return BaseServerModel(status=200, message="Admin has been added")
