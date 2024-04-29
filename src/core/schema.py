from pydantic import BaseModel as pydantic_BaseModel


class BaseModel(pydantic_BaseModel):
    pass


class ExceptionModel(BaseModel):
    detail: str
