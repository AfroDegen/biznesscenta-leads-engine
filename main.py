import os, time
import googlemaps
from supabase import create_client
from dotenv import load_dotenv
from config import CLUSTERS, DAILY_TARGET
from vetter import is_vetted

load_dotenv()
gmaps = googlemaps.Client(key=os.getenv("GOOGLE_MAPS_API_KEY"))
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_KEY"))

def run():
    leads_today = []
    for cluster in CLUSTERS:
        resp = gmaps.places_nearby(
            location=(cluster["lat"], cluster["lng"]),
            radius=cluster["radius"],
            keyword=cluster["category"]
        )
        
        for place in resp.get("results", []):
            if len(leads_today) >= DAILY_TARGET: 
                break
            
            details = gmaps.place(
                place_id=place["place_id"], 
                fields=["name","formatted_address","formatted_phone_number","website","photo","user_ratings_total","rating","url"]
            )["result"]
            
            vetted, score = is_vetted({"details": details})
            if not vetted: 
                continue

            phone = details.get("formatted_phone_number","").replace(" ","").replace("-","")
            whatsapp = f"https://wa.me/{phone}" if phone else None
            if not whatsapp:
                continue  # skip if no phone - you need whatsapp to sell

            exists = supabase.table("leads").select("id").eq("gbp_link", details.get("url")).execute()
            if exists.data: 
                continue

            lead = {
                "place_id": place["place_id"],
                "state": cluster["state"],
                "category": cluster["category"],
                "business_name": details.get("name"),
                "gbp_link": details.get("url"),
                "whatsapp": whatsapp,
                "gbp_score": score,
                "status": "new",
                "notes": f"{details.get('user_ratings_total',0)} reviews, rating {details.get('rating')}"
            }
            supabase.table("leads").insert(lead).execute()
            leads_today.append(lead)
            print(f"+ {lead['business_name']} - Score {score}")
            time.sleep(0.5)

    print(f"DONE: {len(leads_today)} vetted leads today")

if __name__ == "__main__":
    run()