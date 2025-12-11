import sys
sys.path.insert(0, '.')
from chatbot import prepare_booking_confirmation, get_hotel_by_id

test_user_id = "test_user"
hotel_id = "h1"
name = "John Doe"
phone = "9876543210"
checkin_date = "2025-12-25"
nights = 3

hotel = get_hotel_by_id(hotel_id)
print("Hotel found:", hotel['name'] if hotel else "None")
print()

summary, booking_data = prepare_booking_confirmation(
    test_user_id, name, phone, hotel_id, checkin_date, nights
)

print("BOOKING SUMMARY DISPLAY:")
print("=" * 70)
print(summary)
print("=" * 70)
print()
print("Confirmation Request:")
print("Is this correct? Please confirm by saying 'yes' to proceed with the booking, or 'no' to go back.")
