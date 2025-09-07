from typing import Optional

from pydantic import BaseModel, Field, field_validator


class MeetingRoomCreate(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str]

    @field_validator('name')
    @classmethod
    def validate_name(cls, value: str) -> str:
        # Проверка на пустую строку
        if not value.strip():
            raise ValueError(
                'Название не может быть пустым или состоять только из пробелов'
            )
        # Проверка длины (уже есть в Field, но для надежности можно добавить)
        if len(value) > 100:
            raise ValueError('Название не может превышать 100 символов')

        return value
