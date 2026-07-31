from pydantic import BaseModel


class ReservationCreate(BaseModel):
    guest_phone: str
    room_name: str
    reservation_date: str