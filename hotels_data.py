"""
hotels_data.py
Provides a HOTELS list in the format expected by the codebase.
The file converts an internal static list into the expected keys (string ids like 'h1' and price_per_night).
"""
HOTELS = [
    {"id": f"h{i+1}", "name": v["name"], "area": v["area"], "price_per_night": v["price"], "rating": v["rating"], "amenities": v["amenities"]}
    for i, v in enumerate([
        {"name":"Radisson Blu Hotel Nagpur","area":"Wardha Road","price":5200,"rating":4.6,"amenities":"Pool, WiFi, Parking, Bar"},
        {"name":"Le Méridien Nagpur","area":"Wardha Road","price":5800,"rating":4.7,"amenities":"Pool, Gym, Spa, Restaurant"},
        {"name":"The Pride Hotel Nagpur","area":"Wardha Road","price":4500,"rating":4.3,"amenities":"WiFi, Parking, Restaurant"},
        {"name":"Tuli Imperial","area":"Ramdas Peth","price":4000,"rating":4.1,"amenities":"WiFi, Dining, Bar"},
        {"name":"Tuli International","area":"Central Avenue","price":4200,"rating":4.0,"amenities":"WiFi, Parking"},
        {"name":"Hotel Centre Point","area":"Ramdaspeth","price":3900,"rating":4.3,"amenities":"WiFi, Parking, Restaurant"},
        {"name":"Urban Hermitage","area":"Wardha Road","price":3500,"rating":4.2,"amenities":"WiFi, Parking"},
        {"name":"The Majestic Manor","area":"Somalwada","price":2900,"rating":4.0,"amenities":"WiFi, Restaurant"},
        {"name":"Hotel Hardeo","area":"Sitabuldi","price":2700,"rating":4.0,"amenities":"WiFi, Parking"},
        {"name":"Hotel Orient Grand","area":"Sitabuldi","price":2600,"rating":3.9,"amenities":"WiFi, AC"},
        {"name":"Hotel Dwarkamai","area":"Central Avenue","price":2500,"rating":4.2,"amenities":"WiFi, Parking"},
        {"name":"Mango Hotels Nagpur","area":"Sitabuldi","price":2800,"rating":4.0,"amenities":"WiFi, Restaurant"},
        {"name":"Tristar Hotel","area":"Dhantoli","price":2600,"rating":3.8,"amenities":"WiFi"},
        {"name":"Hotel President","area":"Sadar","price":2400,"rating":3.9,"amenities":"WiFi, Restaurant"},
        {"name":"Hotel Girija","area":"Sadar","price":2200,"rating":3.8,"amenities":"WiFi"},
        {"name":"Hotel Vrandavan","area":"Dharampeth","price":2300,"rating":4.0,"amenities":"WiFi, AC"},
        {"name":"Hotel Blue Diamond","area":"Sadar","price":2100,"rating":3.7,"amenities":"WiFi"},
        {"name":"Hotel Rahul","area":"Sitabuldi","price":2000,"rating":3.7,"amenities":"WiFi"},
        {"name":"Hotel Rahul Deluxe","area":"Central Avenue","price":2100,"rating":3.6,"amenities":"WiFi, Parking"},
        {"name":"Hotel Lotus Inn","area":"Manish Nagar","price":2200,"rating":4.1,"amenities":"WiFi, Parking"},
        {"name":"Hotel Airport Centre Point","area":"Sonegaon","price":3600,"rating":4.2,"amenities":"WiFi, Restaurant"},
        {"name":"Krishnum Residency","area":"Manish Nagar","price":1900,"rating":3.9,"amenities":"WiFi, AC"},
        {"name":"Hotel Gokul","area":"Sadar","price":1800,"rating":3.7,"amenities":"WiFi"},
        {"name":"Hotel Sun City","area":"Sadar","price":1700,"rating":3.6,"amenities":"WiFi"},
        {"name":"Hotel Dwarkesh","area":"Gandhibagh","price":1600,"rating":3.8,"amenities":"WiFi"},
        {"name":"Hotel Parashar","area":"Gandhibagh","price":1700,"rating":3.9,"amenities":"WiFi"},
        {"name":"Hotel Pritam","area":"Sitabuldi","price":1500,"rating":3.5,"amenities":"WiFi"},
        {"name":"Hotel City Centre","area":"Sitabuldi","price":1800,"rating":3.7,"amenities":"WiFi, AC"},
        {"name":"Hotel Amrta","area":"Railway Station Road","price":1900,"rating":3.8,"amenities":"WiFi"},
        {"name":"Hotel Royale Heritage","area":"Central Avenue","price":2000,"rating":3.9,"amenities":"WiFi, Parking"},
        # ... for brevity the remainder is omitted; you can add all entries as needed
    ])
]

__all__ = ["HOTELS"]
