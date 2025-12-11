import os
import sys
from dotenv import load_dotenv
from db import test_supabase_connection

def main():
    print("--- Supabase Cloud Setup Verification ---\n")

    # 1. Check .env file
    if not os.path.exists('.env'):
        print("❌ Error: .env file not found.")
        print("   Please copy .env.example to .env and add your credentials.")
        return

    load_dotenv()

    # 2. Check Environment Variables
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_KEY')

    if not url or "your-project-id" in url:
        print("❌ Error: SUPABASE_URL is not set correctly in .env")
        return
    
    if not key or "your-supabase-api-key" in key:
        print("❌ Error: SUPABASE_KEY is not set correctly in .env")
        return

    print(f"✅ Environment variables found.")
    print(f"   URL: {url}")
    print(f"   Key: {key[:5]}...{key[-5:]}") # Mask key for security

    # 3. Test Connection
    print("\nTesting connection to Supabase...")
    
    try:
        info = test_supabase_connection()
        
        if info.get('using_fake'):
            print("❌ Error: Connection failed. The application is falling back to the local fake DB.")
            if 'error' in info:
                print(f"   Error details: {info['error']}")
            print("   Please check your credentials and internet connection.")
        elif info.get('ok'):
            print("✅ Success! Connected to Supabase Cloud.")
            print("   Database tables are accessible.")
        else:
            print("⚠️  Connected to Supabase, but encountered an issue querying the 'users' table.")
            print(f"   Error details: {info.get('error')}")
            print("   Did you run the SQL script in the Supabase Dashboard to create the tables?")

    except Exception as e:
        print(f"❌ Unexpected error during connection test: {e}")

if __name__ == "__main__":
    main()
