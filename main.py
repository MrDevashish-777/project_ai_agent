import os
import logging
import json
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.responses import JSONResponse
from models import (
    ChatRequest, ChatResponse, BookingRequest, User,
    InternalSearchHotelsRequest, InternalBookHotelRequest,
    CreatePaymentIntentRequest, GenerateInvoiceRequest,
    AdminLoginRequest
)
from chatbot import bot_reply, get_hotel_by_id, generate_bill, search_hotels_internal, prepare_booking_confirmation
from validators import validate_booking_input, mask_pii, validate_phone, validate_date
import db
from db import create_audit_log
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import uuid
from collections import defaultdict
import time

load_dotenv()

app = FastAPI(title="Nagpur Hotel AI Agent")

class StructuredLogger:
    """Enhanced logging with structured JSON support for audit trails."""
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.setup_logging()
    
    def setup_logging(self):
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    
    def log_action(self, action, user_id, resource_type, resource_id, status, details=None):
        """Log structured action for audit trail."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "user_id": user_id,
            "resource_type": resource_type,
            "resource_id": resource_id,
            "status": status,
            "details": details or {}
        }
        self.logger.info(json.dumps(log_entry))
        return log_entry
    
    def info(self, msg):
        self.logger.info(msg)
    
    def warning(self, msg):
        self.logger.warning(msg)
    
    def error(self, msg, exc_info=False):
        self.logger.error(msg, exc_info=exc_info)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = StructuredLogger(__name__)

ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:8000",
    os.getenv("FRONTEND_URL", "").strip() if os.getenv("FRONTEND_URL") else None
]
ALLOWED_ORIGINS = [origin for origin in ALLOWED_ORIGINS if origin]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    max_age=3600,
)

class RateLimitMiddleware:
    def __init__(self, app, requests_per_minute: int = 100):
        self.app = app
        self.requests_per_minute = requests_per_minute
        self.requests = defaultdict(list)
    
    async def __call__(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()
        
        if client_ip not in self.requests:
            self.requests[client_ip] = []
        
        self.requests[client_ip] = [req_time for req_time in self.requests[client_ip] if now - req_time < 60]
        
        if len(self.requests[client_ip]) >= self.requests_per_minute:
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            return JSONResponse(
                status_code=429,
                content={"detail": "Too many requests. Please try again later."}
            )
        
        self.requests[client_ip].append(now)
        return await call_next(request)

rate_limit_middleware = RateLimitMiddleware(app, requests_per_minute=100)
app.middleware("http")(lambda request, call_next: rate_limit_middleware(request, call_next))

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
ADMIN_TOKENS = {}

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    try:
        user_id = req.user_id or f"u_{uuid.uuid4().hex[:10]}"
        db.save_conversation(user_id, "user", req.message, meta={})
        reply, suggestions, meta = bot_reply(req.message, user_id=user_id)
        db.save_conversation(user_id, "bot", reply, meta=meta)
        logger.log_action(
            action="CHAT_MESSAGE",
            user_id=user_id,
            resource_type="chat",
            resource_id=user_id,
            status="success",
            details={"message_length": len(req.message), "has_suggestions": len(suggestions or []) > 0}
        )
        return ChatResponse(reply=reply, suggestions=suggestions, meta=meta)
    except Exception as e:
        logger.error(f"Chat error: {e}", exc_info=True)
        logger.log_action(
            action="CHAT_MESSAGE",
            user_id=req.user_id or "unknown",
            resource_type="chat",
            resource_id="unknown",
            status="error",
            details={"error": str(e)}
        )
        raise HTTPException(status_code=500, detail="Chat processing failed")

@app.post("/internal/search_hotels")
async def search_hotels(req: InternalSearchHotelsRequest):
    try:
        results = search_hotels_internal(
            max_price=req.max_price,
            location=req.location,
            min_rating=req.min_rating,
            amenities=req.amenities,
            limit=req.limit
        )
        logger.log_action(
            action="HOTEL_SEARCH",
            user_id=None,
            resource_type="search",
            resource_id=str(uuid.uuid4()),
            status="success",
            details={"results_count": len(results), "max_price": req.max_price, "location": req.location}
        )
        return {"count": len(results), "hotels": results}
    except Exception as e:
        logger.error(f"Search error: {e}", exc_info=True)
        logger.log_action(
            action="HOTEL_SEARCH",
            user_id=None,
            resource_type="search",
            resource_id="unknown",
            status="error",
            details={"error": str(e)}
        )
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/internal/confirm_booking")
async def confirm_booking(req: InternalBookHotelRequest):
    """Generate booking confirmation summary without creating the booking yet."""
    try:
        is_valid, error = validate_booking_input(
            req.name, req.phone, req.checkin_date, req.nights, req.visitors
        )
        if not is_valid:
            logger.warning(f"Invalid booking confirmation input: {error}")
            raise HTTPException(status_code=400, detail=error)
        
        hotel = get_hotel_by_id(req.hotel_id)
        if not hotel:
            logger.warning(f"Hotel not found: {req.hotel_id}")
            raise HTTPException(status_code=404, detail="Hotel not found")
        
        summary, booking_data = prepare_booking_confirmation(
            req.user_id, req.name, req.phone, req.hotel_id, req.checkin_date, req.nights
        )
        
        total_price = hotel["price_per_night"] * req.nights
        tax = total_price * 0.18
        
        logger.info(f"Booking confirmation generated for user {req.user_id}")
        
        return {
            "status": "confirmation_pending",
            "summary": summary,
            "booking_details": {
                "hotel_name": hotel["name"],
                "price_per_night": hotel["price_per_night"],
                "nights": req.nights,
                "subtotal": total_price,
                "gst": tax,
                "total": total_price + tax
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Booking confirmation error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/internal/book_hotel")
async def book_hotel_internal(req: InternalBookHotelRequest):
    try:
        is_valid, error = validate_booking_input(
            req.name, req.phone, req.checkin_date, req.nights, req.visitors
        )
        if not is_valid:
            logger.warning(f"Invalid booking input: {error}")
            logger.log_action(
                action="BOOKING_ATTEMPT",
                user_id=req.user_id,
                resource_type="booking",
                resource_id="unknown",
                status="validation_failed",
                details={"error": error}
            )
            raise HTTPException(status_code=400, detail=error)
        
        hotel = get_hotel_by_id(req.hotel_id)
        if not hotel:
            logger.warning(f"Hotel not found: {req.hotel_id}")
            raise HTTPException(status_code=404, detail="Hotel not found")
        
        user = db.upsert_user(req.name, req.phone)
        user_id = user.get("id")
        total_price = hotel["price_per_night"] * req.nights
        
        booking = db.create_booking(
            user_id, req.hotel_id, hotel["name"],
            req.checkin_date, req.nights, total_price, req.visitors
        )
        
        booking_id = booking["id"]
        
        create_audit_log(
            action="BOOKING_CREATED",
            user_id=user_id,
            resource_type="booking",
            resource_id=booking_id,
            details={
                "hotel_name": hotel["name"],
                "checkin_date": req.checkin_date,
                "nights": req.nights,
                "visitors": req.visitors,
                "total_price": total_price
            }
        )
        
        logger.log_action(
            action="BOOKING_CREATED",
            user_id=user_id,
            resource_type="booking",
            resource_id=booking_id,
            status="success",
            details={
                "hotel_name": hotel["name"],
                "nights": req.nights,
                "visitors": req.visitors,
                "total_price": total_price
            }
        )
        
        return {
            "status": "success",
            "booking_id": booking_id,
            "total_price": total_price,
            "hotel": hotel
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Booking error: {e}", exc_info=True)
        logger.log_action(
            action="BOOKING_CREATED",
            user_id=req.user_id or "unknown",
            resource_type="booking",
            resource_id="unknown",
            status="error",
            details={"error": str(e)}
        )
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/internal/payment_intent")
async def create_payment_intent(req: CreatePaymentIntentRequest):
    try:
        if req.amount_inr <= 0:
            logger.warning(f"Invalid payment amount: {req.amount_inr}")
            raise HTTPException(status_code=400, detail="Amount must be positive")
        
        payment_id = f"pi_{uuid.uuid4().hex[:12]}"
        payment_url = f"https://payment.example.com/{payment_id}"
        client_secret = f"sk_{uuid.uuid4().hex[:20]}"
        
        create_audit_log(
            action="PAYMENT_INTENT_CREATED",
            user_id=None,
            resource_type="payment",
            resource_id=payment_id,
            details={
                "amount_inr": req.amount_inr,
                "currency": req.currency,
                "booking_id": req.booking_id
            }
        )
        
        logger.info(f"Payment intent created: {payment_id} for ₹{req.amount_inr}")
        
        return {
            "payment_id": payment_id,
            "amount_inr": req.amount_inr,
            "currency": req.currency,
            "payment_url": payment_url,
            "client_secret": client_secret,
            "status": "pending"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Payment intent error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/internal/generate_invoice")
async def generate_invoice_internal(req: GenerateInvoiceRequest):
    try:
        bookings = db.supabase.table("bookings").select("*").eq("id", req.booking_id).execute()
        if not bookings.data:
            logger.warning(f"Booking not found for invoice: {req.booking_id}")
            raise HTTPException(status_code=404, detail="Booking not found")
        
        booking = bookings.data[0]
        hotel = get_hotel_by_id(booking["hotel_id"])
        
        if not hotel:
            logger.warning(f"Hotel not found for booking: {booking['hotel_id']}")
            raise HTTPException(status_code=404, detail="Hotel not found")
        
        subtotal = booking["total_price"]
        gst = subtotal * (req.gst_percent / 100)
        total = subtotal + gst
        
        invoice_id = f"inv_{uuid.uuid4().hex[:10]}"
        
        invoice_html = f"""
        <html>
        <body>
        <h1>Invoice</h1>
        <p>Invoice ID: {invoice_id}</p>
        <p>Booking ID: {booking['id']}</p>
        <p>Hotel: {hotel['name']}</p>
        <p>Subtotal: ₹{subtotal:.2f}</p>
        <p>GST ({req.gst_percent}%): ₹{gst:.2f}</p>
        <p><b>Total: ₹{total:.2f}</b></p>
        </body>
        </html>
        """
        
        create_audit_log(
            action="INVOICE_GENERATED",
            user_id=booking.get("user_id"),
            resource_type="invoice",
            resource_id=invoice_id,
            details={
                "booking_id": req.booking_id,
                "subtotal": subtotal,
                "gst": gst,
                "total": total
            }
        )
        
        logger.info(f"Invoice generated: {invoice_id} for booking {req.booking_id}")
        
        return {
            "invoice_id": invoice_id,
            "booking_id": req.booking_id,
            "subtotal": subtotal,
            "gst": gst,
            "total": total,
            "invoice_html": invoice_html
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Invoice generation error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/admin/login")
async def admin_login(req: AdminLoginRequest):
    try:
        if req.username != ADMIN_USERNAME or req.password != ADMIN_PASSWORD:
            logger.warning(f"Failed admin login attempt for user: {req.username}")
            logger.log_action(
                action="ADMIN_LOGIN",
                user_id=req.username,
                resource_type="admin",
                resource_id=req.username,
                status="failed",
                details={"reason": "invalid_credentials"}
            )
            create_audit_log(
                action="ADMIN_LOGIN_FAILED",
                user_id=None,
                resource_type="admin",
                resource_id=req.username,
                details={"attempt_time": datetime.now().isoformat()}
            )
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        token = f"adm_{uuid.uuid4().hex[:20]}"
        ADMIN_TOKENS[token] = {
            "created_at": datetime.now(),
            "expires_at": datetime.now() + timedelta(hours=2)
        }
        
        logger.log_action(
            action="ADMIN_LOGIN",
            user_id=req.username,
            resource_type="admin",
            resource_id=req.username,
            status="success",
            details={"token_generated": True, "expires_in_hours": 2}
        )
        
        create_audit_log(
            action="ADMIN_LOGIN_SUCCESS",
            user_id=req.username,
            resource_type="admin",
            resource_id=req.username,
            details={"token_created": datetime.now().isoformat()}
        )
        
        return {"status": "success", "token": token, "expires_in": 7200}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Admin login error: {e}", exc_info=True)
        logger.log_action(
            action="ADMIN_LOGIN",
            user_id=req.username or "unknown",
            resource_type="admin",
            resource_id="unknown",
            status="error",
            details={"error": str(e)}
        )
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/admin/chats")
async def fetch_chats(limit: int = 50, authorization: str = Header(None)):
    try:
        if not authorization or not authorization.startswith("Bearer "):
            logger.warning("Fetch chats attempt without valid authorization")
            logger.log_action(
                action="ADMIN_FETCH_CHATS",
                user_id=None,
                resource_type="admin",
                resource_id="fetch_chats",
                status="failed",
                details={"reason": "missing_token"}
            )
            raise HTTPException(status_code=401, detail="Missing or invalid token")
        
        token = authorization.split(" ")[1]
        if token not in ADMIN_TOKENS:
            logger.warning(f"Fetch chats attempt with invalid token")
            logger.log_action(
                action="ADMIN_FETCH_CHATS",
                user_id=None,
                resource_type="admin",
                resource_id="fetch_chats",
                status="failed",
                details={"reason": "invalid_token"}
            )
            raise HTTPException(status_code=401, detail="Invalid token")
        
        token_data = ADMIN_TOKENS[token]
        if datetime.now() > token_data["expires_at"]:
            del ADMIN_TOKENS[token]
            logger.warning(f"Fetch chats attempt with expired token")
            logger.log_action(
                action="ADMIN_FETCH_CHATS",
                user_id=None,
                resource_type="admin",
                resource_id="fetch_chats",
                status="failed",
                details={"reason": "token_expired"}
            )
            raise HTTPException(status_code=401, detail="Token expired")
        
        conversations = db.supabase.table("conversations").select("*").limit(limit).order("created_at", desc=True).execute()
        
        safe_conversations = []
        for conv in conversations.data:
            safe_conv = {
                "id": conv.get("id"),
                "user_id": conv.get("user_id"),
                "role": conv.get("role"),
                "message_preview": conv.get("message", "")[:100],
                "created_at": conv.get("created_at"),
                "meta": conv.get("meta", {})
            }
            safe_conversations.append(safe_conv)
        
        logger.log_action(
            action="ADMIN_FETCH_CHATS",
            user_id=None,
            resource_type="admin",
            resource_id="fetch_chats",
            status="success",
            details={"conversation_count": len(safe_conversations), "limit": limit}
        )
        
        create_audit_log(
            action="ADMIN_FETCH_CHATS",
            user_id=None,
            resource_type="admin",
            resource_id="fetch_chats",
            details={"conversation_count": len(safe_conversations), "limit": limit}
        )
        
        return {"conversations": safe_conversations, "count": len(safe_conversations)}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Fetch chats error: {e}", exc_info=True)
        logger.log_action(
            action="ADMIN_FETCH_CHATS",
            user_id=None,
            resource_type="admin",
            resource_id="fetch_chats",
            status="error",
            details={"error": str(e)}
        )
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/book")
async def book(req: InternalBookHotelRequest):
    """Legacy /book endpoint for backwards compatibility with frontend."""
    try:
        is_valid, error = validate_booking_input(
            req.name, req.phone, req.checkin_date, req.nights, req.visitors
        )
        if not is_valid:
            logger.warning(f"Invalid booking input: {error}")
            raise HTTPException(status_code=400, detail=error)
        
        hotel = get_hotel_by_id(req.hotel_id)
        if not hotel:
            logger.warning(f"Hotel not found: {req.hotel_id}")
            raise HTTPException(status_code=404, detail="Hotel not found")
        
        user = db.upsert_user(req.name, req.phone)
        user_id = user.get("id")
        total_price = hotel["price_per_night"] * req.nights
        
        booking = db.create_booking(
            user_id, req.hotel_id, hotel["name"],
            req.checkin_date, req.nights, total_price, req.visitors
        )
        
        booking_id = booking["id"]
        
        create_audit_log(
            action="BOOKING_CREATED",
            user_id=user_id,
            resource_type="booking",
            resource_id=booking_id,
            details={
                "hotel_name": hotel["name"],
                "checkin_date": req.checkin_date,
                "nights": req.nights,
                "visitors": req.visitors,
                "total_price": total_price
            }
        )
        
        bill_text = generate_bill(hotel, req.nights, req.name, booking_id)
        
        logger.info(f"Booking created via /book: {booking_id}")
        
        return {
            "status": "success",
            "booking_id": booking_id,
            "bill": bill_text,
            "total_price": total_price,
            "hotel": hotel
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Booking error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/hotels")
async def hotels(max_price: int = None):
    from hotels_data import HOTELS
    if max_price:
        results = [h for h in HOTELS if h["price_per_night"] <= max_price]
    else:
        results = HOTELS
    results.sort(key=lambda x: (-x["rating"], x["price_per_night"]))
    return {"count": len(results), "hotels": results}

@app.get("/supabase_test")
async def supabase_test():
    try:
        info = db.test_supabase_connection()
        return info
    except Exception as e:
        logger.error(f"Supabase test error: {e}")
        return {"ok": False, "error": str(e)}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
