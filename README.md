# Nagpur Hotel AI Booking Agent 🤖🏨

An intelligent AI-powered hotel booking chatbot that helps customers find and book hotels in Nagpur through natural conversation. Features Google Gemini AI for smart recommendations, Supabase for data persistence, and a modern responsive web interface.

<div align="center">

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688.svg)](https://fastapi.tiangolo.com/)
[![Gemini API](https://img.shields.io/badge/Google_Gemini-API-4285F4.svg)](https://ai.google.dev/)
[![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-3ECF8E.svg)](https://supabase.com/)

</div>

## ✨ Key Features

- **🤖 AI-Powered Conversations** - Google Gemini integration for intelligent, context-aware responses
- **🏨 Smart Hotel Search** - Filter by budget, location, amenities, and ratings
- **💰 Budget-Conscious** - Affordable hotel options in Nagpur with transparent pricing
- **📋 Instant Billing** - Automatic invoice generation with GST calculation
- **💾 Persistent Storage** - Supabase PostgreSQL for bookings, conversations, and user data
- **🎯 Personalization** - Learn user preferences for tailored recommendations
- **📱 Responsive Design** - Mobile-friendly HTML5/CSS3 interface
- **⚡ RESTful API** - Well-documented endpoints with async support
- **🔐 Data Validation** - Input validation and PII masking for security
- **📊 Audit Logging** - Track all transactions and interactions

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

This creates all required tables and schema in your Supabase database.

### 6. Run the Application

**Start the backend server:**
```bash
python main.py
```

**Or with explicit Uvicorn command:**
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

**Access the application:**
- Frontend: Open `index.html` in your web browser
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs (Swagger UI)

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

### POST /chat - Chat with Bot

```http
POST /chat
Content-Type: application/json

{
  "user_id": "user123",
  "message": "Show me hotels under ₹5000"
}
```

**Response:**
```json
{
  "reply": "Found 5 hotels within budget...",
  "metadata": {
    "budget": 5000,
    "hotels_count": 5
  }
}
```

### POST /book - Make a Booking

```http
POST /book
Content-Type: application/json

{
  "name": "John Doe",
  "phone": "9876543210",
  "hotel_id": "hotel_001",
  "checkin_date": "2025-12-20",
  "nights": 3,
  "visitors": 2,
  "gst_rate": 18
}
```

### GET /hotels - Search Hotels

```http
GET /hotels?max_price=5000&location=Sitabuldi&min_rating=4.0&limit=10
```

**Response:**
```json
[
  {
    "id": "hotel_001",
    "name": "Grand Plaza",
    "price_per_night": 4500,
    "rating": 4.8,
    "area": "Sitabuldi",
    "amenities": ["WiFi", "AC", "Restaurant", "24/7 Service"]
  }
]
```

### GET /docs - Interactive API Documentation

Visit `http://localhost:8000/docs` for Swagger UI with all endpoints documented.

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

## 🔧 Configuration

### Environment Variables Reference

```env
# REQUIRED - Supabase (database)
SUPABASE_URL=https://your-id.supabase.co
SUPABASE_KEY=your-anon-key

# REQUIRED - Google Gemini (AI)
GEMINIE_KEY=your-gemini-api-key

# OPTIONAL - Server Configuration
ENVIRONMENT=development  # or production
DEBUG=true             # Verbose logging
```

**Important Security Notes:**
- Never commit `.env` to version control
- Never share API keys publicly
- Rotate keys periodically
- Use different keys for dev/prod environments

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

## 🆘 Troubleshooting

### "ModuleNotFoundError: No module named 'fastapi'"

**Solution:** Activate virtual environment and install dependencies:
```bash
# Windows
.\.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate

# Then install
pip install -r requirements.txt
```

### "SUPABASE_URL not set" or authentication errors

**Solution:** Check `.env` file:
```bash
# Verify file exists in project root
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
