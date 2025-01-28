from pydantic import BaseModel


class ErrorOut(BaseModel):
    result: bool = False
    error_type: str
    error_message: str


class GoodOut(BaseModel):
    result: bool = True

    class Config:
        from_attributes = True
