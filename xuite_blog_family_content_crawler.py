# !coding:utf-8
import requests as r
from bs4 import BeautifulSoup as bs
from Queue import Queue
from threading import Thread
from datetime import datetime
import json

NUM_THREADS = 8
aList = []
bList = []
queue = Queue()
with open("E:/urls_B&B.txt","r") as f:
    for line in f.readlines():
        bList.append(line)

def crawler(url):
    res = r.get(url)
    soup = bs(res.text, "lxml")
    dict = {
        "title":"",
        "area":"",
        "auth":"",
        "date":"",
        "resp":"",
        "content":"",
        "tags":""
    }
    if soup.select_one("h2.title"):
        dict["title"] = soup.select_one("h2.title").select_one("span.titlename").text
        dict["date"] = soup.select_one("h2.title").select_one("span.titledate-year").text + "/" + soup.select_one("h2.title").\
                      select_one("span.titledate-month").text + "/" + soup.select_one("h2.title").select_one("span.titledate-day").text
    if soup.select_one("#clouddiv"):
        tagText = ""
        tags = soup.select_one("#clouddiv").select("a.cloud_css")
        for tag in tags:
            tagText += tag.text+","
        dict["tags"] = tagText

    if soup.select_one("h1.blogname"):
        dict["auth"] = soup.select_one("h1.blogname").text

    if soup.select_one("#content_all"):
        dict["content"] = soup.select_one("#content_all").text
    if soup.select_one("Detailinner"):
        dict["content"] = soup.select_one("#Detailinner").text

    aList.append(dict)
    print len(aList)

def worker():
    while not queue.empty():
        sText=queue.get()
        crawler(sText)

for i in range(0,15):
    aList = []
    queue = Queue();

    beginPage = 1+500*i
    endPage = 501+500*i

    for j in range(beginPage,endPage):
        if j == len(bList):
            break
        queue.put(bList.__getitem__(j))

    s1 = datetime.now()
    try:
        #設定THREAD數量及執行的FUNCTION
        threads = map(lambda k: Thread(target=worker), xrange(NUM_THREADS))
        #啟動THREAD
        map(lambda th: th.start(), threads)
        map(lambda th: th.join(), threads)
    except:
        print "thread error"
    finally:
        s2 = datetime.now()
        encodedjson = json.dumps(aList, ensure_ascii=False)
        with open("E:\\xuite_blog_"+str(endPage)+".json", "w") as f:
            f.write(encodedjson.encode("utf-8"))
            f.close()
        print "All - "+str(i)+" Finish "+str(s2-s1)+"!!"