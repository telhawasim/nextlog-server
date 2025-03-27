from .authentication_request_models import LoginRequest
from app.exception import CustomException
from app.mongodb import db
from app.jwt_token import create_access_token
from app.hash_password import verify_password
from ..admins.admin_serialization import admin_serialize
from .authentication_response_models import LoginResponseModel


async def login_user(request: LoginRequest):
    # Check if the role is 'admin'
    if request.role.lower() != "admin":
        raise CustomException(
            status_code=403, message="Access denied. Only admins can login"
        )
    # Get the first instance of admin from database
    admin = await db.admins.find_one({"email": request.email})
    # In case admin is null, throw an exception
    if not admin:
        raise CustomException(status_code=404, message="Admin not found")
    # In case password is not matched with the hashed password throw exception
    if not verify_password(request.password, admin["password"]):
        raise CustomException(status_code=401, message="Invalid email or password")
    # Generate access token
    token = create_access_token(
        {"id": str(admin["_id"]), "email": admin["email"], "role": "admin"}
    )
    # Seriazlied the data according to requirement
    serialized_admin = admin_serialize(admin=admin)
    # Response
    return LoginResponseModel(access_token=token, data=serialized_admin)
