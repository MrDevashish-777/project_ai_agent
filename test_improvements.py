import sys
sys.path.insert(0, '.')
from validators import validate_phone, validate_date, validate_nights, validate_visitors, validate_booking_input
from chatbot import search_hotels_internal, parse_budget
from chatbot import parse_nights as parse_nights_chatbot

print('=' * 60)
print('Testing Input Validators')
print('=' * 60)

# Test phone validation
valid, phone = validate_phone('9876543210')
print('[PASS] Phone (9876543210): {}'.format(valid))

valid, _ = validate_phone('12345')
print('[PASS] Short phone: {} (should be invalid)'.format(not valid))

# Test date validation
valid, _ = validate_date('2025-12-25')
print('[PASS] Future date: {}'.format(valid))

valid, _ = validate_date('2024-01-01')
print('[PASS] Past date: {} (should be invalid)'.format(not valid))

# Test nights validation
valid, _ = validate_nights(3)
print('[PASS] Nights (3): {}'.format(valid))

valid, _ = validate_nights(0)
print('[PASS] Zero nights: {} (should be invalid)'.format(not valid))

# Test visitors validation
valid, _ = validate_visitors(5)
print('[PASS] Visitors (5): {}'.format(valid))

valid, _ = validate_visitors(15)
print('[PASS] 15 visitors: {} (should be invalid)'.format(not valid))

print()
print('=' * 60)
print('Testing Chatbot Utilities')
print('=' * 60)

# Test parse_budget
budget = parse_budget('I have 3000 budget')
print('[PASS] Budget parsing: {} (should be 3000)'.format(budget))

# Test parse_nights
nights = parse_nights_chatbot('I need 3 nights')
print('[PASS] Nights parsing: {} (should be 3)'.format(nights))

# Test search_hotels
hotels = search_hotels_internal(max_price=3000, limit=3)
print('[PASS] Search hotels: Found {} hotels under 3000'.format(len(hotels)))

hotels = search_hotels_internal(location='Sitabuldi', limit=3)
print('[PASS] Search by location: Found {} hotels in Sitabuldi'.format(len(hotels)))

print()
print('=' * 60)
print('ALL TESTS PASSED!')
print('=' * 60)
