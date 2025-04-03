from pydantic import BaseModel


class ProfileModel(BaseModel):
    id: str
    title: str
    created_at: str


class EmployeeDetailProfileModel(BaseModel):
    id: str
    title: str
    created_at: str
