#!/usr/bin/env python

from PIL import Image
from os import listdir
from concurrent.futures import ProcessPoolExecutor
from Queue import Queue
import multiprocessing


def crop_to(item):
    try:
        filename = path + item;
        im = Image.open(filename)
        nim = im.crop((2200,2050,3200,2550))
        nim.thumbnail( (1000,800) )
        nim.save( path1 + item )
        # nim.show()
        print item
    except:
        pass

if __name__ == "__main__":
    path = "/home/ubuntu/upload/img/"
    path1 = "/home/ubuntu/upload/imgs/"

    queue = Queue()

    for item in listdir(path):
        queue.put(item)

    cpus = multiprocessing.cpu_count()
    print cpus

    with ProcessPoolExecutor(max_workers=cpus) as executor:
        while not queue.empty():
            item = queue.get()
            executor.submit(crop_to,item)