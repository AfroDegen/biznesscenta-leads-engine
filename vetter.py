def score_lead(place):
    """Score 0-6, higher = worse = better lead for you"""
    score = 0
    details = place.get("details", {})
    
    photos = len(details.get("photos", []))
    if photos <= 3: score += 2
    elif photos <= 5: score += 1

    reviews = details.get("user_ratings_total", 0)
    if reviews == 0: score += 2
    elif reviews <= 10: score += 1

    if not details.get("website"): score += 1
    if not details.get("formatted_phone_number"): score += 1

    return score, photos, reviews

def is_vetted(place):
    score, photos, reviews = score_lead(place)
    # We want BAD GBPs, score >=3
    return score >= 3, score