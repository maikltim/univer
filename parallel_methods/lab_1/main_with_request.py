import os 
import hashlib
from urllib.parse import urlparse, urljoin
import requests
from bs4 import BeautifulSoup


URLS_FILE = 'urls.txt'
OUT_DIR = "images_seq"

def safefilename_from_url(url):
    parsed = urlparse(url)
    ext = os.path.splitext(parsed.path)[1] or ".jpg"
    return hashlib.sha1(url.encode('utf-8')).hexdigest() + ext


def download_image(img_url, out_dir):
    print(f"      [IMG] Start {img_url}")
    try:
        r = requests.get(img_url, timeout=10, stream=True)
        r.raise_for_status()
        filename = safefilename_from_url(img_url)
        path = os.path.join(out_dir, filename)
        os.makedirs(out_dir, exist_ok=True)
        with open(path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print(f"      [IMG] Downloaded {img_url} to {path}")
    except Exception as e:
        print(f"      [IMG] Error {img_url}: {e}")
        return
    
def process_pager(url, out_dir):
    print(f"[PAGE] Start {url}")
    try:
        r = requests.get(url ,timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        imgs = set()
        for tag in soup.find_all("img"):
            src = tag.get("src") or tag.get("data-src")
            if src:
                imgs.add(urljoin(url, src))
        print(f"      [PAGE] Found {len(imgs)} images on {url}")
        for img in imgs:
            download_image(img, out_dir)
        print(f"[PAGE] Finished {url}")
    except Exception as e:
        print(f"[PAGE] Error {url}: {e}")
        
        
if __name__ == "__main__":
    urls = [line.strip() for line in open(URLS_FILE, encoding="utf-8") if line.strip()]
    
    for u in urls:
        process_pager(u, OUT_DIR)
    print("Done")