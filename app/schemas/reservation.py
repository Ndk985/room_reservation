from datetime import datetime
from pydantic import BaseModel, Field, root_validator, validator


class ReservationBase(BaseModel):
    from_reserve: datetime = Field(..., example="2024-01-01T10:00:00")
    to_reserve: datetime = Field(..., example="2024-01-01T11:00:00")


class ReservationUpdate(ReservationBase):

    @validator('from_reserve')
    def check_from_reserve_later_than_now(cls, value):
        if value <= datetime.now():
            raise ValueError(
                'Время начала бронирования '
                'не может быть меньше текущего времени'
            )
        return value

    @root_validator(skip_on_failure=True)
    def check_from_reserve_before_to_reserve(cls, values):
        if values["from_reserve"] >= values["to_reserve"]:
            raise ValueError(
                'Время начала бронирования '
                'не может быть больше времени окончания'
            )
        return values


class ReservationCreate(ReservationUpdate):
    meetingroom_id: int = Field(..., gt=0, example=1)


class ReservationDB(ReservationCreate):
    id: int
    meetingroom_id: int

    class Config:
        orm_mode = True
