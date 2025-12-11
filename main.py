import os
import logging
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, Header
from models import (
    ChatRequest, ChatResponse, BookingRequest, User,
    InternalSearchHotelsRequest, InternalBookHotelRequest,
    CreatePaymentIntentRequest, GenerateInvoiceRequest,
    AdminLoginRequest
)
from chatbot import bot_reply, get_hotel_by_id, generate_bill, search_hotels_internal
from validators import validate_booking_input, mask_pii, validate_phone, validate_date
import db
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import uuid

load_dotenv()

app = FastAPI(title="Nagpur Hotel AI Agent")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)

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
        return ChatResponse(reply=reply, suggestions=suggestions, meta=meta)
    except Exception as e:
        logger.error(f"Chat error: {e}")
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
        logger.info(f"Search returned {len(results)} hotels")
        return {"count": len(results), "hotels": results}
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/internal/book_hotel")
async def book_hotel_internal(req: InternalBookHotelRequest):
    try:
        is_valid, error = validate_booking_input(
            req.name, req.phone, req.checkin_date, req.nights, req.visitors
        )
        if not is_valid:
            raise HTTPException(status_code=400, detail=error)
        
        hotel = get_hotel_by_id(req.hotel_id)
        if not hotel:
            raise HTTPException(status_code=404, detail="Hotel not found")
        
        user = db.upsert_user(req.name, req.phone)
        user_id = user.get("id")
        total_price = hotel["price_per_night"] * req.nights
        
        booking = db.create_booking(
            user_id, req.hotel_id, hotel["name"],
            req.checkin_date, req.nights, total_price, req.visitors
        )
        
        logger.info(f"Booking created: {booking['id']} for user {user_id}")
        
        return {
            "status": "success",
            "booking_id": booking["id"],
            "total_price": total_price,
            "hotel": hotel
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Booking error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/internal/payment_intent")
async def create_payment_intent(req: CreatePaymentIntentRequest):
    try:
        if req.amount_inr <= 0:
            raise HTTPException(status_code=400, detail="Amount must be positive")
        
        payment_id = f"pi_{uuid.uuid4().hex[:12]}"
        payment_url = f"https://payment.example.com/{payment_id}"
        client_secret = f"sk_{uuid.uuid4().hex[:20]}"
        
        logger.info(f"Payment intent created: {payment_id} for ₹{req.amount_inr}")
        
        return {
            "payment_id": payment_id,
            "amount_inr": req.amount_inr,
            "currency": req.currency,
            "payment_url": payment_url,
            "client_secret": client_secret,
            "status": "pending"
        }
    except Exception as e:
        logger.error(f"Payment intent error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/internal/generate_invoice")
async def generate_invoice_internal(req: GenerateInvoiceRequest):
    try:
        bookings = db.supabase.table("bookings").select("*").eq("id", req.booking_id).execute()
        if not bookings.data:
            raise HTTPException(status_code=404, detail="Booking not found")
        
        booking = bookings.data[0]
        hotel = get_hotel_by_id(booking["hotel_id"])
        
        if not hotel:
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
        logger.error(f"Invoice generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/admin/login")
async def admin_login(req: AdminLoginRequest):
    try:
        if req.username != ADMIN_USERNAME or req.password != ADMIN_PASSWORD:
            logger.warning(f"Failed admin login attempt for user: {req.username}")
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        token = f"adm_{uuid.uuid4().hex[:20]}"
        ADMIN_TOKENS[token] = {
            "created_at": datetime.now(),
            "expires_at": datetime.now() + timedelta(hours=2)
        }
        
        logger.info(f"Admin login successful")
        return {"status": "success", "token": token, "expires_in": 7200}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Admin login error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/admin/chats")
async def fetch_chats(limit: int = 50, authorization: str = Header(None)):
    try:
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing or invalid token")
        
        token = authorization.split(" ")[1]
        if token not in ADMIN_TOKENS:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        token_data = ADMIN_TOKENS[token]
        if datetime.now() > token_data["expires_at"]:
            del ADMIN_TOKENS[token]
            raise HTTPException(status_code=401, detail="Token expired")
        
        conversations = db.supabase.table("conversations").select("*").limit(limit).order("created_at", desc=True).execute()
        
        masked_conversations = []
        for conv in conversations.data:
            masked = dict(conv)
            if "message" in masked:
                pii = mask_pii("", "")
                masked["message_preview"] = masked["message"][:100]
            masked_conversations.append(masked)
        
        logger.info(f"Admin fetched {len(conversations.data)} conversations")
        return {"conversations": masked_conversations, "count": len(conversations.data)}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Fetch chats error: {e}")
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
