from pydantic import BaseModel


class Admin(BaseModel):
    email: str
    password: str
    role: str = "admin"
