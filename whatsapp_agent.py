import os, re, time, requests
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_KEY"))

PHONE_ID = os.getenv("WHATSAPP_PHONE_ID") # from Meta Developer Dashboard
TOKEN = os.getenv("WHATSAPP_TOKEN")

def clean_number(wa_link):
    # wa_link is https://wa.me/234801... -> 234801...
    digits = re.sub(r'\D', '', wa_link)
    if digits.startswith('0'):
        digits = '234' + digits[1:] # auto-fix NG 0 -> 234
    return digits

def send_dm(to, business_name, category):
    # Beacon pitch - change this copy
    msg = f"""Hi {business_name} 👋

Saw your {category} on Google - love the reviews.

Quick question: are you getting online orders from your Google profile? We help {category}s in your area turn Google views into WhatsApp orders in 24hrs.

Want a 2-min demo of how your profile would look?"""

    url = f"https://graph.facebook.com/v20.0/{PHONE_ID}/messages"
    headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": msg}
    }
    r = requests.post(url, headers=headers, json=payload)
    print(r.status_code, r.text)
    return r.ok

def run():
    # only new leads
    resp = supabase.table("leads").select("*").eq("status", "new").limit(10).execute()
    leads = resp.data
    print(f"Found {len(leads)} to DM")

    for lead in leads:
        try:
            to = clean_number(lead["whatsapp"])
            ok = send_dm(to, lead["business_name"], lead["category"])
            if ok:
                supabase.table("leads").update({"status": "contacted"}).eq("id", lead["id"]).execute()
                print(f"✓ DM sent to {lead['business_name']}")
            time.sleep(15) # don't get banned - 15 sec between
        except Exception as e:
            print(f"X failed {lead['business_name']}: {e}")
            time.sleep(5)

if __name__ == "__main__":
    run()