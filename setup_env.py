#!/usr/bin/env python3
import os
import sys

def setup_env():
    project_root = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(project_root, '.env')
    old_env_folder = os.path.join(project_root, '.env')
    
    supabase_url = "https://dehuipkdltaiumsifyka.supabase.co"
    supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRlaHVpcGtkbHRhaXVtc2lmeWthIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NDMxNzExNCwiZXhwIjoyMDc5ODkzMTE0fQ.gOKJU2Jm_rh7aaAOErLW0v8XbgnR6lWuDUmij2IKO1k"
    
    env_content = f"""SUPABASE_URL={supabase_url}
SUPABASE_KEY={supabase_key}
"""
    
    try:
        if os.path.isdir(env_path):
            print(f"⚠️  Removing old .env folder...")
            import shutil
            shutil.rmtree(env_path)
        
        with open(env_path, 'w') as f:
            f.write(env_content)
        
        print(f"✅ .env file created at: {env_path}")
        print(f"✅ Supabase URL: {supabase_url}")
        print(f"✅ Supabase Key: {supabase_key[:50]}...")
        print(f"\n🎉 Setup complete! You can now run:")
        print(f"   uvicorn main:app --reload --host 127.0.0.1 --port 8000")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    setup_env()
