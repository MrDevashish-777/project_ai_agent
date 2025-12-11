# models.py
from pydantic import BaseModel
from typing import Optional, List

class ChatRequest(BaseModel):
    user_id: Optional[str] = None
    message: str

class ChatResponse(BaseModel):
    reply: str
    suggestions: Optional[List[dict]] = None

class BookingRequest(BaseModel):
    user_id: Optional[str] = None
    name: str
    phone: str
    hotel_id: str
    checkin_date: str
    nights: int
    visitors: int = 1

class User(BaseModel):
    id: Optional[str]
    name: Optional[str]
    phone: Optional[str]
