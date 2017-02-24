#!/usr/bin/python
#!coding:utf-8
#
# import requests as r
from bs4 import BeautifulSoup as bs
from threading import Thread
from Queue import Queue
from datetime import datetime
import json

queue = Queue();
NUM_THREADS = 8
baseUrl = "https://www.abic.com.tw"
searchUrl = "https://www.abic.com.tw/index/search/area/1,2,4,5,6,7,8,10,11,12,13,14,16,18,19,20,21,22,23/filter/74/sort/distance/map_lat/24.9679464/map_lng/121.19183/page/{}"
page=1
res1 = r.get(searchUrl.format(page))
soup1 = bs(res1.text,"lxml")
lastPage = int(soup1.select_one("#pager").select("a")[13]["href"].split("page/")[1])

aList=[]
for i in range(1,lastPage):
    queue.put(i)

def worker():
    while not queue.empty():
        page=queue.get()
        print page
        crawler(page)

def crawlerContent(url, aDict):
    contentRes = r.get(url)
    contentSoup = bs(contentRes.text,"lxml")
    aDict["address"] = contentSoup.select_one("div.placeview_info").select("li")[0].text.encode("utf-8").split("：")[1].decode("utf-8")
    aDict["phone"] = contentSoup.select_one("div.placeview_info").select("li")[1].text.encode("utf-8").split("：")[1].decode("utf-8")
    tagString = ""
    tags = contentSoup.select_one("div.tag").select("a")
    for tag in tags:
        tagString += tag.text.strip() + ","
    aDict["tags"] = tagString
    aDict["content"] = contentSoup.select_one(".first_letter_big").text.strip()
    aDict["date"] = ""

def crawler(page):
    url = searchUrl.format(page)
    res = r.get(url)
    soup = bs(res.text,"lxml")

    articles = soup.select("div.round_corner_5_bottomleft")
    for article in articles:
        try:
            article_dict = {
                "title": "",
                "area": "",
                "address": "",
                "phone": "",
                "date": "",
                "content": "",
                "tags": "",
                "resp": "",
            }
            article_dict["area"] = article.select_one("div.area").select_one("a").text.strip();
            article_dict["title"] = article.select_one("div.title").select_one("a").text.strip();
            article_dict["resp"] = article.select_one("div.info").select_one("span").text.strip();
            tmpUrl = article.select_one("div.info").select_one("a")["href"]
            contentUrl = baseUrl + tmpUrl
            crawlerContent(contentUrl,article_dict)
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

encodedjson = json.dumps(aList, ensure_ascii=False)
with open("E:\\abicCrawler.json", "w") as f:
    f.write(encodedjson.encode("utf-8"))
    f.close()

print "All  Finish "+str(s2-s1)+"!!"