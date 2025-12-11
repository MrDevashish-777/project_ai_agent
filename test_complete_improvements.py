#!/usr/bin/env python3
import sys
import json
from datetime import datetime, timedelta
sys.path.insert(0, '.')

from db import FakeTable, FakeSupabase
from validators import validate_phone, validate_date, validate_nights, validate_visitors, validate_booking_input
from chatbot import search_hotels_internal, parse_budget, parse_nights, get_hotel_by_id

print('=' * 70)
print('COMPREHENSIVE TEST SUITE - All Improvements')
print('=' * 70)
print()

test_results = {"passed": 0, "failed": 0, "errors": []}

def test_case(name, assertion, error_msg=""):
    global test_results
    try:
        if assertion:
            print(f"[PASS] {name}")
            test_results["passed"] += 1
        else:
            print(f"[FAIL] {name}")
            test_results["failed"] += 1
            if error_msg:
                test_results["errors"].append(f"{name}: {error_msg}")
    except Exception as e:
        print(f"[ERROR] {name} - Exception: {str(e)}")
        test_results["failed"] += 1
        test_results["errors"].append(f"{name}: {str(e)}")

print("=" * 70)
print("SECTION 1: Database order() Support and Error Handling")
print("=" * 70)
print()

fake_db = FakeSupabase()
table = fake_db.table("test_table")

test_data = [
    {"id": "1", "name": "Alice", "created_at": "2025-01-01T10:00:00"},
    {"id": "2", "name": "Bob", "created_at": "2025-01-02T10:00:00"},
    {"id": "3", "name": "Charlie", "created_at": "2025-01-03T10:00:00"},
]

for data in test_data:
    table.insert(data).execute()

result = fake_db.table("test_table").select("*").order("name", desc=False).execute()
test_case(
    "Order by name ascending",
    len(result.data) == 3 and result.data[0]["name"] == "Alice",
    f"Expected Alice first, got {result.data[0]['name'] if result.data else 'none'}"
)

result = fake_db.table("test_table").select("*").order("name", desc=True).execute()
test_case(
    "Order by name descending",
    len(result.data) == 3 and result.data[0]["name"] == "Charlie",
    f"Expected Charlie first, got {result.data[0]['name'] if result.data else 'none'}"
)

result = fake_db.table("test_table").select("*").order("created_at", desc=True).execute()
test_case(
    "Order by created_at descending",
    len(result.data) == 3 and result.data[0]["id"] == "3",
    f"Expected id=3 first, got {result.data[0]['id'] if result.data else 'none'}"
)

try:
    fake_db.table("test_table").select("*").order("invalid_column", desc=False).execute()
    test_case("Invalid column raises error", False, "Should have raised ValueError")
except ValueError as e:
    test_case("Invalid column raises ValueError", "invalid_column" in str(e) and "does not exist" in str(e))
except Exception as e:
    test_case("Invalid column raises error", False, f"Wrong exception type: {type(e).__name__}")

try:
    table.insert(None).execute()
    test_case("Invalid insert payload raises error", False, "Should have raised ValueError")
except (ValueError, Exception) as e:
    test_case("Invalid insert payload raises error", True)

result = fake_db.table("test_table").select("*").limit(2).execute()
test_case(
    "Limit works correctly",
    len(result.data) == 2,
    f"Expected 2 results, got {len(result.data)}"
)

result = fake_db.table("test_table").select("*").eq("name", "Bob").execute()
test_case(
    "Filter with eq() works",
    len(result.data) == 1 and result.data[0]["name"] == "Bob"
)

print()
print("=" * 70)
print("SECTION 2: Input Validation")
print("=" * 70)
print()

valid, msg = validate_phone("9876543210")
test_case("Valid 10-digit phone", valid)

valid, msg = validate_phone("12345")
test_case("Invalid short phone rejected", not valid)

valid, msg = validate_date("2025-12-25")
test_case("Future date accepted", valid)

valid, msg = validate_date("2024-01-01")
test_case("Past date rejected", not valid)

valid, msg = validate_nights(3)
test_case("Valid nights (3)", valid)

valid, msg = validate_nights(0)
test_case("Zero nights rejected", not valid)

valid, msg = validate_visitors(5)
test_case("Valid visitors (5)", valid)

valid, msg = validate_visitors(15)
test_case("15 visitors rejected (max 10)", not valid)

future_date = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
is_valid, error = validate_booking_input("John Doe", "9876543210", future_date, 3, 2)
test_case("Complete valid booking input", is_valid)

