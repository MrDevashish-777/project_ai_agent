import os
from dotenv import load_dotenv
import sys

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print(f"Checking Supabase Connection...")
print(f"URL: {SUPABASE_URL}")
print(f"KEY: {SUPABASE_KEY[:10]}..." if SUPABASE_KEY else "KEY: Not Set")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ Error: SUPABASE_URL or SUPABASE_KEY is missing in .env file")
    sys.exit(1)

try:
    from supabase import create_client, Client
except ImportError:
    print("❌ Error: 'supabase' package not installed. Run: pip install supabase")
    sys.exit(1)

try:
    print("Attempting to create client...")
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    print("Attempting to query 'users' table...")
    # Try a simple query
    response = supabase.table('users').select('*').limit(1).execute()
    
    print("✅ Connection Successful!")
    print(f"Data received: {response.data}")
    
except Exception as e:
    print("\n❌ Connection Failed!")
    print(f"Error Type: {type(e).__name__}")
    print(f"Error Message: {str(e)}")
    
    if "relation \"public.users\" does not exist" in str(e):
        print("\n💡 Hint: The 'users' table does not exist. Please run the SQL from 'supabase_tables.sql' in your Supabase SQL Editor.")
    elif "connection refused" in str(e).lower():
        print("\n💡 Hint: Network error. Check your internet connection or URL.")
    elif "apikey" in str(e).lower() or "jwt" in str(e).lower():
        print("\n💡 Hint: Authentication failed. Check your SUPABASE_KEY.")
