import re
from datetime import datetime
from typing import Tuple, Optional

def validate_phone(phone: str) -> Tuple[bool, Optional[str]]:
    phone = phone.strip().replace("+", "").replace(" ", "").replace("-", "")
    if not phone.replace("+91", "").isdigit():
        return False, "Phone must contain only digits"
    if len(phone) < 10:
        return False, "Phone must be at least 10 digits"
    if len(phone) > 12:
        return False, "Phone must be at most 12 digits"
    return True, phone

def validate_date(date_str: str) -> Tuple[bool, Optional[str]]:
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d")
        if d.date() <= datetime.now().date():
            return False, "Check-in date must be in the future"
        return True, date_str
    except ValueError:
        return False, "Date must be in YYYY-MM-DD format"

def validate_nights(nights: int) -> Tuple[bool, str]:
    if not isinstance(nights, int) or nights < 1:
        return False, "Nights must be a positive integer"
    if nights > 365:
        return False, "Nights cannot exceed 365"
    return True, str(nights)

def validate_visitors(visitors: int) -> Tuple[bool, str]:
    if not isinstance(visitors, int) or visitors < 1:
        return False, "Visitors must be at least 1"
    if visitors > 10:
        return False, "Visitors cannot exceed 10"
    return True, str(visitors)

def validate_booking_input(name: str, phone: str, checkin_date: str, nights: int, visitors: int) -> Tuple[bool, Optional[str]]:
    if not name or len(name.strip()) < 2:
        return False, "Name must be at least 2 characters"
    if len(name) > 100:
        return False, "Name cannot exceed 100 characters"
    
    valid_phone, error = validate_phone(phone)
    if not valid_phone:
        return False, f"Phone: {error}"
    
    valid_date, error = validate_date(checkin_date)
    if not valid_date:
        return False, f"Date: {error}"
    
    valid_nights, error = validate_nights(nights)
    if not valid_nights:
        return False, f"Nights: {error}"
    
    valid_visitors, error = validate_visitors(visitors)
    if not valid_visitors:
        return False, f"Visitors: {error}"
    
    return True, None

def mask_pii(phone: str = "", name: str = None) -> dict:
    """Mask personally identifiable information for secure display."""
    if not phone:
        masked_phone = "***"
    else:
        phone_str = str(phone).replace("+91", "").strip()
        if len(phone_str) >= 10:
            masked_phone = phone_str[:0] + "*" * (len(phone_str) - 4) + phone_str[-4:]
        else:
            masked_phone = "*" * len(phone_str)
    
    if not name or len(name.strip()) < 2:
        masked_name = "***"
    else:
        name_parts = name.strip().split()
        masked_parts = []
        for part in name_parts:
            if len(part) <= 2:
                masked_parts.append("*" * len(part))
            else:
                masked_parts.append(part[0] + "*" * (len(part) - 2) + part[-1])
        masked_name = " ".join(masked_parts)
    
    return {"phone": masked_phone, "name": masked_name}

def get_safe_user_data(user: dict) -> dict:
    """Return user data with PII masked for non-admin display."""
    if not user:
        return {}
    return {
        "id": user.get("id"),
        "name": mask_pii(user.get("phone"), user.get("name"))["name"],
        "phone": mask_pii(user.get("phone"), user.get("name"))["phone"],
    }
