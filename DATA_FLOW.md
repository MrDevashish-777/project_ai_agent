# Complete Data Flow - End-to-End Tracking

## What Gets Saved to Supabase

### 📱 Chat Interactions Table: `conversations`

Every single message interaction is saved:

```
User Message: "Hi"
  ↓ SAVED ↓
{
  "id": "uuid-1",
  "user_id": "u123abc456",
  "role": "user",
  "message": "Hi",
  "meta": {},
  "created_at": "2025-12-06T15:30:00Z"
}

Bot Message: "Hello! Welcome..."
  ↓ SAVED ↓
{
  "id": "uuid-2",
  "user_id": "u123abc456",
  "role": "bot",
  "message": "Hello! Welcome to Nagpur hotel helper...",
  "meta": {},
  "created_at": "2025-12-06T15:30:02Z"
}
```

### 💰 Budget Entry

```
User: "2500"
  ↓ PARSED & SAVED ↓
{
  "id": "uuid-3",
  "user_id": "u123abc456",
  "role": "user",
  "message": "2500",
  "meta": {
    "budget": 2500
  },
  "created_at": "2025-12-06T15:30:10Z"
}

Bot: "Great! ₹2500/night budget noted..."
  ↓ SAVED WITH ACTION ↓
{
  "id": "uuid-4",
  "user_id": "u123abc456",
  "role": "bot",
  "message": "Great! ₹2500/night budget noted...",
  "meta": {
    "action": "budget_confirmed",
    "budget": 2500
  },
  "created_at": "2025-12-06T15:30:12Z"
}
```

### 🏨 Nights/Duration Entry

```
User: "3 nights"
  ↓ PARSED & SAVED ↓
{
  "id": "uuid-5",
  "user_id": "u123abc456",
  "role": "user",
  "message": "3 nights",
  "meta": {
    "nights": 3
  },
  "created_at": "2025-12-06T15:30:20Z"
}

Bot: "Found 8 hotels within your budget for 3 nights!"
  ↓ SAVED WITH SUGGESTIONS ↓
{
  "id": "uuid-6",
  "user_id": "u123abc456",
  "role": "bot",
  "message": "Found 8 hotels within your budget...",
  "meta": {
    "action": "hotels_filtered",
    "budget": 2500,
    "nights": 3,
    "suggestions": [
      {
        "id": "h1",
        "name": "Hotel A",
        "price_per_night": 2500,
        "rating": 4.5,
        "area": "Downtown"
      },
      ...
    ]
  },
  "created_at": "2025-12-06T15:30:22Z"
}
```

### 🏠 Hotel Selection

```
User: "h1" (clicks Select button)
  ↓ SAVED ↓
{
  "id": "uuid-7",
  "user_id": "u123abc456",
  "role": "user",
  "message": "h1",
  "meta": {
    "selected_hotel_id": "h1",
    "action": "hotel_selected"
  },
  "created_at": "2025-12-06T15:30:30Z"
}

Bot: "You chose Hotel A. Price ₹2500/night, rating 4.5..."
  ↓ SAVED ↓
{
  "id": "uuid-8",
  "user_id": "u123abc456",
  "role": "bot",
  "message": "You chose Hotel A...",
  "meta": {
    "action": "hotel_details_shown",
    "selected_hotel": {
      "id": "h1",
      "name": "Hotel A",
      "price_per_night": 2500
    }
  },
  "created_at": "2025-12-06T15:30:32Z"
}
```

### 📋 Booking Form Interaction

```
Opening Booking Form
  ↓ SAVED ↓
{
  "id": "uuid-9",
  "user_id": "u123abc456",
  "role": "bot",
  "message": "📋 Opening booking form for Hotel A...",
  "meta": {
    "action": "booking_form_opened",
    "hotel_id": "h1"
  },
  "created_at": "2025-12-06T15:30:35Z"
}

Form Fields Filled:
- Name: "John Doe"
- Phone: "+919876543210"
- Date: "2025-12-20"
- Nights: "3"
- Visitors: "2"
  ↓ SUBMITTED & SAVED ↓
{
  "id": "uuid-10",
  "user_id": "u123abc456",
  "role": "user",
  "message": "Book Hotel A as John Doe from 2025-12-20 nights 3 visitors 2",
  "meta": {
    "action": "booking_submitted",
    "name": "John Doe",
    "phone": "+919876543210",
    "checkin_date": "2025-12-20",
    "nights": 3,
    "visitors": 2,
    "hotel_id": "h1"
  },
  "created_at": "2025-12-06T15:30:45Z"
}
```

### ✅ Booking Confirmation

```
Booking Record Created in `bookings` table:
  ↓ SAVED ↓
{
  "id": "booking-uuid-12345",
  "user_id": "u123abc456",
  "hotel_id": "h1",
  "hotel_name": "Hotel A",
  "checkin_date": "2025-12-20",
  "nights": 3,
  "visitors": 2,
  "total_price": 8850.00,  # 2500*3 + 18% GST
  "created_at": "2025-12-06T15:30:47Z"
}

Confirmation Message Saved:
{
  "id": "uuid-11",
  "user_id": "u123abc456",
  "role": "bot",
  "message": "Booking confirmed!\n\n[Bill Details]",
  "meta": {
    "action": "booking_confirmed",
    "booking_id": "booking-uuid-12345",
    "booking": {
      "id": "booking-uuid-12345",
      "hotel_name": "Hotel A",
      "total_price": 8850.00
    }
  },
  "created_at": "2025-12-06T15:30:49Z"
}
```

