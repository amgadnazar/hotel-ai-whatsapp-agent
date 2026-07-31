from fastapi import FastAPI

from schemas.guest import GuestCreate
from schemas.chat import ChatRequest
from schemas.reservation import ReservationCreate

from db.supabase_client import supabase
from agent.agent import run_agent

app = FastAPI()


@app.get("/")
def root():
    return {"status": "running"}


@app.post("/chat")
def chat(request: ChatRequest):

    try:

        answer = run_agent(
            request.phone,
            request.text
        )

    except Exception as e:

        print("CHAT ERROR:", e)

        answer = (
            "عذراً، حدث خطأ في النظام."
            "\nيرجى المحاولة مرة أخرى بعد قليل."
        )

    return {
        "reply": answer
    }


@app.post("/guest")
def create_guest(guest: GuestCreate):

    supabase.table("guests").insert({
        "phone": guest.phone,
        "name": guest.name,
        "age": guest.age,
        "gender": guest.gender
    }).execute()

    return {
        "message": "Guest created successfully"
    }


@app.post("/reservation")
def create_reservation(request: ReservationCreate):

    supabase.table("reservations").insert({
        "guest_phone": request.guest_phone,
        "room_name": request.room_name,
        "reservation_date": request.reservation_date
    }).execute()

    return {
        "message": "Reservation created successfully"
    }