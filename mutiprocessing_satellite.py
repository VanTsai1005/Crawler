#!/usr/bin/env python

import multiprocessing
from concurrent.futures import ProcessPoolExecutor
import requests as r
from threading import Thread
from Queue import Queue



def worker():
    while not queue.empty():
        page = queue.get()
        crawler(page)


def crawler(s_total):
    s_year = s_total.split(",")[0]
    ss = s_total.split(",")[1]

    url = base_url1.format(s_year, ss)
    res = r.get(url)
    if res.status_code == 404:
        url = base_url2.format(s_year, ss)
        res = r.get(url)
        if res.status_code == 404:
            url = base_url3.format(s_year, ss)
            res = r.get(url, timeout=timeoutSec)

    if res.status_code == 200:
        filename = path + ss + ".jpg"
        from PIL import Image

        im = Image.open()
        nim = im.crop((2200, 2050, 3200, 2550))
        nim.thumbnail((1000, 800))
        nim.save("/Users/iii/Desktop/croped.jpg")
        nim.show()
        open(filename, 'wb').write(res.content)
        print ss


if __name__ == "__main__":
    NUM_THREADS = 8
    timeoutSec = 6

    yearAry = ["15","16"]
    monthAry = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    base_url1 = "http://agora.ex.nii.ac.jp/digital-typhoon/globe/color/20{}/8192x8192/MTS1{}00.globe.0.jpg"
    base_url2 = "http://agora.ex.nii.ac.jp/digital-typhoon/globe/color/20{}/8192x8192/MTS2{}00.globe.0.jpg"
    base_url3 = "http://agora.ex.nii.ac.jp/digital-typhoon/globe/color/20{}/8192x8192/HMW8{}00.globe.0.jpg"
    path = "/Users/iii/Desktop/imgs/"

    queue = Queue();
    for s_year in yearAry:
        for idx, month_num in enumerate(monthAry):
            if idx+1<7:
                continue
            month = idx + 1
            s_month = "0" + str(idx + 1) if idx + 1 < 10 else str(idx + 1)
            for date in range(month_num):
                s_date = "0" + str(date + 1) if date + 1 < 10 else str(date + 1)
                s_total = s_year + "," + s_year + s_month + s_date
                queue.put(s_total)
    # threads = map(lambda i: Thread(target=worker), xrange(NUM_THREADS))
    # map(lambda th: th.start(), threads)
    # map(lambda th: th.join(), threads)

    cpus = multiprocessing.cpu_count()
    print cpus

    with ProcessPoolExecutor(max_workers=cpus) as executor:
        while not queue.empty():
            page = queue.get()
            executor.submit(crawler,page)





