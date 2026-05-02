from bs4 import BeautifulSoup
import requests
import time

def extract_attributes(url: str):
    start_time = time.time()
    try:
        response = requests.get(url, timeout=10)
        load_time = round((time.time() - start_time) * 1000) # ms
        soup = BeautifulSoup(response.text, 'html.parser')

        # Title
        title = soup.title.string if soup.title else None

        # Meta Description
        meta_desc = None
        meta = soup.find('meta', attrs={'name': 'description'})
        if meta:
            meta_desc = meta.get('content')
        
        # H1, H2
        h1_count = len(soup.find_all('h1'))
        h2_count = len(soup.find_all('h2'))

        # Word count (very basic approximation)
        text = soup.get_text()
        word_count = len(text.split())

        # Links
        internal_links = 0
        external_links = 0
        # TODO: Logic to differentiate internal/external (needs base domain) -> For now just count all
        # We will refine this in the main logic by passing domain
        
        # Images
        images = soup.find_all('img')
        missing_alt = sum(1 for img in images if not img.get('alt'))

        # Tech SEO
        canonical = soup.find('link', attrs={'rel': 'canonical'})
        canonical_href = canonical['href'] if canonical else None
        
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        mobile_friendly = True if viewport else False

        # Return dict
        return {
            "url": url,
            "title": title,
            "meta_description": meta_desc,
            "h1_count": h1_count,
            "h2_count": h2_count,
            "word_count": word_count,
            "total_links": len(soup.find_all('a')), # Placeholder
            "image_count": len(images),
            "missing_alt": missing_alt,
            "canonical": canonical_href,
            "mobile_friendly": mobile_friendly,
            "load_time_ms": load_time
        }

    except Exception as e:
        return {"error": str(e)}
