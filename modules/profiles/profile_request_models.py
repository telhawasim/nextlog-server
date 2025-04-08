from typing import List, Optional
from pydantic import BaseModel
from app.exception import CustomException
from modules.profiles.profile import Experience


class AddProfile(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None

    def add_profile_validation(self):
        if not self.id:
            raise CustomException(status_code=422, message="Employee ID is required")
        if not self.name:
            raise CustomException(status_code=422, message="Profile name is required")


class AddBasicInformation(BaseModel):
    name: Optional[str] = None
    designation: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    git_link: Optional[str] = None
    linked_in_link: Optional[str] = None
    summary: Optional[str] = None

    def add_basic_information_validation(self):
        if not self.name:
            raise CustomException(status_code=422, message="Name is required")
        if not self.designation:
            raise CustomException(status_code=422, message="Designation is required")
        if not self.email:
            raise CustomException(status_code=422, message="Email is required")
        if not self.phone:
            raise CustomException(status_code=422, message="Phone number is required")
        if not self.summary:
            raise CustomException(status_code=422, message="Summar is required")


class AddExperienceRequest(BaseModel):
    company_name: str
    designation: str
    start_date: str
    end_date: str
    description: str

    def add_experience_validation(self):
        if not self.company_name:
            raise CustomException(status_code=422, message="Company name is required")
        if not self.designation:
            raise CustomException(status_code=422, message="Designation is required")
        if not self.start_date:
            raise CustomException(status_code=422, message="Start date is required")
        if not self.end_date:
            raise CustomException(status_code=422, message="End date is required")
        if not self.description:
            raise CustomException(status_code=422, message="Description is required")


class AddExperienceRequest(BaseModel):
    current_experience: AddExperienceRequest
    previous_experience: Optional[List[AddExperienceRequest]] = None
