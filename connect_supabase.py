"""connect_supabase.py
Quick script to test the Supabase connection and print useful diagnostics.
"""
import os
from db import test_supabase_connection, SUPABASE_URL, USE_FAKE
from dotenv import load_dotenv

load_dotenv()

def main():
    print('Testing Supabase connection using SUPABASE_URL:', SUPABASE_URL)
    print('Using Fake DB fallback:', USE_FAKE)
    info = test_supabase_connection()
    print('Connection info:')
    for k,v in info.items():
        print('  ', k, ':', v)

if __name__ == '__main__':
    main()
