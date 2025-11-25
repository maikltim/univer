# mpi_downloader.py
"""
MPI версия задания: master/worker динамическая раздача URL.
Запуск: mpiexec -n <P> python mpi_downloader.py
Требует: mpi4py, requests, beautifulsoup4
"""

import os
import hashlib
import time
from urllib.parse import urljoin, urlparse

from mpi4py import MPI
import requests
from bs4 import BeautifulSoup

URLS_FILE = "urls.txt"
OUT_DIR = "mpi_images"
TIMEOUT = 10

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

MASTER = 0
TAG_TASK = 1
TAG_DONE = 2
TAG_STATUS = 3

def safe_filename_from_url(url):
    parsed = urlparse(url)
    ext = os.path.splitext(parsed.path)[1]
    if not ext:
        ext = ".jpg"
    return hashlib.sha1(url.encode()).hexdigest() + ext

def download_image(img_url, out_dir):
    try:
        r = requests.get(img_url, timeout=TIMEOUT, stream=True)
        r.raise_for_status()
        ct = r.headers.get("Content-Type","")
        if "image" not in ct:
            return False, f"Not image (Content-Type: {ct})"
        os.makedirs(out_dir, exist_ok=True)
        fname = safe_filename_from_url(img_url)
        path = os.path.join(out_dir, fname)
        with open(path, "wb") as f:
            for chunk in r.iter_content(8192):
                if chunk:
                    f.write(chunk)
        return True, path
    except Exception as e:
        return False, str(e)

def process_page(url, out_dir):
    """Скачивает страницу, парсит img и скачивает каждое изображение
    """
    imgs_found = 0
    imgs_dl = 0
    errors = []
    try:
        r = requests.get(url, timeout=TIMEOUT)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        imgs = set()
        for tag in soup.find_all("img"):
            src = tag.get("src')") if False else (tag.get("src") or tag.get("data-src"))
            if not src:
                continue
            imgs.add(urljoin(url, src))
        imgs_found = len(imgs)
        for img in imgs:
            ok, info = download_image(img, out_dir)
            if ok:
                imgs_dl += 1
            else:
                errors.append((img, info))
    except Exception as e:
        errors.append(("page_error", str(e)))
    return imgs_found, imgs_dl, errors

def master():
    # читаем urls
    with open(URLS_FILE, encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]
    n_urls = len(urls)
    n_workers = size - 1
    print(f"[MASTER] Read {n_urls} URLs. Starting distribution to {n_workers} workers.")

    # индекс следующей задачи для выдачи
    next_idx = 0
    done_sent = 0
    stats = {"pages":0, "images_found":0, "images_dl":0, "errors":0}
    status = MPI.Status()

    # 1) initial dispatch: раздать по одной задаче каждому воркеру (или None, если задач меньше)
    for worker_rank in range(1, size):
        if next_idx < n_urls:
            comm.send(urls[next_idx], dest=worker_rank, tag=TAG_TASK)
            next_idx += 1
        else:
            # если задач уже нет — сразу посылаем DONE
            comm.send(None, dest=worker_rank, tag=TAG_DONE)
            done_sent += 1

    # 2) теперь в цикле ждём отчёты; как придёт отчёт — даём следующую задачу этому воркеру
    while done_sent < n_workers:
        # ждём отчёт от любого воркера (report должен быть словарём)
        msg = comm.recv(source=MPI.ANY_SOURCE, tag=TAG_STATUS, status=status)
        src = status.Get_source()

        if isinstance(msg, dict) and msg.get("report"):
            r = msg
            stats["pages"] += 1
            stats["images_found"] += r.get("images_found", 0)
            stats["images_dl"] += r.get("images_dl", 0)
            stats["errors"] += len(r.get("errors", []))
            print(f"[MASTER] Report from worker {src}: page done, found {r.get('images_found',0)}, dl {r.get('images_dl',0)}, errs {len(r.get('errors',[]))}")

            # отправляем следующую задачу или DONE если задач больше нет
            if next_idx < n_urls:
                comm.send(urls[next_idx], dest=src, tag=TAG_TASK)
                next_idx += 1
            else:
                comm.send(None, dest=src, tag=TAG_DONE)
                done_sent += 1
        else:
            # неожиданные сообщения логируем (на случай ошибок)
            print(f"[MASTER] Unexpected message from {src}: {msg}")

    # все воркеры получили DONE и вышли
    print("[MASTER] All workers finished.")
    print("[MASTER] Summary:", stats)


def worker():
    my_out = os.path.join(OUT_DIR, f"rank_{rank}")
    os.makedirs(my_out, exist_ok=True)
    status = MPI.Status()

    while True:
        # получаем задачу (разуная метка — TAG_TASK или TAG_DONE)
        task = comm.recv(source=MASTER, tag=MPI.ANY_TAG, status=status)
        tag = status.Get_tag()

        if tag == TAG_DONE or task is None:
            print(f"[WORKER {rank}] Received DONE, exiting.")
            break

        url = task
        print(f"[WORKER {rank}] Start processing {url}")

        # process page и скачивание картинок
        imgs_found, imgs_dl, errors = process_page(url, my_out)

        # отправляем отчёт мастеру (словарь)
        report = {"report": True, "images_found": imgs_found, "images_dl": imgs_dl, "errors": errors}
        # Для видимости логируем отправку
        print(f"[WORKER {rank}] Sending report for {url}: found {imgs_found}, dl {imgs_dl}, errs {len(errors)}")
        comm.send(report, dest=MASTER, tag=TAG_STATUS)

    print(f"[WORKER {rank}] Exiting.")


if __name__ == "__main__":
    if size < 2:
        if rank == MASTER:
            print("Need at least 2 MPI ranks: 1 master + 1 worker")
    else:
        if rank == MASTER:
            master()
        else:
            worker()
