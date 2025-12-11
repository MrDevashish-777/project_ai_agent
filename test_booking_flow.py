import sys
sys.path.insert(0, '.')
from chatbot import bot_reply, user_preferences, booking_state

print('=' * 70)
print('TESTING COMPLETE BOOKING FLOW WITH CONFIRMATION')
print('=' * 70)

test_user_id = "test_user_123"

messages = [
    ("hi", "User greeting"),
    ("I want a hotel under 3000 rupees for 3 nights", "User provides budget and nights"),
    ("show me hotels", "User asks to see hotels"),
    ("h1", "User selects first hotel"),
    ("book it", "User initiates booking"),
    ("John Doe", "User provides name"),
    ("9876543210", "User provides phone"),
    ("2025-12-25", "User provides check-in date"),
    ("yes", "User confirms booking"),
]

print()
for i, (message, description) in enumerate(messages, 1):
    print(f"\n{'='*70}")
    print(f"Step {i}: {description}")
    print(f"User Message: \"{message}\"")
    print(f"{'='*70}")
    
    reply, suggestions, meta = bot_reply(message, user_id=test_user_id)
    
    print(f"\nBot Reply:")
    print(reply)
    
    if suggestions:
        print(f"\nSuggestions/Hotels:")
        for s in suggestions:
            if isinstance(s, dict):
                print(f"  - {s.get('name', s.get('id'))}")
    
    if meta:
        print(f"\nMeta Info:")
        for key, value in meta.items():
            if key not in ['hotels', 'selected_hotel']:
                print(f"  - {key}: {value}")
            elif key == 'action':
                print(f"  - Action: {value}")
    
    if test_user_id in booking_state:
        state = booking_state[test_user_id]
        print(f"\nBooking State:")
        print(f"  - Current Step: {state['step']}")
        print(f"  - Hotel ID: {state.get('hotel_id')}")
        print(f"  - Name: {state.get('name')}")
        print(f"  - Phone: {state.get('phone')}")
        print(f"  - Check-in Date: {state.get('checkin_date')}")

print(f"\n{'='*70}")
print("FINAL VERIFICATION")
print(f"{'='*70}")

if test_user_id in booking_state:
    print("❌ Booking state still exists (should be cleared after confirmation)")
else:
    print("✅ Booking state properly cleared after confirmation")

print("\n✅ ALL BOOKING FLOW STEPS COMPLETED!")
print("=" * 70)