## Complete Data Structure

### Users Table (`users`)
```sql
{
  "id": "uuid",
  "name": "John Doe",
  "phone": "+919876543210",  -- UNIQUE
  "created_at": "2025-12-06T15:30:00Z"
}
```

### Conversations Table (`conversations`)
```sql
{
  "id": "uuid",
  "user_id": "uuid (FK to users)",
  "role": "user|bot",
  "message": "Full message text",
  "meta": {
    -- Dynamic fields based on interaction type:
    "action": "greeting|budget_confirmed|hotel_selected|booking_submitted|booking_confirmed",
    "budget": 2500,
    "nights": 3,
    "hotel_id": "h1",
    "suggestions": [...],
    "booking_id": "uuid",
    ...
  },
  "created_at": "timestamp"
}
```

### Bookings Table (`bookings`)
```sql
{
  "id": "uuid",
  "user_id": "uuid (FK to users)",
  "hotel_id": "h1",
  "hotel_name": "Hotel Name",
  "checkin_date": "2025-12-20",
  "nights": 3,
  "visitors": 2,
  "total_price": 8850.00,
  "created_at": "2025-12-06T15:30:47Z"
}
```

## API Endpoints for Data Retrieval

### 1. View All Data
```
GET /all_data

Response:
{
  "users": [...all users...],
  "total_users": 5,
  "conversations": [...all conversations...],
  "total_conversations": 127,
  "bookings": [...all bookings...],
  "total_bookings": 18
}
```

### 2. Get Specific User's Data
```
GET /user_data/{user_id}

Example: GET /user_data/u123abc456

Response:
{
  "user_id": "u123abc456",
  "conversations_count": 15,
  "bookings_count": 2,
  "conversations": [
    {
      "id": "uuid-1",
      "role": "user",
      "message": "Hi",
      "meta": {},
      "created_at": "..."
    },
    ...
  ],
  "bookings": [
    {
      "id": "booking-uuid-1",
      "hotel_name": "Hotel A",
      "nights": 3,
      "total_price": 8850.00,
      ...
    }
  ]
}
```

### 3. Get User Conversations
```
GET /conversations/{user_id}

Returns all chat messages in chronological order with metadata
```

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interactions                        │
└─────────────────────────────────────────────────────────────┘
                          ↓
                    ┌─────────────┐
                    │   Browser   │
                    └─────────────┘
                          ↓
                ┌─────────────────────────┐
                │  Frontend (index.html)  │
                │  - Validates input      │
                │  - Shows UI             │
                └─────────────────────────┘
                          ↓
                   ┌──────────────┐
                   │  FastAPI     │
                   │  Backend     │
                   └──────────────┘
                       ↙  ↓  ↖
            ┌──────────┐ │ ┌──────────┐
            │ Chatbot  │─┼─│Database  │
            │ Logic    │ │ │Functions │
            └──────────┘ │ └──────────┘
                         ↓
               ┌─────────────────────┐
               │     Supabase        │
               │   (PostgreSQL)      │
               ├─────────────────────┤
               │  users table        │
               │  bookings table     │
               │  conversations tbl  │
               └─────────────────────┘
                         ↓
              ✅ Data Persists!
```

## Metadata Actions Tracked

| Action | When | Data Saved |
|--------|------|-----------|
| `greeting` | User says "Hi" | Initial state |
| `budget_confirmed` | User enters budget | Budget amount |
| `nights_confirmed` | User enters nights | Night count |
| `hotels_filtered` | Hotels shown | Budget, nights, suggestions |
| `hotel_selected` | User clicks Select | Selected hotel ID |
| `hotel_details_shown` | Bot shows hotel details | Hotel information |
| `booking_form_opened` | Form modal opens | Hotel being booked |
| `booking_submitted` | Form submitted | All form data |
| `booking_confirmed` | Booking successful | Booking record + ID |

## Verification Commands

### Check total data:
```powershell
curl http://127.0.0.1:8000/all_data | findstr /C:"total"
```

### Check specific user:
```powershell
curl http://127.0.0.1:8000/user_data/u123abc456
```

### Check Supabase connection:
```powershell
curl http://127.0.0.1:8000/supabase_test
```

## Troubleshooting Data Not Saving

✅ Check 1: Is .env in project root with correct credentials?
✅ Check 2: Is backend showing "✅ Conversation saved" messages?
✅ Check 3: Is /supabase_test showing "using_fake": false?
✅ Check 4: Check Supabase dashboard - are tables created?
✅ Check 5: Check browser console for network errors
✅ Check 6: Check backend terminal for error messages

If all above are OK but data still not saving:
- Check Supabase Row Level Security (RLS) policies
- Ensure service role key has permissions
- Check network connectivity to Supabase
