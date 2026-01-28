import re
import sys

def extract_images(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Regex to find links ending in image extensions, case insensitive
    urls = re.findall(r'(https?://[^"\s<>]+\.(?:jpg|jpeg|png|gif|webp))', content, re.IGNORECASE)
    
    unique_urls = sorted(list(set(urls)))
    for url in unique_urls:
        print(url)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        extract_images(sys.argv[1])
