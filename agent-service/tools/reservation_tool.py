from db.supabase_client import supabase


def create_reservation(
    guest_phone: str,
    room_name: str,
    reservation_date: str
):

    supabase.table("reservations").insert({
        "guest_phone": guest_phone,
        "room_name": room_name,
        "reservation_date": reservation_date
    }).execute()

    return "Reservation Created"