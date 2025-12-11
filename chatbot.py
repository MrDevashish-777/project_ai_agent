from typing import Tuple, List, Optional, Dict
import re
from datetime import datetime
from hotels_data import HOTELS

user_preferences = {}
booking_in_progress = {}
booking_state = {}

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

def parse_phone(message: str) -> Optional[str]:
    m = re.search(r"(?:\+91)?[\s-]?(\d{10})", message)
    if m:
        return m.group(1)
    return None

def parse_checkin_date(message: str) -> Optional[str]:
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", message)
    if m:
        try:
            date_obj = datetime.strptime(f"{m.group(1)}-{m.group(2)}-{m.group(3)}", "%Y-%m-%d")
            if date_obj.date() > datetime.now().date():
                return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
        except ValueError:
            pass
    return None

def extract_name(message: str) -> Optional[str]:
    cleaned = re.sub(r"[\d\-\+\(\)]+", "", message).strip()
    if len(cleaned) >= 2 and len(cleaned) <= 100:
        return cleaned
    return None

def prepare_booking_confirmation(user_id: str, name: str, phone: str, hotel_id: str, checkin_date: str, nights: int) -> Tuple[str, Optional[dict]]:
    """Prepare booking confirmation with summary. Returns (summary_text, booking_dict)."""
    hotel = get_hotel_by_id(hotel_id)
    if not hotel:
        return ("❌ Hotel not found", None)
    
    total_price = hotel["price_per_night"] * nights
    
    summary = format_booking_summary(hotel, nights, total_price, name, checkin_date)
    confirmation_text = summary + "\n\n🔐 **Confirm booking? Please reply 'yes' to confirm or 'no' to cancel.**"
    
    booking_data = {
        "user_id": user_id,
        "name": name,
        "phone": phone,
        "hotel_id": hotel_id,
        "checkin_date": checkin_date,
        "nights": nights,
        "visitors": 1
    }
    
    booking_in_progress[user_id] = booking_data
    
    return (confirmation_text, booking_data)

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

