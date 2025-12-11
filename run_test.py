"""run_test.py
Quick script to show how to get output from the core functions without starting the API.
This helps validate that the bot reply and data sources work locally.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
from chatbot import bot_reply, find_hotels_by_budget

def main():
    print("== Example 1: greeting -> bot_reply\n")
    r, s, m = bot_reply("Hi there!")
    # print safely to avoid unicode encoding errors on Windows terminals
    print("Reply:", str(r).encode('utf-8', errors='replace').decode('utf-8'))
    print("Suggestions:", s)
    print("Meta:", m)

    print("\n== Example 2: budget -> bot_reply\n")
    r, s, m = bot_reply("My budget is 2500 per night")
    print("Reply:", str(r).encode('utf-8', errors='replace').decode('utf-8'))
    print("Number of suggestions:", len(s) if s else 0)
    if s:
        for h in s[:3]:
            print(h)

    print("\n== Example 3: booking flow parse -> bot_reply\n")
    msg = "I want to book h2 name:John Doe phone: +919876543210 2025-12-12 nights 2"
    r, s, m = bot_reply(msg)
    print("Reply:", str(r).encode('utf-8', errors='replace').decode('utf-8'))
    print("Meta:", m)

if __name__ == '__main__':
    main()