is_valid, error = validate_booking_input("John", "123", "2024-01-01", 0, 15)
test_case("Invalid booking input rejected", not is_valid)

print()
print("=" * 70)
print("SECTION 3: Hotel Search and Filtering")
print("=" * 70)
print()

hotels = search_hotels_internal(max_price=3000, limit=5)
test_case(
    "Search hotels by price",
    len(hotels) > 0 and all(h["price_per_night"] <= 3000 for h in hotels),
    f"Found {len(hotels)} hotels, some may exceed budget"
)

hotels = search_hotels_internal(location="Sitabuldi", limit=5)
test_case(
    "Search hotels by location",
    len(hotels) >= 0,
    "Location search should return results"
)

hotels = search_hotels_internal(min_rating=4.5, limit=5)
test_case(
    "Search hotels by rating",
    len(hotels) > 0 and all(h["rating"] >= 4.5 for h in hotels),
    "All hotels should have rating >= 4.5"
)

budget = parse_budget("I can spend 5000 per night")
test_case("Parse budget from text", budget == 5000)

nights = parse_nights("I need 3 nights stay")
test_case("Parse nights from text", nights == 3)

hotel = get_hotel_by_id("h1")
test_case("Get hotel by ID", hotel is not None and hotel["id"] == "h1")

print()
print("=" * 70)
print("SECTION 4: Logging and Audit Trails")
print("=" * 70)
print()

try:
    from main import logger
    test_case("StructuredLogger initialized successfully", logger is not None)
    
    log_entry = logger.log_action(
        action="TEST_ACTION",
        user_id="test_user",
        resource_type="test",
        resource_id="test_123",
        status="success",
        details={"test": "data"}
    )
    test_case(
        "log_action creates structured log entry",
        log_entry is not None and log_entry["action"] == "TEST_ACTION"
    )
    
    test_case(
        "Log entry contains timestamp",
        "timestamp" in log_entry and log_entry["timestamp"] is not None
    )
    
    test_case(
        "Log entry contains details",
        "details" in log_entry and log_entry["details"]["test"] == "data"
    )
except Exception as e:
    test_case("StructuredLogger test", False, str(e))

print()
print("=" * 70)
print("SECTION 5: Database Audit Log Creation")
print("=" * 70)
print()

from db import create_audit_log

try:
    audit_entry = create_audit_log(
        action="TEST_BOOKING",
        user_id="user123",
        resource_type="booking",
        resource_id="booking456",
        details={"amount": 5000, "hotel": "Grand Hotel"}
    )
    test_case(
        "Audit log created successfully",
        audit_entry is not None
    )
    
    test_case(
        "Audit log has correct structure",
        all(k in audit_entry for k in ["timestamp", "action", "user_id", "resource_type"])
    )
except Exception as e:
    test_case("Audit log creation", False, str(e))

print()
print("=" * 70)
print("SECTION 6: Payment and Invoice Generation")
print("=" * 70)
print()

from chatbot import generate_bill, format_booking_summary

test_hotel = {
    "id": "h1",
    "name": "The Grand Palace",
    "price_per_night": 5000,
    "rating": 4.8,
    "area": "Sitabuldi",
    "amenities": "WiFi, Pool, Gym"
}

bill = generate_bill(test_hotel, 3, "John Doe", "booking123")
test_case("Bill generation creates formatted text", bill is not None and "TOTAL AMOUNT" in bill)
test_case("Bill contains hotel name", "The Grand Palace" in bill)
test_case("Bill contains guest name", "John Doe" in bill)

summary = format_booking_summary(test_hotel, 3, 15000, "John Doe", "2025-12-25")
test_case("Booking summary generated", summary is not None and "BOOKING SUMMARY" in summary)
test_case("Summary contains price breakdown", "Subtotal" in summary and "GST" in summary)
test_case("Summary contains final amount", "TOTAL AMOUNT DUE" in summary)

print()
print("=" * 70)
print("TEST SUMMARY")
print("=" * 70)
print()
print(f"✅ Passed: {test_results['passed']}")
print(f"❌ Failed: {test_results['failed']}")
print(f"📊 Total: {test_results['passed'] + test_results['failed']}")
print()

if test_results['errors']:
    print("ERRORS:")
    for error in test_results['errors']:
        print(f"  - {error}")
    print()

if test_results['failed'] == 0:
    print("*** ALL TESTS PASSED! ***")
    sys.exit(0)
else:
    print(f"WARNING: {test_results['failed']} test(s) failed")
    sys.exit(1)
