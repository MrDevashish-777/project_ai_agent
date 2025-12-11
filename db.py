# db.py
import os
from typing import Optional, Dict, Any
from uuid import uuid4

# Try to import supabase client if available and configured; if not, use an in-memory FakeSupabase
try:
    from supabase import create_client, Client
except Exception:
    create_client = None
    Client = None

# Default to the project URL you provided (can be overridden with SUPABASE_URL env var)
DEFAULT_SUPABASE_URL = "https://dehuipkdltaiumsifyka.supabase.co"
SUPABASE_URL = os.getenv("SUPABASE_URL", DEFAULT_SUPABASE_URL)
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

class FakeResponse:
    def __init__(self, data):
        self.data = data

class FakeTable:
    def __init__(self, storage, name):
        self._storage = storage
        self._name = name
        self._select_cols = None
        self._filters = []
        self._limit = None

    def select(self, *cols):
        self._select_cols = cols
        return self

    def eq(self, col, val):
        self._filters.append((col, val))
        return self

    def limit(self, n):
        self._limit = n
        return self

    def insert(self, payload):
        # Queue insert payload and return self to allow .execute() chaining like the real supabase client
        self._insert_payload = payload if isinstance(payload, dict) else (payload[0] if payload else {})
        return self

    def execute(self):
        # apply filters
        # Check for pending insert
        if hasattr(self, '_insert_payload') and self._insert_payload is not None:
            payload = self._insert_payload
            if "id" not in payload:
                payload = {**payload, "id": str(uuid4())}
            self._storage.setdefault(self._name, []).append(payload)
            self._insert_payload = None
            return FakeResponse([payload])
        table = list(self._storage.get(self._name, []))
        for col, val in self._filters:
            table = [r for r in table if r.get(col) == val]
        if self._limit:
            table = table[: self._limit]
        return FakeResponse(table)

class FakeSupabase:
    def __init__(self):
        self._storage = {"users": [], "bookings": [], "conversations": []}

    def table(self, name):
        return FakeTable(self._storage, name)

USE_FAKE = True
if create_client and SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        # Quick connection test (non-failing call)
        try:
            supabase.table('users').select('*').limit(1).execute()
            print('Supabase client initialized: using remote DB')
            USE_FAKE = False
        except Exception as e:
            print('Warning: Supabase client created but call failed; falling back to local fake DB')
            print('Error when calling supabase:', e)
            supabase = FakeSupabase()
    except Exception as e:
        print('Error initializing supabase client:', e)
        supabase = FakeSupabase()
else:
    print('SUPABASE_KEY not set; using local FakeSupabase storage')
    supabase = FakeSupabase()

def upsert_user(name: str, phone: str) -> Dict[str, Any]:
    # find user by phone or create
    resp = supabase.table("users").select("*").eq("phone", phone).limit(1).execute()
    data = resp.data
    if data:
        return data[0]
    ins = supabase.table("users").insert({"name": name, "phone": phone}).execute()
    return ins.data[0]

def save_conversation(user_id: Optional[str], role: str, message: str, meta: dict = None):
    payload = {"user_id": user_id, "role": role, "message": message, "meta": meta or {}}
    try:
        r = supabase.table("conversations").insert(payload).execute()
        print(f"✅ Conversation saved: {user_id} - {role} - {r.data}")
        return r
    except Exception as e:
        print(f"❌ Error saving conversation: {e}")
        raise

def create_booking(user_id: Optional[str], hotel_id: str, hotel_name: str, checkin_date: str, nights: int, total_price: float, visitors: int = 1):
    payload = {
        "user_id": user_id,
        "hotel_id": hotel_id,
        "hotel_name": hotel_name,
        "checkin_date": checkin_date,
        "nights": nights,
        "total_price": total_price,
        "visitors": visitors
    }
    try:
        r = supabase.table("bookings").insert(payload).execute()
        booking = r.data[0]
        print(f"✅ Booking created: {booking['id']} for user {user_id}")
        return booking
    except Exception as e:
        print(f"❌ Error creating booking: {e}")
        raise

def get_user_bookings(user_id: str) -> Dict[str, Any]:
    try:
        r = supabase.table("bookings").select("*").eq("user_id", user_id).execute()
        print(f"✅ Retrieved {len(r.data)} bookings for user {user_id}")
        return r.data
    except Exception as e:
        print(f"❌ Error retrieving bookings: {e}")
        return []

def get_user_conversations(user_id: str) -> Dict[str, Any]:
    try:
        r = supabase.table("conversations").select("*").eq("user_id", user_id).order("created_at", desc=False).execute()
        print(f"✅ Retrieved {len(r.data)} conversations for user {user_id}")
        return r.data
    except Exception as e:
        print(f"❌ Error retrieving conversations: {e}")
        return []


def test_supabase_connection() -> Dict[str, Any]:
    """Return connection info and whether a real supabase DB is used.
    This can be used by external code or an admin script to auto-validate connection.
    """
    info = {"using_fake": USE_FAKE, "supabase_url": SUPABASE_URL}
    if not USE_FAKE:
        try:
            r = supabase.table('users').select('*').limit(1).execute()
            info['ok'] = True
            info['user_sample'] = r.data
        except Exception as e:
            info['ok'] = False
            info['error'] = str(e)
    return info
