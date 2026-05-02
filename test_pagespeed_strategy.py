
import os
import sys

# Add backend directory to sys.path
sys.path.append(os.path.abspath('e:/SEO_ASSISTANT/SEO_Assistant/backend'))

from services.pagespeed import run_audit
from dotenv import load_dotenv

load_dotenv(os.path.abspath('e:/SEO_ASSISTANT/SEO_Assistant/backend/.env'))

print("Testing Mobile Strategy...")
try:
    res_mobile = run_audit('https://example.com', 'mobile')
    print(f"Mobile Strategy Result: {res_mobile.get('strategy')}")
except Exception as e:
    print(f"Mobile failed: {e}")

print("\nTesting Desktop Strategy...")
try:
    res_desktop = run_audit('https://example.com', 'desktop')
    print(f"Desktop Strategy Result: {res_desktop.get('strategy')}")
except Exception as e:
    print(f"Desktop failed: {e}")
