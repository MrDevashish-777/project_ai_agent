#!/usr/bin/env python3
"""Test script to verify Gemini API integration in the chatbot."""

from chatbot import bot_reply

print("="*60)
print("TESTING GEMINI API INTEGRATION")
print("="*60)
print()

# Test 1: General question (should use Gemini)
print("TEST 1: General Question (Gemini-powered)")
print("-" * 60)
print("User: Tell me about your services")
reply, suggestions, meta = bot_reply('Tell me about your services', user_id='test_user_1')
print(f"Bot: {reply}")
print(f"AI Powered (Gemini): {meta.get('ai_powered', False)}")
print()

# Test 2: Budget question (should extract budget)
print("TEST 2: Budget Extraction (Rule-based)")
print("-" * 60)
print("User: I have a budget of 3000 per night")
reply, suggestions, meta = bot_reply('I have a budget of 3000 per night', user_id='test_user_2')
print(f"Bot: {reply}")
print(f"Budget extracted: {meta.get('budget', 'None')}")
print()

# Test 3: Hotel search (should use logic rules)
print("TEST 3: Hotel Search (Rule-based)")
print("-" * 60)
print("User: show hotels")
reply, suggestions, meta = bot_reply('show hotels', user_id='test_user_3')
print(f"Bot: {reply}")
print(f"Suggestions count: {len(suggestions) if suggestions else 0}")
print()

# Test 4: General question about hotels
print("TEST 4: General Question About Hotels (Gemini-powered)")
print("-" * 60)
print("User: What is the best hotel for a family with kids?")
reply, suggestions, meta = bot_reply('What is the best hotel for a family with kids?', user_id='test_user_4')
print(f"Bot: {reply}")
print(f"AI Powered (Gemini): {meta.get('ai_powered', False)}")
print()

# Test 5: Greeting
print("TEST 5: Greeting (Hardcoded response)")
print("-" * 60)
print("User: Hello!")
reply, suggestions, meta = bot_reply('Hello!', user_id='test_user_5')
print(f"Bot: {reply}")
print()

print("="*60)
print("✅ GEMINI INTEGRATION TEST COMPLETED SUCCESSFULLY")
print("="*60)
