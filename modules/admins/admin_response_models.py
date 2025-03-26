from pydantic import BaseModel
from typing import List
from typing import List


class AdminModel(BaseModel):
    id: str
    email: str
    role: str


class GetAllAdminResponesModel(BaseModel):
    admins: List[AdminModel]


class GetAdminResponseModel(BaseModel):
    data: AdminModel


# class GetAllDesignationsModel(BaseModel):
#     designations: List[AdminModel]
