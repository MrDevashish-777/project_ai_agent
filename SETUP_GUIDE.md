# Setup Guide - Nagpur Hotel AI Agent

## Quick Setup (3 Steps)

### Step 1: Move Environment Variables to Root

**Windows (PowerShell):**
```powershell
# Navigate to project
cd c:\Users\OM\Downloads\project_ai_agent

# Create .env file in root
$env_content = @"
SUPABASE_URL=https://dehuipkdltaiumsifyka.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRlaHVpcGtkbHRhaXVtc2lmeWthIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NDMxNzExNCwiZXhwIjoyMDc5ODkzMTE0fQ.gOKJO2Jm_rh7aaAOErLW0v8XbgnR6lWuDUmij2IKO1k
"@

$env_content | Out-File -Encoding UTF8 ".env"
```

### Step 2: Activate Virtual Environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 3: Install & Run

```powershell
# Update dependencies
pip install -r requirements.txt --upgrade

# Start backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

## Verify Supabase Connection

Once backend is running, open a new terminal:

```powershell
# Test connection
curl http://127.0.0.1:8000/supabase_test
```

**Expected Response (Real Supabase):**
```json
{
  "using_fake": false,
  "supabase_url": "https://dehuipkdltaiumsifyka.supabase.co",
  "ok": true,
  "user_sample": []
}
```

## View Saved Data

### All Data Endpoint
```
GET http://127.0.0.1:8000/all_data
```

Returns total counts and all data:
```json
{
  "users": [...],
  "total_users": 2,
  "conversations": [...],
  "total_conversations": 15,
  "bookings": [...],
  "total_bookings": 3
}
```

### User-Specific Data
```
GET http://127.0.0.1:8000/user_data/{user_id}
```

Returns all conversations and bookings for a specific user.

## Database Tables

### conversations table
Stores every message:
- `id`: UUID (auto)
- `user_id`: User identifier
- `role`: "user" or "bot"
- `message`: Full message text
- `meta`: JSON metadata (budget, nights, hotel_id, action, etc.)
- `created_at`: Timestamp (auto)

### bookings table
Stores completed bookings:
- `id`: UUID (auto)
- `user_id`: Foreign key to users
- `hotel_id`: Hotel ID
- `hotel_name`: Hotel name
- `checkin_date`: Check-in date
- `nights`: Number of nights
- `visitors`: Number of guests
- `total_price`: Total booking price
- `created_at`: Timestamp (auto)

### users table
Stores guest information:
- `id`: UUID (auto)
- `name`: Guest name
- `phone`: Phone number (unique)
- `created_at`: Timestamp (auto)

## What Gets Saved (End-to-End)

### Chat Interactions
✅ Initial greeting ("Hi")
✅ Budget entry ("2500")
✅ Nights entry ("3 nights")
✅ Hotel selection ("h1")
✅ Each bot response
✅ All with metadata tracking action type

### Booking Form
✅ Form opening
✅ Form cancellation
✅ All field fills
✅ Final submission
✅ Confirmation

### Complete Records
Each saved with:
- **user_id**: Unique user identifier
- **timestamp**: When action occurred
- **metadata**: action type, extracted data, suggestions shown
- **role**: User or Bot message

## Troubleshooting

### Data Not Appearing?

1. **Check .env file location:**
   ```powershell
   Get-Content .env
   ```
   Should show Supabase credentials

2. **Check backend logs:**
   Look for `✅ Conversation saved:` or `✅ Booking created:` messages

3. **Verify Supabase connection:**
   ```powershell
   curl http://127.0.0.1:8000/supabase_test
   ```

4. **Check Supabase dashboard:**
   - Go to https://app.supabase.com
   - Select your project
   - Check "conversations", "bookings", "users" tables

### Wrong Credentials?

1. Get correct credentials from Supabase:
   - Project Settings > API
   - Copy `Project URL` (SUPABASE_URL)
   - Copy `Service Role` key (SUPABASE_KEY)

2. Update .env file with correct values

3. Restart backend

## Testing the Flow

1. Open `index.html` in browser
2. Click 💬 button
3. Say "Hi"
4. Enter budget: "2500"
5. Enter nights: "3 nights"
6. Select a hotel
7. Fill booking form
8. Click "Confirm Booking"
9. Check data was saved:
   ```powershell
   curl http://127.0.0.1:8000/all_data
   ```

## API Endpoints for Data Retrieval

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/all_data` | GET | View all users, conversations, bookings |
| `/user_data/{user_id}` | GET | View specific user's data |
| `/supabase_test` | GET | Test Supabase connection |
| `/conversations/{user_id}` | GET | Get conversations for user |

## Important Notes

⚠️ **Data Persistence:**
- With .env configured: Data persists in Supabase
- Without .env: Data stored locally (lost on restart)

⚠️ **Credentials:**
- Keep SUPABASE_KEY secret
- Don't commit .env to version control

✅ **Verification:**
- All chat messages logged to console
- All saves show `✅` message
- All errors show `❌` message
- Check browser console for frontend errors
- Check backend terminal for backend errors

## Support

Check these files for configuration:
- `.env` - Credentials
- `db.py` - Database functions
- `main.py` - API endpoints
- `chatbot.py` - Chat logic
- `index.html` - Frontend logic
