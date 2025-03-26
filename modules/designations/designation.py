from pydantic import BaseModel


class Designation(BaseModel):
    name: str
