import os
from fastapi import FastAPI, HTTPException
from models import ChatRequest, ChatResponse, BookingRequest, User
from chatbot import bot_reply, get_hotel_by_id, generate_bill
import db
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI(title="Nagpur Hotel AI Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    user_id = req.user_id
    db.save_conversation(user_id, "user", req.message, meta={})
    reply, suggestions, meta = bot_reply(req.message, user_id=user_id)
    db.save_conversation(user_id, "bot", reply, meta=meta)
    return {"reply": reply, "suggestions": suggestions}

@app.post("/book")
async def book(req: BookingRequest):
    user = db.upsert_user(req.name, req.phone)
    user_id = user.get("id")
    hotel = get_hotel_by_id(req.hotel_id)
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    total_price = hotel["price_per_night"] * req.nights
    booking = db.create_booking(user_id, req.hotel_id, hotel["name"], req.checkin_date, req.nights, total_price, req.visitors)
    bill = generate_bill(hotel, req.nights, req.name, booking["id"])
    db.save_conversation(user_id, "user", f"Book {hotel['name']} check-in {req.checkin_date} nights {req.nights} visitors {req.visitors}", meta={"booking_id": booking["id"], "action": "booking_submitted"})
    db.save_conversation(user_id, "bot", f"Booking confirmed!\n\n{bill}", meta={"booking": booking, "action": "booking_confirmed"})
    return {"status": "ok", "booking": booking, "bill": bill}

@app.get("/hotels")
async def hotels(max_price: int = None):
    from hotels_data import HOTELS
    if max_price:
        results = [h for h in HOTELS if h["price_per_night"] <= max_price]
    else:
        results = HOTELS
    results.sort(key=lambda x: (-x["rating"], x["price_per_night"]))
    return {"count": len(results), "hotels": results}

@app.get("/conversations/{user_id}")
async def get_conversations(user_id: str):
    r = db.supabase.table("conversations").select("*").eq("user_id", user_id).order("created_at", desc=False).execute()
    return {"conversations": r.data}

@app.get("/supabase_test")
async def supabase_test():
    try:
        info = db.test_supabase_connection()
        return info
    except Exception as e:
        return {"ok": False, "error": str(e)}

@app.get("/user_data/{user_id}")
async def get_user_data(user_id: str):
    try:
        conversations = db.get_user_conversations(user_id)
        bookings = db.get_user_bookings(user_id)
        return {
            "user_id": user_id,
            "conversations_count": len(conversations),
            "bookings_count": len(bookings),
            "conversations": conversations,
            "bookings": bookings
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}

@app.get("/all_data")
async def get_all_data():
    try:
        users_r = db.supabase.table("users").select("*").execute()
        conversations_r = db.supabase.table("conversations").select("*").execute()
        bookings_r = db.supabase.table("bookings").select("*").execute()
        
        return {
            "users": users_r.data,
            "total_users": len(users_r.data),
            "conversations": conversations_r.data,
            "total_conversations": len(conversations_r.data),
            "bookings": bookings_r.data,
            "total_bookings": len(bookings_r.data)
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
