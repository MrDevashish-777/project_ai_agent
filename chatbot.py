from typing import Tuple, List, Optional, Dict
import re
from hotels_data import HOTELS

user_preferences = {}

def parse_budget(message: str) -> Optional[int]:
    m = re.search(r"₹\s*(\d{3,6})|(\d{3,6})", message.replace(",", ""))
    if m:
        try:
            budget = int(m.group(1) if m.group(1) else m.group(2))
            return budget if 500 <= budget <= 100000 else None
        except:
            return None
    return None

def parse_nights(message: str) -> Optional[int]:
    m = re.search(r"(\d+)\s*(?:night|nights|day|days)", message.lower())
    if m:
        try:
            nights = int(m.group(1))
            return nights if 1 <= nights <= 365 else None
        except:
            return None
    return None

def search_hotels_internal(max_price: Optional[int] = None, location: Optional[str] = None, 
                          min_rating: Optional[float] = None, amenities: Optional[List[str]] = None, 
                          limit: int = 5) -> List[dict]:
    results = HOTELS.copy()
    
    if max_price:
        results = [h for h in results if h["price_per_night"] <= max_price]
    
    if location:
        location_lower = location.lower()
        results = [h for h in results if location_lower in h.get("area", "").lower()]
    
    if min_rating:
        results = [h for h in results if h.get("rating", 0) >= min_rating]
    
    if amenities:
        amenities_lower = [a.lower() for a in amenities]
        results = [
            h for h in results 
            if any(a in h.get("amenities", "").lower() for a in amenities_lower)
        ]
    
    results.sort(key=lambda x: (-x["rating"], x["price_per_night"]))
    return results[:limit]

def find_hotels_by_budget(budget: int) -> List[dict]:
    hotels = [h for h in HOTELS if h["price_per_night"] <= budget]
    hotels.sort(key=lambda x: (-x["rating"], x["price_per_night"]))
    return hotels

def get_hotel_by_id(hotel_id: str) -> Optional[dict]:
    for h in HOTELS:
        if h["id"] == hotel_id:
            return h
    return None

def generate_bill(hotel: dict, nights: int, guest_name: str, booking_id: str) -> str:
    price_per_night = hotel["price_per_night"]
    subtotal = price_per_night * nights
    tax = subtotal * 0.18
    total = subtotal + tax
    
    bill = f"""
╔════════════════════════════════════════╗
║         BOOKING CONFIRMATION BILL      ║
╠════════════════════════════════════════╣
║ Hotel: {hotel['name']:<30} ║
║ Location: {hotel['area']:<28} ║
║ Rating: {hotel['rating']} ⭐           {' '*16} ║
║ Guest: {guest_name:<30} ║
║ Booking ID: {booking_id[:8]:<24} ║
╠════════════════════════════════════════╣
║ Price/Night: ₹{price_per_night:<28} ║
║ Number of Nights: {nights:<20} ║
║ Subtotal: ₹{subtotal:<30.2f} ║
║ Tax (18% GST): ₹{tax:<25.2f} ║
╠════════════════════════════════════════╣
║ TOTAL AMOUNT: ₹{total:<27.2f} ║
╚════════════════════════════════════════╝
"""
    return bill

