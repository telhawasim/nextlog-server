from pydantic import BaseModel
from ..admins.admin_response_models import AdminModel


class LoginResponseModel(BaseModel):
    access_token: str
    data: AdminModel
