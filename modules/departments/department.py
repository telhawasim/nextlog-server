from pydantic import BaseModel, Field
from bson import ObjectId


class Department(BaseModel):
    name: str
