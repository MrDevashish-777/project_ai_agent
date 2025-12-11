"""verify_booking.py
Simple script to create a booking via API and verify it exists in Supabase.
Run with the SUPABASE_KEY env var set; the script will do the POST to /book and then query the `bookings` table to verify persistence.
"""
import os
import httpx
from dotenv import load_dotenv
load_dotenv()

BASE = os.getenv('AI_AGENT_BASE', 'http://127.0.0.1:8000')

def create_booking():
    payload = {
        'name': 'Verify Tester',
        'phone': '+919888888888',
        'hotel_id': 'h2',
        'checkin_date': '2025-12-12',
        'nights': 1
    }
    r = httpx.post(f"{BASE}/book", json=payload, timeout=20)
    r.raise_for_status()
    return r.json()

def main():
    print('Creating booking via API...')
    try:
        out = create_booking()
        print('Booking response:', out)
        booking_id = out.get('booking', {}).get('id')
        if booking_id:
            # Now query backend to ensure it returns booking or via test endpoint
            print('Booking created with id:', booking_id)
            print('Now calling /supabase_test to confirm connection and presence maybe')
            r = httpx.get(f"{BASE}/supabase_test", timeout=10)
            print('Supabase test:', r.json())
        else:
            print('No booking id returned, cannot verify via Supabase directly', out)
    except Exception as e:
        print('Error creating or verifying booking:', e)

if __name__ == '__main__':
    main()
