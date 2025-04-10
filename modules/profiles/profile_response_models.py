from pydantic import BaseModel

from modules.profiles.profile import Profile, ProfileExperience


class ProfileModel(BaseModel):
    id: str
    title: str
    created_at: str


class EmployeeDetailProfileModel(BaseModel):
    id: str
    title: str
    created_at: str


class ProfileDetailEmployeeModel(BaseModel):
    id: str
    name: str
    avatar: str


class ProfileDetailResponseModel(BaseModel):
    employee: ProfileDetailEmployeeModel
    profile: Profile