def bot_reply(user_msg: str, user_id: str = None) -> Tuple[str, Optional[List[dict]], dict]:
    lower = user_msg.lower()
    meta = {}

    if any(w in lower for w in ["hi", "hello", "hey", "namaste", "start", "begin"]):
        if user_id not in user_preferences:
            user_preferences[user_id] = {"budget": None, "nights": None, "location": None}
        reply = "🏨 Welcome to Nagpur Hotel Booking Assistant!\n\nTo help you find the perfect hotel, please tell me:\n1️⃣ Your budget per night (e.g., '₹3000')\n2️⃣ Number of nights (e.g., '3 nights')\n3️⃣ Preferred location (optional, e.g., 'Sitabuldi')"
        return reply, None, meta

    if user_id not in user_preferences:
        user_preferences[user_id] = {"budget": None, "nights": None, "location": None}
    
    budget = parse_budget(user_msg)
    nights = parse_nights(user_msg)
    location = None
    if not budget and not nights:
        for area in ["sitabuldi", "wardha road", "ramdas peth", "central avenue", "sadar", "dharampeth", "gandhibagh"]:
            if area in lower:
                location = area
                break
    
    pref = user_preferences[user_id]
    
    if budget:
        pref["budget"] = budget
        meta["budget"] = budget
    
    if nights:
        pref["nights"] = nights
        meta["nights"] = nights
    
    if location:
        pref["location"] = location
        meta["location"] = location
    
    if budget and not pref["nights"]:
        reply = f"✅ Budget ₹{budget}/night noted.\n\nHow many nights would you like to stay? (e.g., '3 nights')"
        return reply, None, meta
    
    if nights and not pref["budget"]:
        reply = f"✅ {nights} nights noted.\n\nWhat's your budget per night? (e.g., '₹2500')"
        return reply, None, meta
    
    if pref["budget"] and pref["nights"]:
        hotels = search_hotels_internal(
            max_price=pref["budget"],
            location=pref.get("location"),
            limit=6
        )
        
        if not hotels:
            reply = f"😔 Sorry, no hotels found under ₹{pref['budget']}/night. Would you like me to show options up to ₹{pref['budget'] + 1000}?"
            return reply, None, meta
        
        suggestions = [
            {
                "id": h["id"],
                "name": h["name"],
                "price_per_night": h["price_per_night"],
                "rating": h["rating"],
                "area": h["area"]
            }
            for h in hotels
        ]
        
        reply = f"🎉 Found {len(hotels)} hotels for {pref['nights']} nights within ₹{pref['budget']}/night. Here are the top options:\n\nSelect a hotel to proceed or ask for details."
        meta["hotels"] = suggestions
        return reply, suggestions, meta

    if any(w in lower for w in ["show hotels", "list hotels", "hotels in nagpur", "show me hotels", "find hotels"]):
        hotels = sorted(HOTELS, key=lambda x: (-x["rating"], x["price_per_night"]))[:6]
        suggestions = [
            {"id": h["id"], "name": h["name"], "price_per_night": h["price_per_night"], "rating": h["rating"], "area": h["area"]}
            for h in hotels
        ]
        reply = "📋 Here are popular hotels in Nagpur. Click on a hotel or reply with the hotel id (e.g., 'h1') to view details or book."
        return reply, suggestions, meta

    m_id = re.search(r"\b(h\d{1,2})\b", user_msg.lower())
    if m_id:
        hid = m_id.group(1)
        hotel = get_hotel_by_id(hid)
        if hotel:
            meta["selected_hotel"] = hotel
            details = f"⭐ {hotel['rating']} | 💰 ₹{hotel['price_per_night']}/night | 📍 {hotel['area']}\n\nAmenities: {hotel.get('amenities', 'N/A')}"
            reply = f"📍 *{hotel['name']}*\n\n{details}\n\nWould you like to book this hotel?"
            return reply, [hotel], meta
        else:
            return "❌ I couldn't find that hotel id. Please use the id shown in the list (e.g., 'h1', 'h2').", None, meta

    if any(w in lower for w in ["book", "booking", "i want to book", "reserve", "confirm", "proceed"]):
        pref = user_preferences.get(user_id, {})
        if not pref.get("budget") or not pref.get("nights"):
            reply = "📋 To book a hotel, please first tell me your budget and number of nights. What's your budget per night?"
            return reply, None, meta
        
        reply = "📝 Great! I'll open the booking form for you. Please provide your details (name, phone, check-in date) to complete the booking."
        meta["action"] = "open_booking_form"
        return reply, None, meta

    if pref.get("budget") and pref.get("nights"):
        reply = f"You're looking for a hotel under ₹{pref['budget']}/night for {pref['nights']} nights. Would you like me to show you the available hotels?"
        return reply, None, meta
    
    return "I'm here to help you book a hotel! Tell me your budget (e.g., '₹3000') and number of nights (e.g., '3 nights'), or search by saying 'show hotels'.", None, meta
