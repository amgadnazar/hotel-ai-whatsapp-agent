from pydantic import BaseModel

class GuestCreate(BaseModel):
    phone: str
    name: str
    age: int
    gender: str