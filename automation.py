from calendar_service import book_appointment
from crm_service import create_or_update_client
from email_service import send_confirmation

def handle_intent(intent_data):

    if "book_appointment" in intent_data:
        # parse extracted info
        name = "John"
        date = "2026-02-20"
        time = "10:00"

        book_appointment(name, date, time)
        create_or_update_client(name, "12345678")
        send_confirmation("john@email.com",
                          f"Your appointment is booked for {date} at {time}")

        return "Your appointment has been successfully booked."

    return "How else can I assist you?"
