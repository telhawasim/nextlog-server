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


class AddExperience(BaseModel):
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
    current_experience: AddExperience
    previous_experience: Optional[List[AddExperience]] = None


class AddQualification(BaseModel):
    degree: str
    institution: str
    start_date: str
    end_date: str

    def add_qualification_validation(self):
        if not self.degree:
            raise CustomException(status_code=422, message="Degree is required")
        if not self.institution:
            raise CustomException(status_code=422, message="Institution is required")
        if not self.start_date:
            raise CustomException(status_code=422, message="Start date is required")
        if not self.end_date:
            raise CustomException(status_code=422, message="End date is required")


class AddCertification(BaseModel):
    course_name: str
    institution: str
    start_date: str
    end_date: str

    def add_cerfication_validation(self):
        if not self.course_name:
            raise CustomException(status_code=422, message="Course name is required")
        if not self.institution:
            raise CustomException(status_code=422, message="Institution is required")
        if not self.start_date:
            raise CustomException(status_code=422, message="Start date is required")
        if not self.end_date:
            raise CustomException(status_code=422, message="End date is required")


class AddQualificationRequest(BaseModel):
    qualification: List[AddQualification]
    certification: Optional[List[AddCertification]] = None


class AddSkill(BaseModel):
    name: str

    def add_skill_validation(self):
        if not self.name:
            raise CustomException(status_code=422, message="Skill name is required")


class AddSkillRequest(BaseModel):
    technical_skills: Optional[List[AddSkill]] = None
    non_technical_skills: Optional[List[AddSkill]] = None
    tools: Optional[List[AddSkill]] = None
