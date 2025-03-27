from fastapi import APIRouter
from .authentication_request_models import LoginRequest
from .authetication_repository import *

router = APIRouter(tags=["Authentication"])


@router.post("/login")
async def login(request: LoginRequest):
    return await login_user(request=request)
