import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import xml.etree.ElementTree as ET

# Pretend to be a browser to avoid some WAF blocks
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def fetch_sitemap_pages(base_url: str) -> list[str]:
    """
    Attempts to find sitemap.xml and extract pages.
    Fallback to crawling homepage links if sitemap not found.
    """
    # Ensure base_url has scheme
    if not base_url.startswith("http"):
        base_url = "https://" + base_url

    # 1. Try sitemap.xml
    sitemap_url = urljoin(base_url, "sitemap.xml")
    try:
        response = requests.get(sitemap_url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            # Check content size/type before parsing to avoid massive files
            if len(response.content) > 5 * 1024 * 1024: # 5MB limit
                print("Sitemap too large, skipping")
                raise Exception("Sitemap too large")
                
            # Parse XML
            root = ET.fromstring(response.content)
            # Handle default namespace dynamically if possible, or just ignore namespaces by using local-name() in xpath if ET supported it more robustly.
            # Simple approach: strip namespaces or try both with/without
            
            # Simple namespace strip for parsing
            urls = []
            for elem in root.iter():
                if 'url' in elem.tag:
                    # Find loc child
                    for child in elem:
                        if 'loc' in child.tag and child.text:
                            urls.append(child.text)
            
            if urls:
                return list(set(urls))[:20] # Unique and limit
    except Exception as e:
        print(f"Sitemap error: {e}")

    # 2. Fallback: Simple extraction from homepage
    try:
        response = requests.get(base_url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = set()
        parsed_base = urlparse(base_url)
        domain = parsed_base.netloc
        
        # Also add the base url itself if it's reachable
        links.add(base_url)

        for a in soup.find_all('a', href=True):
            href = a['href']
            # Handle relative URLs
            full_url = urljoin(base_url, href)
            parsed = urlparse(full_url)
            
            # Same domain only
            if parsed.netloc == domain and parsed.scheme in ['http', 'https']:
                # Filter out basics
                if not any(ext in parsed.path.lower() for ext in ['.jpg', '.png', '.pdf', '.css', '.js']):
                    links.add(full_url)
                    
        return list(links)[:20]
    except Exception as e:
        print(f"Crawl error: {e}")
        return [base_url] # At least return the entered URL if crawl fails
