from typing import Tuple, List, Optional, Dict
import re
from hotels_data import HOTELS

user_preferences = {}

def parse_budget(message: str) -> Optional[int]:
    m = re.search(r"(\d{3,6})", message.replace(",", ""))
    if m:
        try:
            return int(m.group(1))
        except:
            return None
    return None

def parse_nights(message: str) -> Optional[int]:
    m = re.search(r"(\d+)\s*(?:night|nights|day|days)", message.lower())
    if m:
        try:
            return int(m.group(1))
        except:
            return None
    return None

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

    if any(w in lower for w in ["hi", "hello", "hey", "namaste"]):
        if user_id not in user_preferences:
            user_preferences[user_id] = {"budget": None, "nights": None}
        reply = "Hello! Welcome to Nagpur hotel helper. 🏨\n\nFirst, let me know:\n1️⃣ What's your budget per night? (e.g., '2500')\n2️⃣ How many nights/days? (e.g., '3 nights')"
        return reply, None, meta

    budget = parse_budget(user_msg)
    nights = parse_nights(user_msg)
    
    if user_id not in user_preferences:
        user_preferences[user_id] = {"budget": None, "nights": None}
    
    if budget:
        user_preferences[user_id]["budget"] = budget
        meta["budget"] = budget
    
    if nights:
        user_preferences[user_id]["nights"] = nights
        meta["nights"] = nights
    
    pref = user_preferences[user_id]
    
    if budget and not pref["nights"]:
        reply = f"Great! ₹{budget}/night budget noted. 📝\n\nNow, how many nights would you like to stay? (e.g., '3 nights', '5 days')"
        return reply, None, meta
    
    if nights and not pref["budget"]:
        reply = f"Perfect! {nights} nights noted. 📅\n\nWhat's your budget per night? (e.g., '₹2500', '2500')"
        return reply, None, meta
    
    if pref["budget"] and pref["nights"]:
        hotels = find_hotels_by_budget(pref["budget"])
        if not hotels:
            reply = f"Sorry—no hotels found under ₹{pref['budget']}/night. Want me to show options up to ₹{pref['budget'] + 2000}?"
            return reply, None, meta
        suggestions = []
        for h in hotels[:6]:
            suggestions.append({
                "id": h["id"],
                "name": h["name"],
                "price_per_night": h["price_per_night"],
                "rating": h["rating"],
                "area": h["area"]
            })
        reply = f"Found {len(hotels)} hotels within your budget (₹{pref['budget']}/night) for {pref['nights']} nights! Select one to proceed:"
        return reply, suggestions, meta

    if any(w in lower for w in ["show hotels", "list hotels", "hotels in nagpur", "show me hotels", "find hotels"]):
        hotels = sorted(HOTELS, key=lambda x: (-x["rating"], x["price_per_night"]))[:6]
        suggestions = [{"id": h["id"], "name": h["name"], "price_per_night": h["price_per_night"], "rating": h["rating"]} for h in hotels]
        reply = "Here are some hotels in Nagpur (id, name, price_per_night, rating). Reply with the hotel id to book or ask details."
        return reply, suggestions, meta

    m_id = re.search(r"\b(h\d{1,2})\b", user_msg.lower())
    if m_id:
        hid = m_id.group(1)
        hotel = get_hotel_by_id(hid)
        if hotel:
            meta["selected_hotel"] = hotel
            reply = (f"You chose *{hotel['name']}* in {hotel['area']}. Price ₹{hotel['price_per_night']}/night, rating {hotel['rating']}. "
                     "Do you want to book? If yes, please provide your name, phone, check-in date (YYYY-MM-DD) and number of nights.")
            return reply, [hotel], meta
        else:
            return "I couldn't find that hotel id. Please reply with a valid hotel id shown in the list.", None, meta

    if any(w in lower for w in ["book", "booking", "i want to book", "reserve"]):
        phone_m = re.search(r"(\+?\d{10,12})", user_msg.replace(" ", ""))
        date_m = re.search(r"(\d{4}-\d{2}-\d{2})", user_msg)
        nights_m = re.search(r"(\b\d+\b)\s*(?:night|nights|days)", lower)
        hotel_id_m = re.search(r"(h\d{1,2})", lower)
        name_m = re.search(r"name[:\-]?\s*([A-Za-z ]{2,40})", user_msg, re.IGNORECASE)

        extracted = {}
        if hotel_id_m:
            extracted["hotel_id"] = hotel_id_m.group(1)
        if phone_m:
            extracted["phone"] = phone_m.group(1)
        if date_m:
            extracted["checkin_date"] = date_m.group(1)
        if nights_m:
            extracted["nights"] = int(nights_m.group(1))
        if name_m:
            extracted["name"] = name_m.group(1).strip()

        meta.update(extracted)
        if extracted.get("hotel_id") and extracted.get("name") and extracted.get("phone") and extracted.get("checkin_date") and extracted.get("nights"):
            hotel = get_hotel_by_id(extracted["hotel_id"])
            if not hotel:
                return "Hotel id not found. Please check the id and try again.", None, meta
            total = hotel["price_per_night"] * extracted["nights"]
            reply = (f"Got it. I'll book *{hotel['name']}* for {extracted['nights']} nights from {extracted['checkin_date']} for {extracted['name']} (phone: {extracted['phone']}). "
                     f"The estimated total is ₹{total}. Reply 'confirm' to finalize booking.")
            meta["estimated_total"] = total
            return reply, [hotel], meta
        else:
            missing = []
            for k in ("hotel_id", "name", "phone", "checkin_date", "nights"):
                if k not in extracted and k not in meta:
                    missing.append(k)
            if missing:
                reply = "I need a few details to book: please provide " + ", ".join(missing) + ". Also include hotel id (e.g. h2)."
                return reply, None, meta

    if "confirm" in lower or "yes confirm" in lower:
        reply = "Confirmed! Processing your booking now..."
        meta["confirm"] = True
        return reply, None, meta

    pref = user_preferences.get(user_id, {})
    if pref.get("budget") or pref.get("nights"):
        if not pref.get("budget"):
            return "What's your budget per night? (e.g., '₹2500')", None, meta
        if not pref.get("nights"):
            return "How many nights would you like to stay?", None, meta
    
    return "I didn't catch that. Please tell me your budget (₹2500) and nights (3 nights), or reply with a hotel id (h2) to book.", None, meta
