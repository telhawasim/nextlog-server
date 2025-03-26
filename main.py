from fastapi import FastAPI
from modules.departments.department_router import router as department_router
from app.exception import custom_exception_handler, CustomException

app = FastAPI()

app.add_exception_handler(CustomException, custom_exception_handler)

app.include_router(department_router)
