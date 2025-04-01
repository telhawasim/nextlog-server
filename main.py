from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from modules.departments.department_router import router as department_router
from modules.designations.designation_router import router as designation_router
from modules.admins.admin_router import router as admin_router
from modules.authentication.authentication_router import router as authentication_router
from modules.employees.employee_router import router as employee_router
from modules.profiles.profile_router import router as profile_router
from app.exception import custom_exception_handler, CustomException

app = FastAPI()

app.mount("/upload", StaticFiles(directory="uploads"), name="uploads")
app.add_exception_handler(CustomException, custom_exception_handler)

app.include_router(authentication_router)
app.include_router(admin_router)
app.include_router(employee_router)
app.include_router(department_router)
app.include_router(designation_router)
app.include_router(profile_router)
