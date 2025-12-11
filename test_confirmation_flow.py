#!/usr/bin/env python3
"""Test the improved booking confirmation flow per spec."""

import sys
import io
from chatbot import bot_reply
import uuid

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def test_confirmation_flow():
    """Test the complete booking confirmation flow."""
    user_id = f"test_user_{uuid.uuid4().hex[:6]}"
    
    print("=" * 80)
    print("TESTING BOOKING CONFIRMATION FLOW")
    print("=" * 80)
    
    print("\n[STEP 1] GREETING")
    reply, suggestions, meta = bot_reply("Hi", user_id=user_id)
    print(f"Bot: {reply}\n")
    
    print("[STEP 2] SET BUDGET")
    reply, suggestions, meta = bot_reply("3000", user_id=user_id)
    print(f"Bot: {reply}\n")
    
    print("[STEP 3] SET NIGHTS")
    reply, suggestions, meta = bot_reply("2 nights", user_id=user_id)
    print(f"Bot: {reply}\n")
    
    print("[STEP 4] SHOW HOTELS")
    reply, suggestions, meta = bot_reply("show hotels", user_id=user_id)
    print(f"Bot: {reply}")
    if suggestions:
        print(f"Hotels shown: {len(suggestions)}")
        for hotel in suggestions[:2]:
            print(f"  - {hotel['name']} ({hotel['price_per_night']}/night)")
    print()
    
    print("[STEP 5] SELECT HOTEL")
    reply, suggestions, meta = bot_reply("h1", user_id=user_id)
    print(f"Bot: {reply}\n")
    
    print("[STEP 6] INITIATE BOOKING")
    reply, suggestions, meta = bot_reply("book", user_id=user_id)
    print(f"Bot: {reply}\n")
    
    print("[STEP 7] PROVIDE NAME")
    reply, suggestions, meta = bot_reply("John Doe", user_id=user_id)
    print(f"Bot: {reply}\n")
    
    print("[STEP 8] PROVIDE PHONE")
    reply, suggestions, meta = bot_reply("9876543210", user_id=user_id)
    print(f"Bot: {reply}\n")
    
    print("[STEP 9] PROVIDE CHECK-IN DATE")
    reply, suggestions, meta = bot_reply("2025-12-25", user_id=user_id)
    print(f"Bot: {reply}\n")
    
    print("=" * 80)
    print("CONFIRMATION STEP - This should show detailed booking summary")
    print("=" * 80)
    print()
    
    print("[STEP 10] CONFIRM BOOKING (YES)")
    reply, suggestions, meta = bot_reply("yes", user_id=user_id)
    print(f"Bot: {reply}")
    if meta.get("booking_confirmed"):
        print("[SUCCESS] Booking confirmed!")
        print(f"Action: {meta.get('action')}")
    print()
    
    print("=" * 80)
    print("TEST 2: Cancel Booking")
    print("=" * 80)
    
    user_id_2 = f"test_user_{uuid.uuid4().hex[:6]}"
    
    print("\nRestarting flow for second test...\n")
    
    reply, _, _ = bot_reply("Hi", user_id=user_id_2)
    reply, _, _ = bot_reply("2500", user_id=user_id_2)
    reply, _, _ = bot_reply("3 nights", user_id=user_id_2)
    reply, _, _ = bot_reply("show hotels", user_id=user_id_2)
    reply, _, _ = bot_reply("h2", user_id=user_id_2)
    reply, _, _ = bot_reply("book", user_id=user_id_2)
    reply, _, _ = bot_reply("Jane Smith", user_id=user_id_2)
    reply, _, _ = bot_reply("9123456789", user_id=user_id_2)
    reply, _, _ = bot_reply("2025-12-30", user_id=user_id_2)
    
    print("Showing confirmation summary again:")
    print(reply)
    print()
    
    print("User cancels booking (NO):")
    reply, _, meta = bot_reply("no", user_id=user_id_2)
    print(f"Bot: {reply}")
    print()
    
    print("=" * 80)
    print("TEST 3: Incomplete confirmation response")
    print("=" * 80)
    
    user_id_3 = f"test_user_{uuid.uuid4().hex[:6]}"
    
    reply, _, _ = bot_reply("Hi", user_id=user_id_3)
    reply, _, _ = bot_reply("4000", user_id=user_id_3)
    reply, _, _ = bot_reply("1 night", user_id=user_id_3)
    reply, _, _ = bot_reply("show hotels", user_id=user_id_3)
    reply, _, _ = bot_reply("h3", user_id=user_id_3)
    reply, _, _ = bot_reply("book", user_id=user_id_3)
    reply, _, _ = bot_reply("Test User", user_id=user_id_3)
    reply, _, _ = bot_reply("9000000000", user_id=user_id_3)
    reply, _, _ = bot_reply("2025-12-20", user_id=user_id_3)
    
    print("Showing confirmation:")
    print(reply)
    print()
    
    print("User gives invalid confirmation response:")
    reply, _, _ = bot_reply("maybe later", user_id=user_id_3)
    print(f"Bot: {reply}")
    print()
    
    print("=" * 80)
    print("CONFIRMATION FLOW TEST COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    test_confirmation_flow()
