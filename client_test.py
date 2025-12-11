"""client_test.py
Small script that hits the local API endpoints and prints output.
"""
import httpx
import os

BASE = os.getenv('AI_AGENT_BASE', 'http://127.0.0.1:8000')

def post_chat(msg, user_id='u1'):
    url = f"{BASE}/chat"
    payload = {"message": msg, "user_id": user_id}
    r = httpx.post(url, json=payload, timeout=10)
    return r.json()

def get_hotels(max_price=None):
    url = f"{BASE}/hotels"
    params = {}
    if max_price:
        params['max_price'] = max_price
    r = httpx.get(url, params=params, timeout=10)
    return r.json()

def book(name, phone, hotel_id, checkin_date, nights):
    url = f"{BASE}/book"
    payload = {
        "name": name,
        "phone": phone,
        "hotel_id": hotel_id,
        "checkin_date": checkin_date,
        "nights": nights
    }
    r = httpx.post(url, json=payload, timeout=10)
    return r.json()

if __name__ == '__main__':
    print('Chat example ->', post_chat('Hi'))
    print('Budget example ->', post_chat('Budget 2500'))
    print('Hotels ->', get_hotels(max_price=2500))
    print('Book ->', book('Alice', '+919999999999','h2','2025-12-12',2))
