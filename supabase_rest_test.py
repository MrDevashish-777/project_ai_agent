"""supabase_rest_test.py
Query the Supabase REST API (PostgREST) directly to see whether the 'users', 'bookings', 'conversations' endpoints exist and are queryable.
"""
import os
import httpx
from dotenv import load_dotenv
load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://dehuipkdltaiumsifyka.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

HEADERS = {}
if SUPABASE_KEY:
    HEADERS['apikey'] = SUPABASE_KEY
    HEADERS['Authorization'] = f'Bearer {SUPABASE_KEY}'

TABLES = ['users', 'bookings', 'conversations']

def query_table(table):
    url = f"{SUPABASE_URL}/rest/v1/{table}?limit=1"
    try:
        r = httpx.get(url, headers=HEADERS, timeout=10)
        return r.status_code, r.text
    except Exception as e:
        return None, str(e)

def main():
    print('SUPABASE_URL', SUPABASE_URL)
    print('SUPABASE_KEY set?', bool(SUPABASE_KEY))
    for t in TABLES:
        code, body = query_table(t)
        print(t, '->', code)
        if code == 200:
            print('  returned:', body)
        elif code:
            print('  error:', body)
        else:
            print('  exception:', body)

if __name__ == '__main__':
    main()
