"""create_and_verify.py
Convenience script: run the supabase_init script to create tables (via DB URL or print SQL) and then verify by querying the created tables.
"""
import os
import runpy
import subprocess
import sys

# Run the initializer (it will either execute the SQL if SUPABASE_DB_URL is present or print SQL for manual execution)
print('Running supabase_init.py (this will execute SQL if SUPABASE_DB_URL is set)')
try:
    runpy.run_path('supabase_init.py', run_name='__main__')
except Exception as e:
    print('Error running supabase_init.py:', e)
    sys.exit(1)

# If SUPABASE_DB_URL is set, run verify_supabase_tables.py to confirm they exist
if os.getenv('SUPABASE_DB_URL') or os.getenv('DATABASE_URL'):
    print('Verifying tables via DB URL using verify_supabase_tables.py...')
    try:
        runpy.run_path('verify_supabase_tables.py', run_name='__main__')
    except Exception as e:
        print('Error running verify script:', e)
        sys.exit(1)
else:
    # If DB URL missing but we have supabase service key + url, we will run PostgREST check
    if os.getenv('SUPABASE_URL') and (os.getenv('SUPABASE_KEY') or os.getenv('SUPABASE_SERVICE_ROLE_KEY')):
        print('No DB URL provided; verify via PostgREST by running verify_supabase_tables.py which will fallback to HTTP checks. Running now...')
        try:
            runpy.run_path('verify_supabase_tables.py', run_name='__main__')
        except Exception as e:
            print('Error running verify script via HTTP:', e)
            sys.exit(1)
    else:
        print('You may now run `verify_supabase_tables.py` after you have executed the SQL in the Dashboard.')

print('Done')
