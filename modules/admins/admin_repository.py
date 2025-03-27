from app.exception import CustomException
from app.mongodb import db
from .admin_serialization import admin_serialize
from .admin_response_models import GetAllAdminResponesModel
from modules.shared.models import BaseServerModel
from .admin_request_models import AddAdminRequest, DeleteAdminRequest
from app.hash_password import hash_password
from .admin import Admin


async def get_all():
    # Extract all the admins
    admins_cursor = db.admins.find()
    # Make them as a list
    admins = await admins_cursor.to_list(length=None)
    # Serialize the response according to requirement
    serialzied_admins = [admin_serialize(admin) for admin in admins]
    # Response
    return GetAllAdminResponesModel(admins=serialzied_admins)


async def add(request: AddAdminRequest):
    # Request validation
    request.add_admin_validation()
    # Extract the existing admin with same email
    existing_admin = await db.admins.find_one({"email": request.email})
    # Throw exception in case admin already exists
    if existing_admin:
        raise CustomException(status_code=400, message="Admin already exists")
    # Hash the password
    hashed_password = hash_password(request.password)
    # Make new admin object
    new_admin = Admin(email=request.email, password=hashed_password)
    # Add in the database
    await db.admins.insert_one(new_admin.model_dump())
    # Response
    return BaseServerModel(status=200, message="Admin has been added")


async def delete(request: DeleteAdminRequest):
    # Validate the request
    request.delete_admin_validation()
    # Extract the existing admin according to the email
    existing_admin = await db.admins.find_one_and_delete({"email": request.email})
    # In case there is no admin through exception
    if not existing_admin:
        raise CustomException(status_code=404, message="Admin doesn't exisits")
    # Response
    return BaseServerModel(status=200, message="Admin has been deleted successfully")
