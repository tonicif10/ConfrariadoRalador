import os
import re
import urllib.request
from urllib.parse import urljoin, urlparse

# Base URL of the site
BASE_URL = "https://confrariadoralador.webnode.pt"
OUTPUT_DIR = "images/scraped"

# Ensure output directory exists
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Pages to crawl
PAGES = [
    "/",
    "/vinhos/",
    "/quem-somos/",
    "/estatutos/",
    "/contactos/"
]

# Headers to mimic a browser
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
}

def download_image(img_url):
    try:
        # Generate filename
        parsed_url = urlparse(img_url)
        path = parsed_url.path
        filename = os.path.basename(path)
        
        # Helper to ignore weird query param filenames or empty ones
        if not filename or filename.lower().endswith(('.html', '.php', '/')):
             return

        # Handle duplicates/unwanted
        filepath = os.path.join(OUTPUT_DIR, filename)
        if os.path.exists(filepath):
            return

        print(f"Downloading {img_url}...")
        req = urllib.request.Request(img_url, headers=HEADERS)
        with urllib.request.urlopen(req) as response:
            with open(filepath, 'wb') as f:
                f.write(response.read())
        print(f"Saved: {filename}")
        
    except Exception as e:
        print(f"Failed to download {img_url}: {e}")

def scrape_images():
    seen_urls = set()
    
    for page in PAGES:
        url = urljoin(BASE_URL, page)
        print(f"Scraping {url}...")
        
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req) as response:
                html_content = response.read().decode('utf-8')
                
                # Regex to find img src="..."
                # Matches src="http..." or src="/..."
                img_matches = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html_content)
                
                # Regex for background-image: url(...)
                bg_matches = re.findall(r'background-image:\s*url\([\'"]?([^\'"\)]+)[\'"]?\)', html_content)
                
                all_matches = img_matches + bg_matches
                
                for src in all_matches:
                    # Clean up & Resolve URL
                    src = src.strip()
                    if src.startswith('//'):
                        src = 'https:' + src
                    
                    full_url = urljoin(BASE_URL, src)
                    
                    if full_url not in seen_urls:
                        seen_urls.add(full_url)
                        download_image(full_url)
                        
        except Exception as e:
            print(f"Error scraping {url}: {e}")

if __name__ == "__main__":
    scrape_images()
