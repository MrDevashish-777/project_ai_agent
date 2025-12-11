#!/usr/bin/env python3
"""Test confirmation keyword detection."""

import sys
import io
from chatbot import bot_reply
import uuid

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def test_keywords():
    """Test confirmation keyword detection."""
    user_id = f"test_user_{uuid.uuid4().hex[:6]}"
    
    print("Testing keyword detection for confirmation step\n")
    
    print("Setting up booking state...")
    reply, _, _ = bot_reply("Hi", user_id=user_id)
    reply, _, _ = bot_reply("3000", user_id=user_id)
    reply, _, _ = bot_reply("2 nights", user_id=user_id)
    reply, _, _ = bot_reply("show hotels", user_id=user_id)
    reply, _, _ = bot_reply("h1", user_id=user_id)
    reply, _, _ = bot_reply("book", user_id=user_id)
    reply, _, _ = bot_reply("John Doe", user_id=user_id)
    reply, _, _ = bot_reply("9876543210", user_id=user_id)
    reply, _, _ = bot_reply("2025-12-25", user_id=user_id)
    
    print("Confirmation summary shown. Now testing keywords:\n")
    
    test_cases = [
        ("yes", "Should confirm"),
        ("YES", "Should confirm (uppercase)"),
        ("confirm", "Should confirm"),
        ("ok", "Should confirm"),
        ("y", "Should confirm"),
        ("no", "Should cancel"),
        ("NO", "Should cancel (uppercase)"),
        ("cancel", "Should cancel"),
        ("n", "Should cancel"),
        ("maybe later", "Should ask for clarification"),
        ("not sure", "Should ask for clarification"),
        ("I'm unsure", "Should ask for clarification"),
        ("proceed", "Should confirm"),
        ("book it", "Should confirm"),
    ]
    
    for test_input, expected in test_cases:
        user_id = f"test_user_{uuid.uuid4().hex[:6]}"
        
        print("=" * 60)
        print(f"Setting up new booking state...")
        reply, _, _ = bot_reply("Hi", user_id=user_id)
        reply, _, _ = bot_reply("3000", user_id=user_id)
        reply, _, _ = bot_reply("2 nights", user_id=user_id)
        reply, _, _ = bot_reply("show hotels", user_id=user_id)
        reply, _, _ = bot_reply("h1", user_id=user_id)
        reply, _, _ = bot_reply("book", user_id=user_id)
        reply, _, _ = bot_reply("John Doe", user_id=user_id)
        reply, _, _ = bot_reply("9876543210", user_id=user_id)
        reply, _, _ = bot_reply("2025-12-25", user_id=user_id)
        
        print(f"Test Input: '{test_input}'")
        print(f"Expected: {expected}")
        reply, _, meta = bot_reply(test_input, user_id=user_id)
        
        print(f"Response: {reply[:100]}...")
        if "confirmed" in reply.lower():
            print("Result: CONFIRMED")
        elif "cancelled" in reply.lower():
            print("Result: CANCELLED")
        elif "Please confirm" in reply:
            print("Result: ASKED FOR CLARIFICATION")
        else:
            print(f"Result: OTHER")
        print()

if __name__ == "__main__":
    test_keywords()
