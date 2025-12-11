from pydantic import BaseModel, Field
from typing import Optional, List

class ChatRequest(BaseModel):
    user_id: Optional[str] = None
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    reply: str
    suggestions: Optional[List[dict]] = None
    meta: Optional[dict] = None

class BookingRequest(BaseModel):
    user_id: Optional[str] = None
    name: str
    phone: str
    hotel_id: str
    checkin_date: str
    nights: int
    visitors: int = 1

class InternalSearchHotelsRequest(BaseModel):
    max_price: Optional[int] = None
    location: Optional[str] = None
    min_rating: Optional[float] = None
    amenities: Optional[List[str]] = None
    checkin_date: Optional[str] = None
    nights: Optional[int] = None
    limit: int = 5

class InternalBookHotelRequest(BaseModel):
    user_id: str
    name: str
    phone: str
    hotel_id: str
    checkin_date: str
    nights: int
    visitors: int
    payment_intent_id: Optional[str] = None

class CreatePaymentIntentRequest(BaseModel):
    amount_inr: int = Field(..., gt=0)
    currency: str = "INR"
    description: Optional[str] = None
    booking_id: Optional[str] = None

class GenerateInvoiceRequest(BaseModel):
    booking_id: str
    gst_percent: float = 18.0

class AdminLoginRequest(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: Optional[str]
    name: Optional[str]
    phone: Optional[str]
