import threading
import queue
import os 
import hashlib
from urllib.parse import urlparse, urljoin
import requests
from bs4 import BeautifulSoup
import time 


URLS_FILE = 'urls.txt'
OUT_DIR = "images_threads"
N_PAGE_WORKERS = 4 # число потоков, парсящих страницы (N)
M_IMAGE_WORKERS = 4  # число потоков, скачивающих изображения (M)

def safe_filename_url(url):
    parsed = urlparse(url)
    ext = os.path.splitext(parsed.path)[1]
    if not ext:
        # попробуем вытащить расширение из query или поставить .jpg по умолчанию
        ext = ".jpg"
    return hashlib.sha1(url.encode()).hexdigest() + ext


def page_worker(page_q: queue.Queue, image_q: queue.Queue, wid: int):
    session = requests.Session()
    while True:
        url = page_q.get()
        if url is None:
            page_q.task_done()
            print(f"[PAGE-{wid}] Finished")
            break
        print(f"[PAGE-{wid}] Start {url}")
        
        try:
            r = session.get(url, timeout=10)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")
            imgs = set()
            for tag in soup.find_all('img'):
                src = tag.get('src') or tag.get('data-src')
                if not src:
                    continue
                imgs.add(urljoin(url, src))
            print(f"[PAGE-{wid}] Found {len(imgs)} images on {url}")
            for img_url in imgs:
                image_q.put(img_url)
            print(f"[PAGE-{wid}] Finished {url}")
        except Exception as e:
            print(f"[PAGE-{wid}] Error {url}: {e}")
        finally:
            page_q.task_done()
    session.close()
    
def image_worker(image_q: queue.Queue, out_dir: str, wid: int):
    session = requests.Session()
    while True:
        img_url = image_q.get()
        if img_url is None:
            image_q.task_done()
            print(f"[IMG-{wid}] Finished")
            break
        print(f"[IMG-{wid}] Start {img_url}")
        try:
            r = session.get(img_url, timeout=10, stream=True)
            r.raise_for_status()
            ct = r.headers.get('Content-Type', '')
            # Минимальная проверка — содержимое действительно изображение
            if "image" not in ct:
                print(f"[IMG-{wid}] Skipping (not an image): {img_url} (Content-Type: {ct})")
            else:
                os.makedirs(out_dir, exist_ok=True)
                fname = safe_filename_url(img_url)
                path = os.path.join(out_dir, fname)
                with open(path, "wb") as f:
                    for chunk in r.iter_content(8192):
                        if chunk:
                            f.write(chunk)
                print(f"[IMG-{wid}] Downloaded {img_url} to {path}")
        except Exception as e:
            print(f"[IMG-{wid}] Error {img_url}: {e}")
        finally:
            image_q.task_done()
    session.close()        
                
                
              
def main():
    urls = [line.strip() for line in open(URLS_FILE, encoding="utf-8") if line.strip()]
    
    page_q = queue.Queue()
    image_q = queue.Queue()
    
    # стартуем workers
    page_threads = []
    for i in range(N_PAGE_WORKERS):
        t = threading.Thread(target=page_worker, args=(page_q, image_q, i), daemon=True)
        t.start()
        page_threads.append(t)

    image_threads = []
    for i in range(M_IMAGE_WORKERS):
        t = threading.Thread(target=image_worker, args=(image_q, OUT_DIR, i), daemon=True)
        t.start()
        image_threads.append(t)
        
    # кладём задачи (страницы)    
    for u in urls:
        page_q.put(u)
        
        
    for _ in range(N_PAGE_WORKERS):
        page_q.put(None)
    
    # дождёмся что все страницы обработаны    
    page_q.join()
    print("All pages processed")
    
    for _ in range(M_IMAGE_WORKERS):
        image_q.put(None)
    
    # ждём пока все изображения будут скачаны    
    image_q.join()
    print("All images downloaded")
    
    for t in page_threads:
        t.join()
    for t in image_threads:
        t.join()
    
    print("Done")
    
if __name__ == "__main__":
    start = time.perf_counter()
    main()
    print("Elapsed:", time.perf_counter() - start)
        