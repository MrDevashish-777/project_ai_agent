# Nagpur Hotel AI Booking Agent 🤖🏨

An intelligent AI-powered hotel booking chatbot that helps customers find and book hotels in Nagpur through natural conversation. Built with FastAPI, Supabase, and modern web technologies.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688.svg)](https://fastapi.tiangolo.com/)

## ✨ Features

- **🤖 Conversational AI Chatbot** - Natural language interface for hotel discovery and booking
- **💰 Smart Filtering** - Filter hotels by budget, location, and amenities
- **🏨 Rich Hotel Database** - Browse detailed hotel information with ratings, prices, and availability
- **📋 Bill Generation** - Automatic invoice generation with GST calculation
- **💾 Data Persistence** - Store bookings and conversation history in Supabase PostgreSQL
- **🎯 User Preferences** - Remember and leverage user preferences for personalized recommendations
- **📱 Responsive UI** - Modern HTML5/CSS3 interface compatible with desktop and mobile
- **⚡ RESTful API** - Clean, well-documented API endpoints with CORS support

## 🏗️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | FastAPI 0.115.0, Uvicorn |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Database** | Supabase (PostgreSQL) |
| **ORM/Client** | Supabase Python Client |
| **API** | RESTful with CORS middleware |

## 📋 Prerequisites

- **Python 3.9+** (tested with Python 3.13)
- **pip** or **conda** (Python package manager)
- **Virtual Environment** (venv or conda) - recommended
- **Supabase Account** (free tier available) - [Sign up here](https://supabase.com)
- **Git** (for cloning and version control)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/nagpur-hotel-ai-agent.git
cd nagpur-hotel-ai-agent
```

### 2. Create and Activate Virtual Environment

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

Create a `.env` file in the project root directory:

```env
# Supabase Configuration
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-supabase-api-key
```

**Getting Your Supabase Credentials:**
1. Create a free account at [supabase.com](https://supabase.com)
2. Create a new project
3. Go to Project Settings → API
4. Copy your Project URL and API Key
5. Paste them in your `.env` file

### 5. Initialize Database (First Time Only)

```bash
python supabase_init.py
```

### 6. Run the Application

**Start the backend server:**
```bash
python main.py
```

Or with Uvicorn directly:
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

**Open the frontend:**
- Open `index.html` in your web browser

The API will be available at `http://localhost:8000`

## 📚 API Endpoints

### Chat Endpoint

```http
POST /chat
Content-Type: application/json

{
  "user_id": "user123",
  "message": "I want to book a hotel under 5000 rupees"
}
```

**Response:**
```json
{
  "reply": "I found 3 hotels within your budget...",
  "suggestions": ["Show prices", "Filter by rating", "Book now"]
}
```

### Booking Endpoint

```http
POST /book
Content-Type: application/json

{
  "name": "John Doe",
  "phone": "9876543210",
  "hotel_id": 1,
  "checkin_date": "2025-12-20",
  "nights": 3,
  "visitors": 2
}
```

### Hotels Endpoint

```http
GET /hotels?max_price=5000
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Luxury Hotel",
    "price_per_night": 4500,
    "rating": 4.8,
    "location": "Sitabuldi",
    "amenities": ["WiFi", "AC", "Restaurant"]
  }
]
```

## 📁 Project Structure

```
nagpur-hotel-ai-agent/
├── main.py                    # FastAPI application entry point
├── chatbot.py                # AI chatbot logic and conversation handling
├── models.py                 # Pydantic data models
├── db.py                     # Database operations and Supabase integration
├── hotels_data.py            # Hotel database and data management
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
├── index.html                # Frontend HTML interface
├── supabase_init.py          # Database initialization script
├── supabase_tables.sql       # SQL schema for Supabase
├── verify_supabase_tables.py # Database verification utility
├── verify_booking.py         # Booking verification script
├── README.md                 # This file
└── __pycache__/              # Python cache (ignored by git)
```

## 🔧 Configuration

### Environment Variables

The application uses a `.env` file for configuration. Create a `.env` file in the project root:

```env
# Required - Supabase Configuration
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-api-key
```

**Never commit your `.env` file to version control!** It contains sensitive credentials.

### Database Schema

The application uses three main tables:

- **users**: Store customer information
- **bookings**: Store booking records
- **conversations**: Store chat history and conversation context

See `supabase_tables.sql` for the complete schema.

## 🧪 Testing

Run the included test scripts:

```bash
# Test Supabase connection
python connect_supabase.py

# Test client locally
python test_client_local.py

# Verify bookings
python verify_booking.py

# Verify database tables
python verify_supabase_tables.py
```

## 📦 Dependencies

See `requirements.txt` for complete list:

- **fastapi** - Modern web framework for building APIs
- **uvicorn** - ASGI server for running FastAPI
- **pydantic** - Data validation using Python type annotations
- **python-dotenv** - Load environment variables from .env files
- **supabase** - Python client for Supabase
- **httpx** - Modern HTTP client library
- **psycopg** - PostgreSQL adapter for Python

## 🚀 Deployment

### Deploy to Heroku

```bash
# Install Heroku CLI
heroku login
heroku create your-app-name
git push heroku main
```

### Deploy to Railway

1. Push to GitHub
2. Connect repository to [Railway](https://railway.app)
3. Add environment variables
4. Deploy

### Deploy to PythonAnywhere

1. Upload files to PythonAnywhere
2. Set up virtual environment
3. Configure WSGI application
4. Add environment variables in Web tab

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'fastapi'"
**Solution:** Ensure virtual environment is activated and dependencies are installed:
```bash
source .venv/bin/activate  # or .\.venv\Scripts\Activate.ps1 on Windows
pip install -r requirements.txt
```

### Issue: "SUPABASE_URL not set" or authentication errors
**Solution:** Verify your `.env` file exists in the project root with correct credentials:
```bash
ls -la .env  # Check if file exists
cat .env    # Verify contents (be careful with credentials!)
```

### Issue: Port 8000 already in use
**Solution:** Use a different port:
```bash
uvicorn main:app --port 8001 --reload
```

### Issue: Database tables don't exist
**Solution:** Initialize the database:
```bash
python supabase_init.py
```

## 📧 Support

For issues, questions, or suggestions:
- Open an [Issue](https://github.com/yourusername/nagpur-hotel-ai-agent/issues)
- Email: your-email@example.com
- Check [Discussions](https://github.com/yourusername/nagpur-hotel-ai-agent/discussions)

## 🙏 Acknowledgments

- FastAPI documentation and community
- Supabase for excellent database service
- Hotel data and booking system inspiration
- Contributors and users who provide feedback

---

**Made with ❤️ for hotel booking automation**

*Last Updated: December 2025*
