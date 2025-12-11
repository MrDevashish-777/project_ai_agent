# ✅ Complete Setup Guide - Supabase Data Persistence

This guide ensures ALL data (conversations, form details, bookings) is saved to Supabase end-to-end.

## Current Status

✅ **Backend Code**: Ready to save all data
✅ **Frontend Code**: Ready to send all data
❌ **Configuration**: .env file needs to be in correct location

## The Main Issue

Your `.env` file is in the WRONG location:

```
❌ WRONG: c:\Users\OM\Downloads\project_ai_agent\.env\ini
✅ CORRECT: c:\Users\OM\Downloads\project_ai_agent\.env
```

The file needs to be created in the **ROOT** of your project, not in a subfolder.

## 3-Step Fix

### STEP 1: Create .env File in Project Root

**Windows File Explorer Method:**

1. Navigate to: `c:\Users\OM\Downloads\project_ai_agent\`
2. Right-click → New → Text Document
3. Name it: `.env` (important: starts with a dot!)
4. Open it with Notepad
5. Copy and paste these exact lines:

```
SUPABASE_URL=https://dehuipkdltaiumsifyka.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRlaHVpcGtkbHRhaXVtc2lmeWthIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NDMxNzExNCwiZXhwIjoyMDc5ODkzMTE0fQ.gOKJU2Jm_rh7aaAOErLW0v8XbgnR6lWuDUmij2IKO1k
```

6. Save (Ctrl+S)
7. Rename file to `.env` (remove `.txt` extension)

**PowerShell Method:**

```powershell
cd c:\Users\OM\Downloads\project_ai_agent
@"
SUPABASE_URL=https://dehuipkdltaiumsifyka.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRlaHVpcGtkbHRhaXVtc2lmeWthIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NDMxNzExNCwiZXhwIjoyMDc5ODkzMTE0fQ.gOKJU2Jm_rh7aaAOErLW0v8XbgnR6lWuDUmij2IKO1k
"@ | Out-File -Encoding UTF8 ".env"
```

### STEP 2: Verify File Creation

```powershell
cd c:\Users\OM\Downloads\project_ai_agent
Get-Item ".env"
Get-Content ".env"
```

You should see the Supabase credentials displayed.

### STEP 3: Start Backend with New Configuration

```powershell
cd c:\Users\OM\Downloads\project_ai_agent
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt --upgrade
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Watch the terminal for this message:

```
✅ Supabase client initialized: using remote DB
```

If you see this, Supabase is connected! ✅

## Verify Supabase Connection

**In a NEW PowerShell terminal:**

```powershell
curl http://127.0.0.1:8000/supabase_test
```

Look for this in the response:

```json
{
  "using_fake": false,  ← This must be FALSE
  "ok": true,
  "user_sample": [],
  "supabase_url": "https://dehuipkdltaiumsifyka.supabase.co"
}
```

- If `"using_fake": false` → ✅ Connected to real Supabase!
- If `"using_fake": true` → ❌ Still using local storage (check .env file)

## Test Complete Flow

1. **Open index.html in browser** (click 💬 icon)

2. **Chat with bot:**
   - Send: "Hi"
   - Send: "2500"
   - Send: "3 nights"
   - Select a hotel

3. **Fill booking form:**
   - Name: John Doe
   - Phone: +919876543210
   - Date: 2025-12-20
   - Nights: 3
   - Visitors: 2

4. **Click Confirm Booking**

5. **Check backend terminal** for messages like:
   ```
   ✅ Conversation saved: u123abc456 - user - [...]
   ✅ Booking created: 12345-uuid-here for user u123abc456
   ```

6. **View saved data:**
   ```powershell
   curl http://127.0.0.1:8000/all_data
   ```

   Should show:
   ```json
   {
     "total_users": 1,
     "total_conversations": 10,
     "total_bookings": 1
   }
   ```

## Complete Data Saved

After booking, these records exist in Supabase:

### Users Table (1 record)
```
John Doe | +919876543210 | 2025-12-06T...
```

### Conversations Table (10+ records)
1. "Hi" (user message)
2. "Hello! Welcome..." (bot response)
3. "2500" (user message)
4. "Great! ₹2500/night noted..." (bot response)
5. "3 nights" (user message)
6. "Found 8 hotels..." (bot response with suggestions)
7. "h1" (user selects hotel)
8. "You chose Hotel..." (bot details)
9. "Book Hotel..." (user booking form details)
10. "Booking confirmed!..." (bot confirmation)

### Bookings Table (1 record)
```
{
  "hotel_name": "Hotel Paradise",
  "checkin_date": "2025-12-20",
  "nights": 3,
  "visitors": 2,
  "total_price": 8850.00
}
```

## API Endpoints for Verification

### Get All Data
```
GET http://127.0.0.1:8000/all_data
```

Returns counts and all records.

### Get Specific User Data
```
GET http://127.0.0.1:8000/user_data/u123abc456
```

Returns all conversations and bookings for that user.

### Get User Conversations
```
GET http://127.0.0.1:8000/conversations/u123abc456
```

Returns chat history in order.

## Check Supabase Dashboard

1. Go to https://app.supabase.com
2. Log in
3. Select project: `dehuipkdltaiumsifyka`
4. Go to **SQL Editor** or **Table Editor**
5. Check tables:
   - `users` → See all users
   - `conversations` → See all chat messages
   - `bookings` → See all bookings

## Troubleshooting

### Problem: "using_fake": true (Still using local storage)

**Solution:**
1. Check .env file exists in project ROOT:
   ```powershell
   ls -la .env
   ```

2. Check credentials are correct:
   ```powershell
   cat .env
   ```

3. Restart backend:
   ```powershell
   # Stop uvicorn (Ctrl+C)
   # Restart:
   uvicorn main:app --reload --host 127.0.0.1 --port 8000
   ```

### Problem: Data not appearing in Supabase

**Solution:**
1. Check backend console for error messages
2. Look for `❌ Error` messages
3. Verify Supabase tables exist:
   ```powershell
   python supabase_init.py
   ```

4. Check Row Level Security (RLS) in Supabase:
   - Go to SQL Editor
   - Check if RLS policies allow inserts

### Problem: Backend won't start

**Solution:**
1. Ensure Python 3.9+ is installed
2. Reinstall dependencies:
   ```powershell
   pip install -r requirements.txt --force-reinstall
   ```

3. Check for syntax errors:
   ```powershell
   python -m py_compile main.py chatbot.py db.py
   ```

## What Gets Saved - Complete List

✅ **Conversations Table:**
- Every user message
- Every bot response
- Budget information
- Nights information
- Hotel suggestions
- Hotel selection
- Booking form submission
- Booking confirmation
- Each with action metadata

✅ **Bookings Table:**
- Hotel ID and name
- Check-in date
- Number of nights
- Number of visitors
- Total price (with GST)
- Guest information
- Booking timestamp

✅ **Users Table:**
- Guest name
- Phone number
- Registration timestamp

## Next Steps

1. **Create .env file** (Step 1 above)
2. **Restart backend**
3. **Test the flow**
4. **Verify data in Supabase**
5. **Check /all_data endpoint**

## Support Files

- `README.md` - Full documentation
- `SETUP_GUIDE.md` - Detailed setup steps
- `DATA_FLOW.md` - Complete data flow explanation
- `SETUP_SUPABASE.txt` - Quick .env setup reference

---

**Once .env file is created in project root, all your data will automatically be saved to Supabase!** ✅
