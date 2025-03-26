from pydantic import BaseModel


class BaseServerModel(BaseModel):
    message: str
    status: int
