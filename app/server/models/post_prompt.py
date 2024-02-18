from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class PostPromptSchema(BaseModel):
    email: EmailStr = Field(...)
    prompt: str = Field(...)
    image_url: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "jdoe@x.edu.ng",
                "prompt": "feel like dancing ",
                "image_url": "https://example.com/",
            }
        }


class UpdatePostPromptModel(BaseModel):
    email: Optional[EmailStr]
    prompt: Optional[str]
    image_url: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "email": "jdoe@x.edu.ng",
                "prompt": "feel like dancing ",
                "image_url": "https://example.com/",
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}