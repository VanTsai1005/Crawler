#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import requests as r
from bs4 import BeautifulSoup as bs
from datetime import datetime
from Queue import Queue
from threading import Thread

def getContent(linkUrl) :
    res1 = r.get(linkUrl)
    soup1 = bs(res1.text,"lxml")
    content1 = soup1.select_one("#main-content").text.strip()
    return content1

NUM_THREADS = 8
s1 = datetime.now()

originUrl = "http://www.ptt.cc"
firstURL = "https://www.ptt.cc/bbs/BabyMother/index.html"
baseUrl = "https://www.ptt.cc/bbs/BabyMother/index{}.html"
res = r.get(firstURL)
soup = bs(res.text,"lxml")
pageNo =  int(soup.select_one(".btn-group-paging").select("a")[1]["href"].split("index")[1].split(".h")[0])+1
#pageNo = 50

queue = Queue();
for i in range(1,pageNo):
    queue.put(i)

aList=[]

def worker():
    while not queue.empty():
        page=queue.get()
        print page
        crawler(page)

def crawler(page):
    url =baseUrl.format(page)
    res = r.get(url)
    soup = bs(res.text,"lxml")
    articles = soup.select(".r-ent")
    article_dict = {
        "title":"",
        "catogory":"",
        "nrec":"",
        "date":"",
        "author":"",
        "content":""
    }

    for article in articles:
        try:
            s = article.select_one("a").text;
            tmpUrl = article.select_one("a")["href"]
            contentUrl = originUrl+tmpUrl

            article_dict["title"] = s.split("]")[1].strip()
            article_dict["catogory"] = s.split("]")[0].split("[")[1].strip()
            article_dict["nrec"] = article.select_one("div.nrec").select_one("span").text.strip()
            article_dict["date"] = article.select_one("div.date").text.strip()
            article_dict["author"] = article.select_one("div.author").text.strip()
            article_dict["content"] = getContent(contentUrl)

            aList.append(article_dict)
        except:
            pass

s1 = datetime.now()
# 設定THREAD數量及執行的FUNCTION
threads = map(lambda i: Thread(target=worker), xrange(NUM_THREADS))
#啟動THREAD
map(lambda th: th.start(), threads)
map(lambda th: th.join(), threads)
s2 = datetime.now()

encodedjson = json.dumps(aList,ensure_ascii=False)
with open("E:\\test.json", "w") as f:
    f.write(encodedjson.encode("utf-8"))
    f.close()

print "All  Finish "+str(s2-s1)+"!!"








