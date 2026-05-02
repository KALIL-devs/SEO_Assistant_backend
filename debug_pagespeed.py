
import os
import sys
import json
import requests

# Add backend directory to sys.path
sys.path.append(os.path.abspath('e:/SEO_ASSISTANT/SEO_Assistant/backend'))

from dotenv import load_dotenv
load_dotenv(os.path.abspath('e:/SEO_ASSISTANT/SEO_Assistant/backend/.env'))

from services.pagespeed import run_audit

# Test with a high-traffic site that definitely has field data
TEST_URL = "https://www.google.com"

print(f"Running PageSpeed audit for {TEST_URL}...")

try:
    # We call run_audit directly. 
    # Note: This will use the logic in services/pagespeed.py
    result = run_audit(TEST_URL, 'mobile')
    
    print("\n--- Extracted Core Web Vitals ---")
    print(json.dumps(result.get('core_web_vitals'), indent=2))
    
    print("\n--- Extracted Distributions ---")
    print(json.dumps(result.get('cwv_distributions'), indent=2))
    
    print("\n--- Raw API Checks ---")
    # We can't easily see the raw API response from here unless we modify the code or mock requests.
    # But seeing the output will tell us if extraction is working.
    
    if result.get('cwv_distributions') and result.get('cwv_distributions').get('LCP'):
        print("SUCCESS: LCP Distribution found.")
    else:
        print("FAILURE: LCP Distribution MISSING.")

except Exception as e:
    print(f"Error during audit: {e}")
