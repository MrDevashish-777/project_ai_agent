# Nagpur Hotel AI Booking Agent 🤖🏨

An intelligent AI-powered hotel booking chatbot that helps customers find and book hotels in Nagpur through natural conversation. This application uses **FastAPI** backend with **Google Gemini AI** for intelligent recommendations, **Supabase PostgreSQL** for data persistence, and a modern responsive HTML5/CSS3/JavaScript web interface.

<div align="center">

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688.svg)](https://fastapi.tiangolo.com/)
[![Gemini API](https://img.shields.io/badge/Google_Gemini-API-4285F4.svg)](https://ai.google.dev/)
[![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-3ECF8E.svg)](https://supabase.com/)

</div>

## ✨ Key Features

- **🤖 AI-Powered Conversations** - Google Gemini 2.5 Flash integration for intelligent, context-aware hotel recommendations
- **🏨 Smart Hotel Search** - Filter by budget, location, amenities, ratings, and dates
- **💰 Budget-Conscious** - Affordable hotel options in Nagpur starting from ₹1000-15000 with transparent pricing
- **📋 Instant Billing** - Automatic invoice generation with GST (18%) calculation
- **💾 Persistent Storage** - Supabase PostgreSQL database for bookings, conversations, users, and audit logs
- **🎯 Personalization** - Learn user preferences for tailored recommendations
- **📱 Responsive Design** - Mobile-friendly HTML5/CSS3 interface with vanilla JavaScript
- **⚡ RESTful API** - Well-documented async endpoints with request/response models
- **🔐 Data Validation** - Input validation and PII masking for security
- **📊 Audit Logging** - Complete audit trail for all transactions and interactions
- **⏱️ Rate Limiting** - 100 requests per minute per IP with middleware protection
- **👨‍💼 Admin Panel** - Secure admin login with token-based authentication

## 🏗️ Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| **Backend** | FastAPI | 0.115.0 |
| **ASGI Server** | Uvicorn | 0.30.0 |
| **AI/ML** | Google Generative AI (Gemini) | 0.7.2 |
| **Database** | Supabase (PostgreSQL) | 2.4.2 |
| **Frontend** | HTML5, CSS3, Vanilla JS | - |
| **Validation** | Pydantic | 2.8.0 |
| **HTTP Client** | httpx | 0.27.0 |

## 📋 System Requirements

- **Python** 3.9 or higher (tested on 3.13)
- **Virtual Environment** (venv or conda recommended)
- **Supabase Account** (free tier available at [supabase.com](https://supabase.com))
- **Google Gemini API Key** (get from [ai.google.dev](https://ai.google.dev/))
- **Git** (for version control)

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/nagpur-hotel-ai-agent.git
cd nagpur-hotel-ai-agent
```

### 2. Create Virtual Environment

**On Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**On macOS/Linux (Bash/Zsh):**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt --upgrade
```

### 4. Set Up Environment Variables

Create a `.env` file in the **project root directory** (not in a subdirectory):

```env
# Supabase Configuration
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-supabase-api-key

# Google Gemini API
GEMINIE_KEY=your-gemini-api-key
```

**Getting Credentials:**

**Supabase:**
1. Create free account at [supabase.com](https://supabase.com)
2. Create new project
3. Go to Settings → API
4. Copy Project URL and anon key

**Gemini API:**
1. Visit [ai.google.dev](https://ai.google.dev)
2. Click "Get API Key"
3. Create new API key in Google Cloud Console
4. Copy to GEMINIE_KEY

### 5. Initialize Database (First Time Only)

```bash
python supabase_init.py
```

This creates all required tables in your Supabase database:
- **conversations** - Chat history for each user
- **bookings** - Booking records with dates and prices
- **users** - User profiles with contact info
- **audit_logs** - Transaction logs for compliance

### 6. Run the Application

**Start the backend server:**
```bash
python main.py
```

**Or with explicit Uvicorn command (with auto-reload):**
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

**Access the application:**
- **Frontend**: Open `index.html` in your web browser (local file)
- **API Base URL**: http://localhost:8000
- **Interactive API Docs**: http://localhost:8000/docs (Swagger UI)
- **ReDoc Documentation**: http://localhost:8000/redoc

## 🎯 How It Works

```
User Message
    ↓
┌─ Check for hotel keywords (budget, dates, location) ─┐
│                                                        │
├─ MATCH: Use rule-based hotel logic                   ├─ JSON Response
│  (search, filter, book)                              │
│                                                        │
└─ NO MATCH: Call Gemini API                           ┘
   (general questions, recommendations)
```

### Hybrid Intelligence

- **Rule-Based**: Fast, structured responses for booking workflows
- **AI-Powered**: Gemini API for conversational, intelligent recommendations
- **Seamless Integration**: Automatic switching based on user intent

## 📚 API Endpoints

### **POST /chat** - Send Chat Message to Bot

Sends a user message to the bot which processes it using hybrid intelligence (rule-based for hotels, AI for general questions).

**Request:**
```http
POST /chat
Content-Type: application/json

{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Show me hotels under ₹5000 near Sitabuldi",
  "conversation_id": "optional-conversation-id"
}
```

**Response:**
```json
{
  "reply": "I found 4 hotels within your budget in the Sitabuldi area...",
  "suggestions": [
    {"text": "Book this hotel", "action": "book"},
    {"text": "See more options", "action": "search"}
  ],
  "meta": {
    "budget": 5000,
    "location": "Sitabuldi",
    "hotels_count": 4,
    "intent": "hotel_search"
  }
}
```

**Features:**
- Auto-generates UUID if `user_id` is missing
- Validates UUID format
- Saves conversation to database
- Returns AI suggestions for next actions

---

### **POST /internal/search_hotels** - Advanced Hotel Search

Internal endpoint for searching hotels with multiple filter criteria.

**Request:**
```http
POST /internal/search_hotels
Content-Type: application/json

{
  "max_price": 5000,
  "location": "Sitabuldi",
  "min_rating": 4.0,
  "amenities": ["WiFi", "AC", "Restaurant"],
  "limit": 10
}
```

**Response:**
```json
{
  "count": 4,
  "hotels": [
    {
      "id": "hotel_001",
      "name": "Grand Plaza",
      "area": "Sitabuldi",
      "price_per_night": 4500,
      "rating": 4.8,
      "amenities": ["WiFi", "AC", "Restaurant", "24/7 Service"]
    }
  ]
}
```

---

### **POST /internal/confirm_booking** - Get Booking Confirmation Summary

Generates a booking confirmation preview without creating the actual booking (used for verification before payment).

**Request:**
```http
POST /internal/confirm_booking
Content-Type: application/json

{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "John Doe",
  "phone": "9876543210",
  "hotel_id": "hotel_001",
  "checkin_date": "2025-12-20",
  "nights": 3,
  "visitors": 2
}
```

**Response:**
```json
{
  "status": "confirmation_pending",
  "summary": "Booking confirmation for 3 nights...",
  "booking_details": {
    "hotel_name": "Grand Plaza",
    "price_per_night": 4500,
    "nights": 3,
    "subtotal": 13500,
    "gst": 2430,
    "total": 15930
  }
}
```

---

### **POST /internal/book_hotel** - Create Hotel Booking

Creates an actual booking in the database (call `/internal/confirm_booking` first for validation).

**Request:**
```http
POST /internal/book_hotel
Content-Type: application/json

{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "John Doe",
  "phone": "9876543210",
  "hotel_id": "hotel_001",
  "checkin_date": "2025-12-20",
  "nights": 3,
  "visitors": 2
}
```

**Response:**
```json
{
  "status": "success",
  "booking_id": "bk_a1b2c3d4e5f6",
  "total_price": 13500,
  "hotel": {
    "id": "hotel_001",
    "name": "Grand Plaza",
    "price_per_night": 4500,
    "area": "Sitabuldi"
  }
}
```

**Database Updates:**
- Creates user (upsert if exists)
- Creates booking record
- Logs to audit_logs table

---

### **POST /internal/payment_intent** - Create Payment Intent

Generates a payment intent for checkout (gateway integration ready).

**Request:**
```http
POST /internal/payment_intent
Content-Type: application/json

{
  "amount_inr": 15930,
  "currency": "INR",
  "description": "Hotel booking for Grand Plaza",
  "booking_id": "bk_a1b2c3d4e5f6"
}
```

**Response:**
```json
{
  "payment_id": "pi_a1b2c3d4e5f6",
  "amount_inr": 15930,
  "currency": "INR",
  "payment_url": "https://payment.example.com/pi_a1b2c3d4e5f6",
  "client_secret": "sk_a1b2c3d4e5f6g7h8i9j0",
  "status": "pending"
}
```

---

### **POST /internal/generate_invoice** - Generate Invoice

Generates an HTML invoice with GST calculation.

**Request:**
```http
POST /internal/generate_invoice
Content-Type: application/json

{
  "booking_id": "bk_a1b2c3d4e5f6",
  "gst_percent": 18
}
```

**Response:**
```json
{
  "invoice_id": "inv_a1b2c3d4",
  "booking_id": "bk_a1b2c3d4e5f6",
  "subtotal": 13500,
  "gst": 2430,
  "total": 15930,
  "invoice_html": "<html><body>...</body></html>"
}
```

---

### **POST /admin/login** - Admin Authentication

Authenticates admin user and returns a 2-hour token.

**Request:**
```http
POST /admin/login
Content-Type: application/json

{
  "username": "admin",
  "password": "your-secure-password"
}
```

**Response:**
```json
{
  "status": "success",
  "token": "adm_a1b2c3d4e5f6g7h8i9j0",
  "expires_in": 7200
}
```

---

### **GET /admin/chats** - Fetch All Conversations (Admin Only)

Retrieves all chat conversations from database (requires valid admin token).

**Request:**
```http
GET /admin/chats?limit=50
Authorization: Bearer adm_a1b2c3d4e5f6g7h8i9j0
```

**Response:**
```json
{
  "conversations": [
    {
      "id": "conv_123",
      "user_id": "user_123",
      "role": "user",
      "message": "Show me hotels",
      "message_preview": "Show me hotels",
      "created_at": "2025-12-11T10:30:00Z",
      "meta": {}
    }
  ],
  "count": 1
}
```

---

### **POST /book** - Legacy Booking Endpoint

Backward-compatible booking endpoint (calls `/internal/book_hotel` internally).

**Request:**
```http
POST /book
Content-Type: application/json

{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "John Doe",
  "phone": "9876543210",
  "hotel_id": "hotel_001",
  "checkin_date": "2025-12-20",
  "nights": 3,
  "visitors": 2
}
```

**Response:**
```json
{
  "status": "success",
  "booking_id": "bk_a1b2c3d4e5f6",
  "bill": "Invoice details...",
  "total_price": 13500,
  "hotel": {...}
}
```

---

### **GET /hotels** - List All Hotels (Optional Filter)

Returns all hotels or filtered by max price.

**Request:**
```http
GET /hotels?max_price=5000
```

**Response:**
```json
{
  "count": 4,
  "hotels": [
    {
      "id": "hotel_001",
      "name": "Grand Plaza",
      "area": "Sitabuldi",
      "price_per_night": 4500,
      "rating": 4.8,
      "amenities": ["WiFi", "AC", "Restaurant"]
    }
  ]
}
```

---

### **GET /supabase_test** - Test Database Connection

Tests if Supabase connection is working.

**Request:**
```http
GET /supabase_test
```

**Response:**
```json
{
  "ok": true,
  "database": "PostgreSQL",
  "tables_count": 4,
  "message": "Connection successful"
}
```

---

### **Interactive Documentation**

Visit these URLs for full API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## ⚙️ Core Functions Documentation (main.py)

This section explains all the important functions in `main.py` and their working mechanisms.

### **1. StructuredLogger Class** (main.py:27-63)

**Purpose**: Enhanced logging system with structured JSON support for audit trails.

**Methods**:
- **`__init__(name)`** - Initializes the logger with a name
- **`setup_logging()`** - Configures logging format and handlers
- **`log_action(action, user_id, resource_type, resource_id, status, details)`** - Logs structured JSON with timestamp, action, and user context. Returns log_entry dict.
- **`info(msg)`**, **`warning(msg)`**, **`error(msg, exc_info)`** - Standard logging methods

**Example Usage**:
```python
logger.log_action(
    action="BOOKING_CREATED",
    user_id="user123",
    resource_type="booking",
    resource_id="bk_123",
    status="success",
    details={"hotel": "Grand Plaza", "nights": 3}
)
```

---

### **2. RateLimitMiddleware Class** (main.py:89-115)

**Purpose**: Implements rate limiting (100 requests per minute per IP) to prevent abuse.

**How It Works**:
1. Extracts client IP from request
2. Maintains list of request timestamps for each IP
3. Removes requests older than 60 seconds
4. Returns 429 (Too Many Requests) if limit exceeded
5. Otherwise, appends current timestamp and continues request

**Parameters**:
- `requests_per_minute` - Default 100 requests per IP per minute

---

### **3. chat() Endpoint** (main.py:121-159)

**Purpose**: Main chat endpoint that processes user messages and returns AI responses.

**Input**: `ChatRequest` object with `user_id`, `message`, and `conversation_id`

**Processing Steps**:
1. Validates/generates UUID for `user_id`
2. Saves user message to database via `db.save_conversation()`
3. Calls `bot_reply()` from chatbot.py to get response
4. Saves bot reply to database
5. Logs action to audit trail
6. Returns `ChatResponse` with reply, suggestions, and metadata

**Error Handling**: Returns 500 on exception with detailed error logging

**Example**:
```python
request = {"user_id": None, "message": "Show hotels under 5000"}
response = await chat(request)
```

---

### **4. search_hotels() Endpoint** (main.py:161-190)

**Purpose**: Internal API for searching hotels with filters.

**Input**: `InternalSearchHotelsRequest` with:
- `max_price` - Maximum price per night
- `location` - Hotel area/location
- `min_rating` - Minimum star rating
- `amenities` - List of required amenities
- `limit` - Number of results (default 5)

**Processing**:
1. Calls `search_hotels_internal()` from chatbot.py
2. Filters hotels based on criteria
3. Logs search action
4. Returns count and filtered hotel list

**Response**: JSON with hotel count and hotel details

---

### **5. confirm_booking() Endpoint** (main.py:192-233)

**Purpose**: Generates booking confirmation summary WITHOUT creating the booking (for preview before payment).

**Input**: `InternalBookHotelRequest` with user, hotel, and stay details

**Processing Steps**:
1. Validates booking input (name, phone, dates, guests)
2. Retrieves hotel details
3. Calculates total: `price_per_night × nights`
4. Calculates GST: `total × 0.18`
5. Calls `prepare_booking_confirmation()` from chatbot.py
6. Returns confirmation with pricing breakdown

**Important**: Does NOT create booking in database (only confirmation preview)

**Response**:
```json
{
  "status": "confirmation_pending",
  "summary": "...",
  "booking_details": {
    "hotel_name": "...",
    "subtotal": 13500,
    "gst": 2430,
    "total": 15930
  }
}
```

---

### **6. book_hotel_internal() Endpoint** (main.py:235-315)

**Purpose**: Creates an actual hotel booking in the database.

**Input**: `InternalBookHotelRequest` with user and booking details

**Processing Steps**:
1. Validates all input fields
2. Retrieves hotel by ID from `hotels_data.HOTELS`
3. Creates/updates user in database via `db.upsert_user()`
4. Calculates total price: `price_per_night × nights`
5. Creates booking via `db.create_booking()`
6. Creates audit log entry via `create_audit_log()`
7. Logs successful booking action

**Database Operations**:
- Inserts/updates `users` table
- Inserts `bookings` table
- Inserts `audit_logs` table

**Response**: Returns booking_id, total_price, and hotel details

---

### **7. create_payment_intent() Endpoint** (main.py:317-354)

**Purpose**: Generates payment intent for payment gateway integration.

**Input**: `CreatePaymentIntentRequest` with:
- `amount_inr` - Amount in Indian Rupees (must be > 0)
- `currency` - Currency code (default "INR")
- `booking_id` - Associated booking ID

**Processing**:
1. Validates amount > 0
2. Generates unique `payment_id` with format `pi_` + 12 hex chars
3. Generates `client_secret` for payment gateway
4. Creates audit log
5. Returns payment intent details

**Response**: Payment ID, URL, secret, and status "pending"

---

### **8. generate_invoice_internal() Endpoint** (main.py:356-418)

**Purpose**: Generates HTML invoice with GST calculation.

**Input**: `GenerateInvoiceRequest` with:
- `booking_id` - Booking to generate invoice for
- `gst_percent` - GST rate (default 18%)

**Processing Steps**:
1. Retrieves booking from `bookings` table
2. Retrieves hotel details
3. Calculates:
   - `subtotal = booking.total_price`
   - `gst = subtotal × (gst_percent / 100)`
   - `total = subtotal + gst`
4. Generates HTML invoice string
5. Creates audit log
6. Returns invoice ID and HTML

**Response**: Invoice ID, booking ID, amounts, and HTML content

---

### **9. admin_login() Endpoint** (main.py:420-478)

**Purpose**: Authenticates admin user and generates 2-hour token.

**Input**: `AdminLoginRequest` with `username` and `password`

**Authentication Flow**:
1. Compares with environment variables `ADMIN_USERNAME` and `ADMIN_PASSWORD`
2. On failure: logs failed attempt, creates audit log, raises 401 error
3. On success:
   - Generates token: `adm_` + 20 hex chars
   - Stores token in `ADMIN_TOKENS` dict with expiry (current_time + 2 hours)
   - Logs successful login
   - Creates audit log

**Token Format**: `adm_a1b2c3d4e5f6g7h8i9j0k1l2m3`

**Response**: Token and expiry time (7200 seconds = 2 hours)

---

### **10. fetch_chats() Endpoint** (main.py:480-567)

**Purpose**: Retrieves all chat conversations (admin only, requires valid token).

**Input**: 
- `limit` - Number of conversations to fetch (default 50)
- `authorization` - Header with format `Bearer {token}`

**Authorization Flow**:
1. Extracts token from `Authorization: Bearer {token}` header
2. Validates token exists in `ADMIN_TOKENS` dict
3. Checks token not expired
4. If invalid/expired: removes token and raises 401

**Data Processing**:
1. Queries `conversations` table with limit
2. Orders by created_at descending
3. Filters sensitive data (creates "safe_conversations")
4. Includes message_preview (first 100 chars)
5. Logs admin access

**Response**: Array of conversations with user_id, message, timestamp, metadata

---

### **11. book() Endpoint** (main.py:569-625)

**Purpose**: Legacy booking endpoint (backward compatibility with old frontend).

**Working**: 
- Wrapper around `book_hotel_internal()`
- Validates input
- Creates booking in database
- Generates bill via `generate_bill()` from chatbot.py
- Returns booking confirmation with bill text

**Response**: Includes booking_id, bill_text, total_price, and hotel details

---

### **12. hotels() Endpoint** (main.py:627-635)

**Purpose**: Returns all hotels or filters by max price.

**Query Parameters**:
- `max_price` - Optional filter by maximum price per night

**Processing**:
1. Loads all hotels from `hotels_data.HOTELS`
2. If max_price provided, filters hotels
3. Sorts by rating (descending) then price (ascending)
4. Returns count and hotel list

---

### **13. supabase_test() Endpoint** (main.py:637-644)

**Purpose**: Tests Supabase database connection.

**Processing**: Calls `db.test_supabase_connection()` and returns result

**Response**: Connection status and error details if failed

---

## 🤖 Chatbot Intelligence Functions (chatbot.py)

The chatbot uses a hybrid approach: rule-based logic for hotel operations and Gemini AI for general conversations.

### **1. bot_reply()** (chatbot.py)

**Purpose**: Main chatbot function that handles all user messages.

**Logic Flow**:
1. Extracts entities from message (budget, dates, location, phone, visitors)
2. Detects user intent (hotel_search, booking, general_question)
3. **If hotel-related**: Uses rule-based search logic
4. **If general question**: Calls Gemini API for AI response
5. Returns (reply, suggestions, metadata)

**Entity Detection Functions Used**:
- `parse_budget()` - Extracts budget amount from message
- `parse_nights()` - Extracts number of nights
- `parse_visitors()` - Extracts number of guests
- `parse_phone()` - Extracts phone number
- `parse_checkin_date()` - Extracts check-in date

---

### **2. search_hotels_internal()** (chatbot.py:53-76)

**Purpose**: Core hotel search engine with multiple filters.

**Input Parameters**:
- `max_price` - Maximum price per night (optional)
- `location` - Hotel area name (optional)
- `min_rating` - Minimum star rating (optional)
- `amenities` - List of required amenities (optional)
- `limit` - Number of results (default 5)

**Processing Steps**:
1. Loads all hotels from `HOTELS` list
2. Filters by price: `price_per_night <= max_price`
3. Filters by location: case-insensitive area match
4. Filters by rating: `rating >= min_rating`
5. Filters by amenities: any amenity match (case-insensitive)
6. **Sorts by**: Rating (high to low), then Price (low to high)
7. Returns top N results based on limit

**Example**:
```python
results = search_hotels_internal(
    max_price=5000,
    location="Sitabuldi",
    min_rating=4.0,
    limit=5
)
```

---

### **3. find_hotels_by_budget()** (chatbot.py:78-81)

**Purpose**: Quick hotel search by budget only.

**Processing**:
1. Filters hotels where `price_per_night <= budget`
2. Sorts by rating (high to low) then price (low to high)
3. Returns all matching hotels

**Use Case**: When user only mentions budget

---

### **4. get_hotel_by_id()** (chatbot.py:83-87)

**Purpose**: Retrieves a single hotel by ID for booking details.

**Input**: `hotel_id` - Hotel identifier (string)

**Processing**: Linear search in HOTELS list matching ID

**Returns**: Hotel dictionary or None if not found

**Used In**: Booking and invoice generation endpoints

---

### **5. Entity Parsing Functions** (chatbot.py:23-103)

**parse_budget(message)**:
- Regex: `₹\s*(\d{3,6})|(\d{3,6})`
- Validates range: 500 ≤ budget ≤ 100,000
- Returns: integer budget or None

**parse_nights(message)**:
- Regex: `(\d+)\s*(?:night|nights|day|days)`
- Validates range: 1 ≤ nights ≤ 365
- Returns: integer nights or None

**parse_visitors(message)**:
- Regex: `(\d+)\s*(?:people|person|visitors|guests|pax)`
- Validates range: 1 ≤ visitors ≤ 10
- Returns: integer visitors or None

**parse_phone(message)**:
- Regex: `(?:\+91)?[\s-]?(\d{10})`
- Validates 10-digit Indian phone number
- Returns: phone string or None

**parse_checkin_date(message)**:
- Regex: `(\d{4})-(\d{2})-(\d{2})` (YYYY-MM-DD format)
- Validates date is in future
- Returns: date string (YYYY-MM-DD) or None

---

### **6. generate_bill()** (chatbot.py)

**Purpose**: Creates formatted bill text for booking confirmation.

**Input**:
- `hotel` - Hotel dictionary
- `nights` - Number of nights
- `name` - Customer name
- `booking_id` - Booking ID

**Processing**:
1. Calculates subtotal: `hotel['price_per_night'] × nights`
2. Calculates GST (18%): `subtotal × 0.18`
3. Calculates total: `subtotal + gst`
4. Formats as readable text bill

**Output**: Formatted string with:
- Hotel name and details
- Check-in date
- Number of nights
- Price breakdown
- Total amount

---

### **7. prepare_booking_confirmation()** (chatbot.py)

**Purpose**: Creates booking confirmation summary for review before payment.

**Input**: user_id, name, phone, hotel_id, checkin_date, nights

**Processing**:
1. Retrieves hotel details
2. Formats confirmation message
3. Stores booking state for later retrieval

**Returns**: (summary_text, booking_data_dict)

**Used In**: `/internal/confirm_booking` endpoint

---

## 📊 Database Schema & Tables

### **conversations** Table
```sql
CREATE TABLE conversations (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL,
  role VARCHAR(10), -- 'user' or 'bot'
  message TEXT,
  reply TEXT,
  created_at TIMESTAMP,
  meta JSONB -- metadata like budget, location, etc.
);
```

### **bookings** Table
```sql
CREATE TABLE bookings (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  hotel_id VARCHAR(255),
  hotel_name VARCHAR(255),
  checkin_date DATE,
  nights INTEGER,
  visitors INTEGER,
  total_price DECIMAL,
  created_at TIMESTAMP
);
```

### **users** Table
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY,
  name VARCHAR(255),
  phone VARCHAR(15),
  email VARCHAR(255),
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);
```

### **audit_logs** Table
```sql
CREATE TABLE audit_logs (
  id UUID PRIMARY KEY,
  action VARCHAR(100), -- BOOKING_CREATED, PAYMENT_INTENT_CREATED, etc.
  user_id UUID,
  resource_type VARCHAR(50), -- booking, payment, chat, etc.
  resource_id VARCHAR(255),
  status VARCHAR(20), -- success, failed, pending
  details JSONB,
  created_at TIMESTAMP
);
```

---

## 📁 Project Structure

```
nagpur-hotel-ai-agent/
├── Core Application
│   ├── main.py                      # FastAPI app & endpoints
│   ├── chatbot.py                  # AI logic & hotel search
│   ├── models.py                   # Pydantic data models
│   ├── db.py                       # Database & Supabase
│   ├── validators.py               # Input validation & PII
│   └── hotels_data.py              # Hotel database
│
├── Frontend
│   ├── index.html                  # Web interface
│   ├── ui_chat_snapshot.html       # Chat demo snapshot
│   └── ui_demo_output.html         # Demo output
│
├── Database
│   ├── supabase_init.py            # Database initialization
│   ├── supabase_tables.sql         # SQL schema
│   └── verify_supabase_tables.py   # Verification utility
│
├── Testing & Verification
│   ├── test_client_local.py        # Local client tests
│   ├── test_booking_flow.py        # Booking workflow tests
│   ├── test_confirmation_flow.py   # Confirmation tests
│   ├── verify_booking.py           # Booking verification
│   ├── verify_gemini.py            # Gemini API tests
│   └── connect_supabase.py         # Connection tests
│
├── Configuration
│   ├── requirements.txt            # Python dependencies
│   ├── .env.example                # Environment template
│   └── .gitignore                  # Git ignore rules
│
└── Documentation
    ├── README.md                   # This file
    ├── SETUP_GUIDE.md              # Setup instructions
    ├── DATA_FLOW.md                # Data flow diagrams
    └── GEMINI_INTEGRATION_COMPLETE.md  # AI integration docs
```

## 🔧 Configuration & Environment Setup

### Environment Variables Reference

Create a `.env` file with these variables:

```env
# REQUIRED - Supabase Database
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-supabase-anon-key

# REQUIRED - Google Gemini AI
GEMINIE_KEY=your-google-gemini-api-key

# OPTIONAL - Admin Credentials
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your-secure-password

# OPTIONAL - Frontend Configuration
FRONTEND_URL=http://localhost:3000

# OPTIONAL - Server Configuration
ENVIRONMENT=development
DEBUG=false
```

### How Each Variable is Used

| Variable | Used In | Purpose |
|----------|---------|---------|
| `SUPABASE_URL` | db.py, supabase_init.py | Connect to PostgreSQL database |
| `SUPABASE_KEY` | db.py | Authenticate with Supabase |
| `GEMINIE_KEY` | chatbot.py | Initialize Google Gemini AI model |
| `ADMIN_USERNAME` | main.py:117 | Admin login validation |
| `ADMIN_PASSWORD` | main.py:118 | Admin login validation |
| `FRONTEND_URL` | main.py:76 | CORS allowed origins |
| `ENVIRONMENT` | optional | Deployment environment identifier |
| `DEBUG` | optional | Enable verbose logging |

### Security Best Practices

**🔒 Secrets Management**:
1. **Never commit `.env`** to Git (it's in `.gitignore`)
2. **Never share API keys** via email, chat, or public repositories
3. **Rotate keys periodically** (every 3-6 months)
4. **Use different keys** for development and production
5. **Store secrets** in secure environment (GitHub Secrets, cloud provider secrets, etc.)

**Environment-Specific Setup**:
```bash
# Development (.env)
ENVIRONMENT=development
GEMINIE_KEY=dev-key-xxx
SUPABASE_KEY=dev-key-yyy

# Production (use secure secrets manager)
ENVIRONMENT=production
GEMINIE_KEY=prod-key-xxx (from secrets manager)
SUPABASE_KEY=prod-key-yyy (from secrets manager)
```

### Database Schema

Tables created automatically by `supabase_init.py`:

| Table | Purpose | Key Fields |
|-------|---------|-----------|
| `conversations` | Chat history | id, user_id, message, reply, created_at |
| `bookings` | Booking records | id, user_id, hotel_id, checkin_date, total_amount |
| `users` | User profiles | id, name, phone, email, created_at |
| `audit_logs` | Transaction logs | id, action, user_id, resource_type, status |

## 🧪 Testing

### Run All Tests

```bash
# Individual tests
python test_client_local.py           # Basic functionality
python test_booking_flow.py           # Booking workflow
python test_confirmation_flow.py      # Confirmation emails
python verify_gemini.py               # Gemini API
python verify_booking.py              # Booking verification
python connect_supabase.py            # Database connection
```

### Manual Testing

```bash
# Start server
python main.py

# In another terminal, test endpoint
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id":"test123","message":"Show hotels"}'
```

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| fastapi | 0.115.0 | Web framework |
| uvicorn | 0.30.0 | ASGI server |
| pydantic | 2.8.0 | Data validation |
| python-dotenv | 1.0.0 | Environment config |
| supabase | 2.4.2 | PostgreSQL client |
| google-generativeai | 0.7.2 | Gemini API |
| httpx | 0.27.0 | HTTP client |
| psycopg | binary | PostgreSQL adapter |

See [requirements.txt](requirements.txt) for complete list.

## 🚀 Deployment

### Heroku

```bash
heroku login
heroku create your-app-name
heroku config:set SUPABASE_URL=xxx SUPABASE_KEY=xxx GEMINIE_KEY=xxx
git push heroku main
```

### Railway

1. Push to GitHub repository
2. Connect at [railway.app](https://railway.app)
3. Add environment variables in dashboard
4. Deploy automatically on push

### Docker

```bash
docker build -t nagpur-hotel-ai .
docker run -p 8000:8000 --env-file .env nagpur-hotel-ai
```

### PythonAnywhere

1. Upload files to PythonAnywhere
2. Create virtual environment
3. Configure WSGI application
4. Add environment variables in Web tab
5. Reload web app

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork** the repository
2. **Create** feature branch: `git checkout -b feature/NewFeature`
3. **Commit** changes: `git commit -m 'Add NewFeature'`
4. **Push** to branch: `git push origin feature/NewFeature`
5. **Open** Pull Request with description

### Development Guidelines

- Follow PEP 8 style guide
- Write tests for new features
- Update documentation
- Keep commits atomic and descriptive

## 🔄 Complete User Journey & Workflow Examples

### **Example 1: Hotel Search & Booking Flow**

```
1. USER MESSAGE:
   "Show me hotels under ₹5000 near Sitabuldi for 3 nights"

2. CHAT ENDPOINT (/chat):
   - Parses budget: ₹5000
   - Parses location: "Sitabuldi"
   - Parses nights: 3
   - Detects intent: hotel_search

3. CHATBOT LOGIC (bot_reply):
   - Calls search_hotels_internal() with filters
   - Returns 4 hotels matching criteria
   - Generates response: "Found 4 hotels within budget..."
   - Provides suggestions: ["View details", "Book now"]

4. BOT RESPONSE:
   {
     "reply": "Found 4 hotels in Sitabuldi under ₹5000...",
     "suggestions": [...],
     "meta": {"budget": 5000, "hotels_count": 4}
   }

5. USER SELECTS HOTEL:
   - Sends message: "Book Grand Plaza for 3 nights"
   - Or uses /internal/confirm_booking endpoint

6. BOOKING CONFIRMATION (/internal/confirm_booking):
   - Validates all inputs
   - Calculates pricing: 4500 × 3 = 13,500
   - Calculates GST: 13,500 × 18% = 2,430
   - Returns confirmation with total: 15,930

7. USER CONFIRMS:
   - Proceeds to payment

8. CREATE BOOKING (/internal/book_hotel):
   - Creates user record (if new)
   - Creates booking record in DB
   - Logs audit entry
   - Returns booking_id: "bk_a1b2c3d4"

9. PAYMENT INTENT (/internal/payment_intent):
   - Generates payment_id: "pi_a1b2c3d4"
   - Returns payment URL and client secret

10. GENERATE INVOICE (/internal/generate_invoice):
    - Fetches booking details
    - Calculates final amounts
    - Returns HTML invoice
    - Stores in audit logs
```

### **Example 2: Admin Dashboard Access**

```
1. ADMIN LOGIN (/admin/login):
   Request: {"username": "admin", "password": "xxx"}
   Response: {"token": "adm_a1b2c3d4...", "expires_in": 7200}

2. FETCH CHATS (/admin/chats):
   Header: Authorization: Bearer adm_a1b2c3d4...
   Response: [
     {user_id, message, created_at, meta},
     {user_id, message, created_at, meta},
     ...
   ]

3. TOKEN VALIDATION:
   - Checks token in ADMIN_TOKENS dict
   - Validates not expired
   - Returns 401 if invalid/expired
```

---

## 💡 Common Use Cases

### **Use Case 1: User wants to book at specific budget**
- Message: "Show hotels ₹3000 per night"
- Flow: parse_budget() → search_hotels_internal() → Results
- Response: Hotels sorted by rating (best first)

### **Use Case 2: User asks general question**
- Message: "What's the best time to visit Nagpur?"
- Flow: Intent detection → Not hotel-related → Call Gemini API
- Response: AI-generated answer about Nagpur tourism

### **Use Case 3: Multiple filters**
- Message: "5-star hotels near Sitabuldi with WiFi under ₹10000"
- Flow: Parse all entities → search_hotels_internal() with all filters
- Response: Hotels matching ALL criteria

### **Use Case 4: Admin views all conversations**
- Admin logs in → Gets token → Uses token to fetch all chats
- Response: Full conversation history for analytics

---

## 🚀 Deployment Guide

### **Local Testing (Development)**
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create .env file with test credentials
cp .env.example .env
# Edit .env with your Supabase and Gemini keys

# 3. Initialize database
python supabase_init.py

# 4. Run server
python main.py

# 5. Test endpoints
curl http://localhost:8000/docs
```

### **Production Deployment (Heroku)**

```bash
# 1. Create Heroku app
heroku login
heroku create your-app-name

# 2. Set environment variables
heroku config:set SUPABASE_URL=xxx
heroku config:set SUPABASE_KEY=xxx
heroku config:set GEMINIE_KEY=xxx
heroku config:set ADMIN_USERNAME=admin
heroku config:set ADMIN_PASSWORD=your-secure-pass

# 3. Create Procfile
echo "web: uvicorn main:app --host 0.0.0.0 --port \$PORT" > Procfile

# 4. Deploy
git push heroku main

# 5. View logs
heroku logs --tail
```

### **Docker Deployment**

```bash
# Build image
docker build -t hotel-ai-agent .

# Run container
docker run -p 8000:8000 \
  -e SUPABASE_URL=xxx \
  -e SUPABASE_KEY=xxx \
  -e GEMINIE_KEY=xxx \
  hotel-ai-agent

# Or use docker-compose
docker-compose up
```

---

## 🆘 Troubleshooting

### **"ModuleNotFoundError: No module named 'fastapi'"**

**Solution:** Activate virtual environment and install dependencies:
```bash
# Windows
.\.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate

# Then install
pip install -r requirements.txt
```

### **"SUPABASE_URL not set" or authentication errors**

**Solution:** Verify environment variables are correctly set:

```bash
# 1. Check .env file exists in project root (not subdirectory)
ls -la .env

# 2. Verify file contents
cat .env

# 3. Check variables are loaded
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('SUPABASE_URL:', os.getenv('SUPABASE_URL'))"

# 4. If variables still not loading, reload manually
```

**Common mistakes**:
- `.env` is in subdirectory instead of project root
- Missing `=` sign in variable assignment
- Extra spaces around `=` (e.g., `SUPABASE_URL = value` instead of `SUPABASE_URL=value`)
- File has no `SUPABASE_URL` variable at all

### **"GEMINIE_KEY not found" - AI responses not working**

**Solution**: Check Gemini API key setup:

```bash
# 1. Get API key from https://ai.google.dev/
# 2. Add to .env file
echo "GEMINIE_KEY=your-key-here" >> .env

# 3. Restart server
# Note: Variable name is GEMINIE_KEY (with typo), not GEMINI_KEY

# 4. Test Gemini connection
python verify_gemini.py
```

### **"Rate limit exceeded" - Getting 429 errors**

**Solution**: Rate limiting is set to 100 requests/minute per IP. 

```bash
# Ways to fix:
# 1. Wait a minute for limit to reset
# 2. Use different IP/device
# 3. Modify RateLimitMiddleware in main.py to increase limit
# 4. Disable for local testing by commenting out middleware

# To check current rate limit:
curl -I http://localhost:8000/chat
# Look for response code 429
```

### **"Booking not found" - 404 errors**

**Solution**: Check booking ID is correct:

```bash
# 1. Verify booking was created
# Check database bookings table in Supabase dashboard

# 2. Use correct booking_id format
# Should be format: bk_xxxxx (generated UUID)

# 3. Check booking exists for this user
# Make sure user_id matches the booking's user_id
```

### **"Invalid date format" - Booking fails**

**Solution**: Use YYYY-MM-DD format for dates:

```bash
# Correct format
2025-12-20

# Wrong format
12/20/2025 ❌
20-12-2025 ❌
Dec 20, 2025 ❌

# Date must be in future
# Future date: 2025-12-20 ✓
# Past date: 2020-01-01 ✗

# Test date parsing
python -c "from chatbot import parse_checkin_date; print(parse_checkin_date('2025-12-20'))"
```

### **"Invalid phone number" - Validation fails**

**Solution**: Phone number must be 10 digits (Indian format):

```bash
# Correct format
9876543210

# With country code
+919876543210

# Wrong format
98 7654 3210 ❌
9876-543-210 ❌
9876543 ❌ (only 7 digits)
```

### **Database connection timeout**

**Solution**: Check Supabase network and credentials:

```bash
# 1. Test connection
python connect_supabase.py

# 2. Verify SUPABASE_URL format
# Should be: https://xxxxx.supabase.co (not http://)

# 3. Check network connectivity
ping supabase.co

# 4. Verify IP is allowed in Supabase dashboard
# Go to Project Settings → Network

# 5. Check anon key has correct permissions
# Go to Project Settings → API
```

### **Invoice generation returns empty HTML**

**Solution**: Ensure booking exists before generating invoice:

```bash
# 1. Create booking first with /internal/book_hotel
# 2. Get booking_id from response
# 3. Use same booking_id for /internal/generate_invoice

# Check request format
curl -X POST http://localhost:8000/internal/generate_invoice \
  -H "Content-Type: application/json" \
  -d '{"booking_id":"bk_xxxxx","gst_percent":18}'
```

### **Admin login returns 401 "Invalid credentials"**

**Solution**: Check admin credentials:

```bash
# Default credentials from .env
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123

# Or set custom in .env
ADMIN_USERNAME=your_username
ADMIN_PASSWORD=your_secure_password

# Verify before login
cat .env | grep ADMIN

# Token expires after 2 hours
# After expiry, login again to get new token
```

### **Admin fetch chats returns 401 "Invalid token"**

**Solution**: Token validation and refresh:

```bash
# 1. Login first to get token
curl -X POST http://localhost:8000/admin/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# 2. Use token in Authorization header
curl -X GET http://localhost:8000/admin/chats?limit=10 \
  -H "Authorization: Bearer adm_xxxxxxxx"

# 3. Check token expiry (2 hours = 7200 seconds)
# If expired, login again to get new token

# 4. Correct header format
# Authorization: Bearer <token> ✓
# Bearer: <token> ❌
# Authorization: <token> ❌
```

---

## 📞 Getting Help

### **Debugging Steps**

1. **Check logs**: Look at console output for error messages
2. **Test endpoints**: Use Swagger UI at `/docs`
3. **Verify database**: Check Supabase dashboard for data
4. **Test files**: Run test scripts:
   ```bash
   python test_client_local.py           # Basic tests
   python verify_gemini.py               # Gemini API test
   python connect_supabase.py            # Database test
   ```

### **Common Error Codes**

| Code | Meaning | Solution |
|------|---------|----------|
| **200** | Success | ✓ Request successful |
| **400** | Bad Request | Invalid input (check parameters) |
| **401** | Unauthorized | Missing/invalid auth token |
| **404** | Not Found | Hotel/booking/resource doesn't exist |
| **429** | Too Many Requests | Rate limit exceeded, wait a minute |
| **500** | Server Error | Server crash, check logs |

---

## 📚 Additional Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Supabase Docs**: https://supabase.com/docs/
- **Google Gemini API**: https://ai.google.dev/docs
- **Pydantic Validation**: https://docs.pydantic.dev/
- **Python Regex**: https://docs.python.org/3/library/re.html

---

## 📝 File Purpose Reference

| File | Purpose |
|------|---------|
| **main.py** | FastAPI app, endpoints, rate limiting, admin auth |
| **chatbot.py** | Bot logic, hotel search, entity parsing, Gemini integration |
| **models.py** | Pydantic request/response models and validation |
| **db.py** | Supabase connection, CRUD operations |
| **validators.py** | Input validation, PII masking, data sanitization |
| **hotels_data.py** | Hotel database (in-memory) |
| **supabase_init.py** | Database schema initialization |
| **supabase_tables.sql** | SQL schema definition |
| **index.html** | Frontend web interface |
| **requirements.txt** | Python dependencies |
| **.env** | Environment variables (secrets) |
| **.env.example** | Environment template (without secrets) |
| **.gitignore** | Git ignore rules (includes .env) |

---

## ✅ Verification Checklist

Before deploying to production:

- [ ] All environment variables are set in `.env`
- [ ] Supabase connection works (`python connect_supabase.py`)
- [ ] Gemini API key works (`python verify_gemini.py`)
- [ ] Database tables created (`python supabase_init.py`)
- [ ] Frontend loads without errors (`index.html`)
- [ ] All tests pass (`python test_*.py`)
- [ ] Rate limiting is configured appropriately
- [ ] Admin credentials are secure (not default)
- [ ] CORS origins are correct for your domain
- [ ] No sensitive data in logs or error messages

---

## 📞 Support & Contact

For issues, suggestions, or contributions:
1. Check troubleshooting section above
2. Review API documentation at `/docs`
3. Check Supabase/Gemini API documentation
4. Open issue on GitHub repository
dir .env          # Windows
ls -la .env       # macOS/Linux

# Verify contents
type .env         # Windows
cat .env          # macOS/Linux
```

### Port 8000 already in use

**Solution:** Use different port:
```bash
uvicorn main:app --port 8001 --reload
```

### Database tables don't exist

**Solution:** Initialize database:
```bash
python supabase_init.py
```

### Gemini API not responding

**Solution:** Verify API key:
```bash
# Check GEMINIE_KEY in .env
# Verify at https://ai.google.dev
# Check API quota and billing
```

### CORS errors in browser

**Solution:** Check CORS configuration in `main.py`:
```python
# Should already be configured, but verify:
app.add_middleware(CORSMiddleware, allow_origins=["*"], ...)
```

## 📊 Performance & Monitoring

### Monitoring

- Check logs: `tail -f server.log`
- API metrics at `/docs`
- Database metrics in Supabase dashboard
- Gemini API quota in Google Cloud Console

### Optimization Tips

- Enable response caching for hotel searches
- Use connection pooling for Supabase
- Cache Gemini API responses
- Monitor API rate limits

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

## 📧 Support & Contact

- **Issues**: Open [GitHub Issues](https://github.com/yourusername/nagpur-hotel-ai-agent/issues)
- **Discussions**: Join [GitHub Discussions](https://github.com/yourusername/nagpur-hotel-ai-agent/discussions)
- **Email**: your-email@example.com

## 🙏 Acknowledgments

- **FastAPI** - Modern, fast web framework
- **Supabase** - Excellent PostgreSQL hosting
- **Google Gemini** - State-of-the-art AI models
- **Community** - All contributors and users

---

<div align="center">

Made with ❤️ for hotel booking enthusiasts

[⬆ Back to top](#nagpur-hotel-ai-booking-agent-)

</div>
