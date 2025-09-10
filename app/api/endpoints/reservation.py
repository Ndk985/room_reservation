from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_meeting_room_exists, check_reservation_intersections
)

from app.core.db import get_async_session
from app.schemas.reservation import ReservationCreate, ReservationDB
from app.crud.reservation import reservation_crud


router = APIRouter()


@router.post(
    '/',
    response_model=ReservationDB,
)
async def create_reservation(
    reservation: ReservationCreate,
    session: AsyncSession = Depends(get_async_session),
):
    await check_meeting_room_exists(
        meeting_room_id=reservation.meetingroom_id,
        session=session
    )
    await check_reservation_intersections(
        **reservation.dict(), session=session
    )
    new_reservation = await reservation_crud.create(
        obj_in=reservation,
        session=session
    )
    return new_reservation