def format_booking_summary(hotel: dict, nights: int, total_price: float, name: str = None, checkin_date: str = None) -> str:
    """Format booking details summary for user confirmation per spec."""
    price_per_night = hotel["price_per_night"]
    subtotal = total_price
    tax = subtotal * 0.18
    total_with_tax = subtotal + tax
    
    summary = f"""
📋 **BOOKING SUMMARY**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏨 Hotel Name: {hotel['name']}
📍 Location: {hotel['area']}
⭐ Rating: {hotel['rating']}/5.0
"""
    
    if name:
        summary += f"👤 Guest Name: {name}\n"
    
    if checkin_date:
        summary += f"📅 Check-in Date: {checkin_date}\n"
    
    summary += f"""
💰 Pricing Breakdown:
  • Price per night: ₹{price_per_night:,.2f}
  • Number of nights: {nights}
  ┌─────────────────────────────────┐
  • Subtotal (Before Taxes): ₹{subtotal:,.2f}
  
📊 Taxes & Total:
  • GST (18%): ₹{tax:,.2f}
  
💳 Final Amount:
  ✅ TOTAL AMOUNT DUE: ₹{total_with_tax:,.2f}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    return summary

def bot_reply(user_msg: str, user_id: str = None) -> Tuple[str, Optional[List[dict]], dict]:
    lower = user_msg.lower()
    meta = {}

    if any(w in lower for w in ["hi", "hello", "hey", "namaste", "start", "begin"]):
        if user_id not in user_preferences:
            user_preferences[user_id] = {"budget": None, "nights": None, "location": None, "selected_hotel": None}
        if user_id in booking_in_progress:
            del booking_in_progress[user_id]
        if user_id in booking_state:
            del booking_state[user_id]
        reply = "🏨 Welcome to Nagpur Hotel Booking Assistant!\n\nTo help you find the perfect hotel, please tell me:\n1️⃣ Your budget per night (e.g., '₹3000')\n2️⃣ Number of nights (e.g., '3 nights')\n3️⃣ Preferred location (optional, e.g., 'Sitabuldi')"
        return reply, None, meta

    if user_id not in user_preferences:
        user_preferences[user_id] = {"budget": None, "nights": None, "location": None, "selected_hotel": None}
    
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
    
    m_id = re.search(r"\b(h\d{1,2})\b", user_msg.lower())
    if m_id and not user_id in booking_state:
        hid = m_id.group(1)
        hotel = get_hotel_by_id(hid)
        if hotel:
            pref["selected_hotel"] = hotel
            meta["selected_hotel"] = hotel
            details = f"⭐ {hotel['rating']} | 💰 ₹{hotel['price_per_night']}/night | 📍 {hotel['area']}\n\nAmenities: {hotel.get('amenities', 'N/A')}"
            reply = f"📍 *{hotel['name']}*\n\n{details}\n\nWould you like to book this hotel?"
            return reply, [hotel], meta
        else:
            return "❌ I couldn't find that hotel id. Please use the id shown in the list (e.g., 'h1', 'h2').", None, meta

    if any(w in lower for w in ["show hotels", "list hotels", "hotels in nagpur", "show me hotels", "find hotels"]):
        hotels = sorted(HOTELS, key=lambda x: (-x["rating"], x["price_per_night"]))[:6]
        suggestions = [
            {"id": h["id"], "name": h["name"], "price_per_night": h["price_per_night"], "rating": h["rating"], "area": h["area"]}
            for h in hotels
        ]
        reply = "📋 Here are popular hotels in Nagpur. Click on a hotel or reply with the hotel id (e.g., 'h1') to view details or book."
        return reply, suggestions, meta

    if pref["budget"] and pref["nights"] and not pref.get("selected_hotel"):
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

    if user_id in booking_state:
        state = booking_state[user_id]
        
        if state["step"] == "confirm_summary":
            yes_keywords = ["yes", "confirm", "ok", "proceed", "book it", "go ahead", "yep", "yeah"]
            no_keywords = ["no", "cancel", "back", "change", "nope", "decline"]
            
            matches_yes = any(w in lower for w in yes_keywords)
            matches_no = any(w in lower for w in no_keywords)
            
            if matches_yes and not matches_no:
                reply = "✅ Perfect! Your booking is confirmed. Redirecting to payment. Your booking will be completed once payment is processed."
                meta["action"] = "proceed_to_payment"
                meta["booking"] = state["booking_data"]
                meta["booking_confirmed"] = True
                del booking_state[user_id]
                return reply, None, meta
            
            elif matches_no and not matches_yes:
                del booking_state[user_id]
                reply = "❌ Booking cancelled. No charges will be made. Let me help you search for different hotels. What's your budget per night?"
                user_preferences[user_id]["selected_hotel"] = None
                return reply, None, meta
            
            else:
                reply = "Please confirm by typing 'yes' to proceed with the booking, or 'no' to cancel."
                return reply, None, meta
        
        elif state["step"] == "collect_name":
            name = extract_name(user_msg)
            if name:
                state["name"] = name
                state["step"] = "collect_phone"
                reply = f"✅ Thank you, {name}. Now please provide your phone number (10 digits, e.g., 9876543210)."
                return reply, None, meta
            else:
                reply = "Please provide a valid name (at least 2 characters)."
                return reply, None, meta
        
        elif state["step"] == "collect_phone":
            phone = parse_phone(user_msg)
            if phone:
                state["phone"] = phone
                state["step"] = "collect_date"
                reply = f"✅ Thank you. Now please provide your check-in date in YYYY-MM-DD format (e.g., 2025-12-25)."
                return reply, None, meta
            else:
                reply = "Please provide a valid 10-digit phone number."
                return reply, None, meta
        
        elif state["step"] == "collect_date":
            date = parse_checkin_date(user_msg)
            if date:
                state["checkin_date"] = date
                state["step"] = "confirm_summary"
                
                summary, booking_data = prepare_booking_confirmation(
                    user_id, state["name"], state["phone"], state["hotel_id"], state["checkin_date"], state["nights"]
                )
                state["booking_data"] = booking_data
                return summary, None, meta
            else:
                reply = "Please provide a valid date in YYYY-MM-DD format (e.g., 2025-12-25)."
                return reply, None, meta
    
    if any(w in lower for w in ["book", "booking", "i want to book", "reserve", "proceed"]):
        selected_hotel = pref.get("selected_hotel")
        
        if not selected_hotel:
            reply = "📋 Please first select a hotel from the list before booking."
            return reply, None, meta
        
        nights_val = pref.get("nights")
        if not nights_val:
            reply = "How many nights would you like to stay?"
            return reply, None, meta
        
        booking_state[user_id] = {
            "step": "collect_name",
            "hotel_id": selected_hotel["id"],
            "nights": nights_val,
            "name": None,
            "phone": None,
            "checkin_date": None,
            "booking_data": None
        }
        
        reply = "📝 To complete your booking, I'll need some details.\n\nFirst, please provide your full name."
        meta["action"] = "collect_booking_details"
        return reply, None, meta

    if pref.get("budget") and pref.get("nights"):
        reply = f"You're looking for a hotel under ₹{pref['budget']}/night for {pref['nights']} nights. Would you like me to show you the available hotels?"
        return reply, None, meta
    
    return "I'm here to help you book a hotel! Tell me your budget (e.g., '₹3000') and number of nights (e.g., '3 nights'), or search by saying 'show hotels'.", None, meta
