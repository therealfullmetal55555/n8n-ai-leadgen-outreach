#!/usr/bin/env python3
"""
Local offline simulation of the lead generation & outreach pipeline.
Demonstrates the sequence executed by n8n Code Nodes without making live external network calls.
"""

import csv
import json
import re
import time
from pathlib import Path

BASE_DIR = Path(__file__).parent
CSV_PATH = BASE_DIR / "demo-data" / "leads-sample.csv"

# Mock HTML payloads for offline dry-run simulation
MOCK_PAGES = {
    1: {
        "title": "BrightSmile Dental Care - Austin Family Dentist",
        "html": """
        <html>
          <head><title>BrightSmile Dental Care - Austin Family Dentist</title></head>
          <body>
            <h1>Family & Cosmetic Dentistry in Austin</h1>
            <p>Dr. Marcus Vance and team offer comprehensive dental care.</p>
            <div class="booking-notice">
              Please call our front desk during office hours (Mon-Fri 9 AM - 5 PM) at (512) 555-0199 to schedule your appointment.
            </div>
          </body>
        </html>
        """
    },
    2: {
        "title": "Apex Pediatric Dentistry Seattle",
        "html": """
        <html>
          <head><title>Apex Pediatric Dentistry Seattle</title></head>
          <body>
            <h1>Fun Dental Visits for Kids</h1>
            <p>Specialized pediatric dental clinic in Seattle.</p>
            <div class="contact-box">
              Fill out our contact form below. Expect a reply within 2-3 business days.
            </div>
          </body>
        </html>
        """
    },
    3: {
        "title": "Harbor View Dental Studio - Dental Implants",
        "html": """
        <html>
          <head><title>Harbor View Dental Studio</title></head>
          <body>
            <h1>Premium Dental Implants in San Diego</h1>
            <p>Restore your smile with permanent dental implants.</p>
            <p>Pricing inquiries: Send an email to info@harborviewstudio-test.com. We do not have instant pricing or live chat on our website.</p>
          </body>
        </html>
        """
    }
}

def clean_html(raw_html: str) -> str:
    """Strip scripts, styles, and HTML tags using regex heuristics."""
    text = re.sub(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>', ' ', raw_html, flags=re.IGNORECASE)
    text = re.sub(r'<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>', ' ', text, flags=re.IGNORECASE)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def detect_clinic_gaps(clean_text: str) -> str:
    """Analyze text for operational friction points using regex heuristics."""
    lower = clean_text.lower()
    
    has_online_booking = bool(re.search(r'(book\s*online|instant\s*booking|schedule\s*appointment|calendly|zocdoc|janeapp)', lower))
    has_phone_only = bool(re.search(r'(call\s*us|call\s*during\s*office|call\s*our\s*front\s*desk|leave\s*a\s*voicemail)', lower)) and not has_online_booking
    has_slow_form = bool(re.search(r'(2-3\s*business\s*days|within\s*48\s*hours|reply\s*shortly)', lower))
    
    if has_phone_only:
        return "Clinic relies strictly on phone calls during office hours; lacks instant 24/7 online scheduling for after-hours patient inquiries."
    elif has_slow_form:
        return "Contact form has a multi-day response lag (2-3 business days), risking patient drop-off to competing local clinics."
    elif not has_online_booking:
        return "No instant self-service booking or 24/7 interactive triage chat for high-urgency dental cases."
    return "Lacks automated insurance FAQ verification widget."

def generate_simulated_pitch(lead: dict, gap: str) -> str:
    """Generate pitch text from local template for simulation."""
    first_name = lead['contact_name'].split()[1] if len(lead['contact_name'].split()) > 1 else lead['contact_name']
    
    if "phone calls during office hours" in gap:
        return f"Hi {first_name}, I noticed {lead['company_name']} currently requires patients to call during office hours to book visits. Adding a 24/7 AI booking assistant would capture high-intent after-hours patients automatically without adding front-desk overhead."
    elif "multi-day response lag" in gap:
        return f"Hi {first_name}, I saw that inquiries on {lead['company_name']}'s site take 2-3 business days for a reply. An automated intake bot could instantly qualify insurance and schedule appointments on the spot, preventing patient churn."
    else:
        return f"Hi {first_name}, I noticed {lead['company_name']} doesn't have instant online scheduling for emergency inquiries. An AI patient triage agent could capture urgent cases 24/7 and route them straight to your chair calendar."

def run_simulation():
    print("=" * 80)
    print("LEADGEN & OUTREACH PIPELINE - LOCAL SIMULATION (OFFLINE DRY-RUN)")
    print("=" * 80)
    
    with open(CSV_PATH, mode='r', encoding='utf-8') as f:
        reader = list(csv.DictReader(f))
    
    sample_leads = reader[:3]
    
    for idx, lead in enumerate(sample_leads, 1):
        lead_id = int(lead['id'])
        print(f"\n[{idx}/{len(sample_leads)}] Processing Lead #{lead_id}: {lead['company_name']} ({lead['city']})")
        print(f"  Contact: {lead['contact_name']} ({lead['contact_title']}) | {lead['contact_email']}")
        print(f"  Target URL: {lead['website_url']}")
        
        # Step 1: Simulated rate limiting
        print("  [Step 1] Rate limit: 1s delay simulated...")
        time.sleep(0.5)
        
        # Step 2: Scrape & Extract
        mock_data = MOCK_PAGES.get(lead_id, {"title": lead['company_name'], "html": "<html><body>Default Clinic Info</body></html>"})
        cleaned = clean_html(mock_data['html'])
        print(f"  [Step 2] HTML text extracted ({len(cleaned)} characters)")
        
        # Step 3: Gap Detection
        gap = detect_clinic_gaps(cleaned)
        print(f"  [Step 3] Detected Gap: {gap}")
        
        # Step 4: Template-based Simulated Pitch
        pitch = generate_simulated_pitch(lead, gap)
        word_count = len(pitch.split())
        
        # Step 5: Estimated Cost Telemetry
        prompt_tokens = 215
        completion_tokens = 42
        cost_usd = (prompt_tokens / 1_000_000 * 0.150) + (completion_tokens / 1_000_000 * 0.600)
        
        print(f"  [Step 4] Pitch generated (Illustrative example, local simulation):")
        print(f"     \"{pitch}\"")
        print(f"  [Step 5] Estimated Telemetry: {word_count} words | Estimated Cost: ${cost_usd:.6f} USD")
        print(f"  [Step 6] Dispatched to Telegram preview & Google Sheets CRM log.")
        print("-" * 80)

if __name__ == "__main__":
    run_simulation()
