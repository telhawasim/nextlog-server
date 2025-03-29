from .authentication_request_models import LoginRequest
from app.exception import CustomException
from app.mongodb import db
from app.jwt_token import create_access_token
from app.hash_password import verify_password
from ..admins.admin_serialization import admin_serialize
from .authentication_response_models import LoginResponseModel


async def login_user(request: LoginRequest):
    # In case login user is employee
    if request.role.lower() == "employee":
        # Extract the employee
        employee = await db.employees.find_one({"email": request.email})
        # Check if the employee is null
        if not employee:
            raise CustomException(status_code=404, message="Employee does not exist")
        # Check the employee ID is same as per the request
        if request.emp_id != employee["emp_id"]:
            raise CustomException(status_code=404, message="Employee ID does not exist")
        # Generate the token
        token = create_access_token(
            {
                "id": str(employee["_id"]),
                "email": employee["email"],
                "role": "employee",
            }
        )
        # Serialize the employee object
        serialized_employee = admin_serialize(employee)
        # Response
        return LoginResponseModel(access_token=token, data=serialized_employee)
    else:
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
        serialized_admin = admin_serialize(admin)
        # Response
        return LoginResponseModel(access_token=token, data=serialized_admin)
