from typing import Optional

from pydantic import BaseModel, Field, validator


class MeetingRoomCreate(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str]

    @validator('name')
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not value.strip():
            raise ValueError(
                'Название не может быть пустым или состоять только из пробелов'
            )
        if len(value) > 100:
            raise ValueError('Название не может превышать 100 символов')

        return value
