import sys
import os
sys.stdout.reconfigure(encoding='utf-8') if hasattr(sys.stdout, 'reconfigure') else None
sys.path.insert(0, '.')

from chatbot import bot_reply, booking_state

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

for i, (message, description) in enumerate(messages, 1):
    print()
    print('='*70)
    print(f'Step {i}: {description}')
    print(f'User Message: "{message}"')
    print('='*70)
    
    try:
        reply, suggestions, meta = bot_reply(message, user_id=test_user_id)
        
        reply_preview = reply[:200].replace('\n', ' ')
        print(f'Bot Reply (preview): {reply_preview}...')
        
        if suggestions:
            print(f'Suggestions: {len(suggestions)} items')
        
        if meta and 'action' in meta:
            print(f'Action: {meta["action"]}')
        
        if test_user_id in booking_state:
            state = booking_state[test_user_id]
            print(f'Booking State Step: {state["step"]}')
            if state.get('name'):
                print(f'  - Name: {state["name"]}')
            if state.get('phone'):
                print(f'  - Phone: {state["phone"]}')
            if state.get('checkin_date'):
                print(f'  - Check-in: {state["checkin_date"]}')
    except Exception as e:
        print(f'ERROR: {e}')
        import traceback
        traceback.print_exc()

print()
print('='*70)
print('FINAL VERIFICATION')
print('='*70)

if test_user_id not in booking_state:
    print('PASS: Booking state properly cleared after confirmation')
else:
    print('FAIL: Booking state still exists')

print()
print('BOOKING FLOW TEST COMPLETE')
print('='*70)
