CLUSTERS = [
    {"state": "Lagos", "category": "beauty salon", "lat": 6.5244, "lng": 3.3792, "radius": 20000},
    {"state": "Lagos", "category": "restaurant", "lat": 6.5244, "lng": 3.3792, "radius": 20000},
    {"state": "Abuja", "category": "hair salon", "lat": 9.0765, "lng": 7.3986, "radius": 15000},
    {"state": "Abuja", "category": "hotel", "lat": 9.0765, "lng": 7.3986, "radius": 15000},
    {"state": "Rivers", "category": "spa", "lat": 4.8156, "lng": 7.0498, "radius": 15000},
    {"state": "Oyo", "category": "restaurant", "lat": 7.3775, "lng": 3.9470, "radius": 10000},
    {"state": "Kano", "category": "fashion store", "lat": 12.0022, "lng": 8.5920, "radius": 10000},
    {"state": "Anambra", "category": "beauty salon", "lat": 6.2209, "lng": 7.0821, "radius": 10000},
]

# VETTING RULES - What is a "poor GBP"
VETTING = {
    "max_photos": 5,      # Less than 5 photos = poor
    "max_reviews": 10,    # Less than 10 reviews = poor
    "min_rating": 4.0,    # Below 4.0 = poor and needs help
}
DAILY_TARGET = 50