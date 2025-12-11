import os
import sys
import pathlib

SQL_FILE = pathlib.Path(__file__).parent / 'supabase_tables.sql'

# Prefer psycopg (v3) if available, else try psycopg2
try:
    import psycopg
    ps = psycopg
    PSYCOPG_TYPE = 'psycopg'
except Exception:
    try:
        import psycopg2
        ps = psycopg2
        PSYCOPG_TYPE = 'psycopg2'
    except Exception:
        ps = None
        PSYCOPG_TYPE = None


def load_sql():
    if not SQL_FILE.exists():
        print('SQL file not found at', SQL_FILE)
        sys.exit(1)
    return SQL_FILE.read_text()


def run_sql_via_conn(conn_string: str, sql: str):
    if not ps:
        print("No Postgres client installed. Please add 'psycopg[binary]' or 'psycopg2-binary' to requirements and install.")
        sys.exit(1)

    print(f"Using {PSYCOPG_TYPE} to connect to the DB and run SQL...")
    if PSYCOPG_TYPE == 'psycopg':
        # psycopg v3
        with ps.connect(conn_string) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                print('SQL executed successfully.')
    elif PSYCOPG_TYPE == 'psycopg2':
        conn = ps.connect(conn_string)
        try:
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
            print('SQL executed successfully (psycopg2).')
        finally:
            cur.close()
            conn.close()


def main():
    print('Starting Supabase table creation helper...')
    sql = load_sql()

    # Try environment variables for DB URL connection
    db_url = os.getenv('SUPABASE_DB_URL') or os.getenv('DATABASE_URL') or os.getenv('PG_CONNECTION_STRING')

    if db_url:
        print('Found DB URL in environment, proceeding to run SQL.')
        try:
            run_sql_via_conn(db_url, sql)
            print('Done. Tables should now be created. If you use PostgREST or supabase client, make sure the schema is public and RLS policies allow the service key to perform DDL if needed.')
            return
        except Exception as e:
            print('Error while executing SQL against DB URL:', e)
            print('You can also run the SQL manually through the Supabase SQL editor or psql CLI.')
            sys.exit(1)

    # If no DB URL present, but we may have a SUPABASE_URL and a service key
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY') or os.getenv('SUPABASE_KEY')

    if supabase_url and supabase_key:
        print('Found SUPABASE_URL and a service key; attempting to use the Supabase SQL API if available...')
        print('NOTE: The Supabase REST API may not expose raw SQL execution; the typical way is to run the SQL from the Dashboard SQL editor or connect to the DB URL via psql or client. The script will not attempt to run DDL over the REST API.')
        print('\nPlease run the SQL below in the Supabase SQL editor (Project -> SQL Editor -> New Query), or export the DB connection string to SUPABASE_DB_URL and rerun this script.')
        print('\n--- BEGIN SQL ---')
        print(sql)
        print('--- END SQL ---')
        sys.exit(0)

    # Nothing to do; instruct user
    print('No DB URL or SUPABASE service key detected. Please either:')
    print('1) Add SUPABASE_DB_URL to your environment (postgres connection string) and re-run `python supabase_init.py` to run SQL.')
    print('2) Copy the contents of the `supabase_tables.sql` file and run it via the Supabase Project SQL editor in the Dashboard.')
    print('\nAfter creating tables, re-start your FastAPI process and run `python verify_booking.py` to confirm persistence.')


if __name__ == '__main__':
    main()
