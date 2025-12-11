import os
import sys
import httpx
from dotenv import load_dotenv
load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://dehuipkdltaiumsifyka.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
SUPABASE_DB_URL = os.getenv('SUPABASE_DB_URL') or os.getenv('DATABASE_URL')

TABLES = ['users', 'bookings', 'conversations']

# Try DB connection via psycopg if present
try:
    import psycopg
    PSYCOPG_TYPE = 'psycopg'
except Exception:
    try:
        import psycopg2
        PSYCOPG_TYPE = 'psycopg2'
    except Exception:
        PSYCOPG_TYPE = None


if PSYCOPG_TYPE and SUPABASE_DB_URL:
    print('Attempting to query tables via DB connection (SUPABASE_DB_URL)')
    try:
        if PSYCOPG_TYPE == 'psycopg':
            with psycopg.connect(SUPABASE_DB_URL) as conn:
                with conn.cursor() as cur:
                    for t in TABLES:
                        cur.execute("SELECT to_regclass('public.%s');" % t)
                        exists = cur.fetchone()[0]
                        print(t, 'exists:', bool(exists))
        else:
            conn = psycopg2.connect(SUPABASE_DB_URL)
            cur = conn.cursor()
            for t in TABLES:
                cur.execute("SELECT to_regclass('public.%s');" % t)
                exists = cur.fetchone()[0]
                print(t, 'exists:', bool(exists))
            cur.close()
            conn.close()
    except Exception as e:
        print('Error querying DB:', e)
else:
    # Fall back to PostgREST check using SUPABASE_URL and SUPABASE_KEY
    print('No DB connection URL available or psycopg not installed; falling back to PostgREST check')
    headers = {}
    if SUPABASE_KEY:
        headers['apikey'] = SUPABASE_KEY
        headers['Authorization'] = f'Bearer {SUPABASE_KEY}'
    for t in TABLES:
        try:
            url = f"{SUPABASE_URL}/rest/v1/{t}?limit=1"
            r = httpx.get(url, headers=headers, timeout=10)
            print(t, '->', r.status_code)
            if r.status_code == 200:
                print('  returned:', r.text)
            elif r.status_code:
                print('  error:', r.text)
        except Exception as e:
            print('  exception querying', t, e)

print('\nDone')
