#!/usr/bin/python
#!coding:utf-8

import requests as r
from bs4 import BeautifulSoup as bs
from threading import Thread
from Queue import Queue
from datetime import datetime
import json
import random
import time

NUM_THREADS = 8
timeoutSec = 6
searchUrl = "https://www.pixnet.net/searcharticle?q=%E8%A6%AA%E5%AD%90%E9%A4%90%E5%BB%B3&type=related&period=all&page={}"
# cookies = {
#     "__asc":"27dd21e4159731ab8b1d35717ab",
#     "__auc":"27dd21e4159731ab8b1d35717ab",
#     "lang":"zh_TW",
#     "mainpage2":"93f6cfd193742094d1e4b6d92979c071ed6a6fdf6388ee00512653a543c2201d%7C%7B%22data%22%3A%7B%22Pix_Form%3A%3AsToken%22%3A%220a8de88757fc6e8361f0643d1d7db485%22%7D%2C%22expire%22%3A0%2C%22timestamp%22%3A1483694822%7D",
#     "mp_8b1cbbc97d19521d21cd37961ad741db_mixpanel":"%7B%22distinct_id%"
# }
#
# header = {
#     "Accept":"text/html",
#     "Accept-Encoding":"gzip",
#     "Accept-Language":"zh-TW",
#     "Cache-Control":"max-age=0",
#     "Connection":"keep-alive",
#     "Cookie":"lang=zh_TW",
#     "Host":"www.pixnet.net",
#     "Referer":"https://www.pixnet.net/",
#     "Upgrade-Insecure-Requests":"1",
#     "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
# }

areaList = ["新北","台北","桃園","新竹","苗栗","台中","南投","嘉義","台南","雲林","高雄","屏東","台東","花蓮","宜蘭","澎湖"]
baseRes = r.get(searchUrl.format(1))
baseSoup = bs(baseRes.text,"lxml")

ipList = []
with open("E:/ips.txt","r") as f:
    for item in f.readlines():
        ipList.append(item)
    f.close()
# lastPage = (int(baseSoup.select_one("div.search-count").select_one(".num").text) // 10) + 1

aList = []
queue = Queue();

def worker():
    while not queue.empty():
        page=queue.get()
        crawler(page)

def crawler_content(contentUrl,dict,ip):
    n = 0
    while True:
        try:
            if n >= 5:
                dict["content"] = ""
                print("content not found !!")
                return False
            contentRes = r.get(contentUrl, timeout=timeoutSec)
            break
        except:
            n += 1
            pass
    # contentRes = r.get(contentUrl, timeout=timeoutSec)
    contentRes.encoding = "utf-8"
    contentSoup = bs(contentRes.text,"lxml")
    if contentSoup.select_one("#article-content-inner"):
        content = contentSoup.select_one("#article-content-inner").text
        dict["content"] = content
        for i in range(0, len(areaList)):
            area = areaList[i].decode("utf-8")
            if content.__contains__(area):
                dict["area"] = area
                break;
    else:
        print contentUrl
        dict["content"] = ""
    return True

def crawler(page):
    nip = random.randint(0, len(ipList)-1)
    ip = ipList.__getitem__(nip).strip()
    proxy = {"http": "http://{}".format(ip)}
    # proxy = {"http": "http://127.0.0.1:8118"}
    url = searchUrl.format(page)
    n = 0
    while True:
        try:
            if n >= 5:
                print("http not found !!")
                return False
            res = r.get(url, proxies=proxy, timeout=timeoutSec)
            break
        except:
            n += 1
            # nip = random.randint(0, len(ipList) - 1)
            # ip = ipList.__getitem__(nip).strip()
            # proxy = {"http": "http://{}".format(ip)}
            pass

    res.encoding = "utf-8"
    soup = bs(res.text,"lxml")

    articles = soup.select(".search-list")
    for article in articles:
        article_dict = {
            "title": "",
            "area": "",
            "address": "",
            "phone": "",
            "date": "",
            "content": "",
            "tags": "",
            "resp": "",
            "auth":"",
            "url":""
        }

        tmpUrls = article.select_one("a")["href"].split("http%3A%2F%2F")[1].split("%2F")
        tmpUrl = "http://"
        for tmp in tmpUrls:
            tmpUrl += tmp+"/"

        article_dict["url"] = tmpUrl
        article_dict["title"] = article.select_one(".search-title").select_one("a").text.strip()
        article_dict["auth"] = article.select_one("div.search-meta").select_one("a").text.strip()
        article_dict["date"] = article.select_one(".search-postTime").text.strip()
        article_dict["resp"] = article.select_one(".search-views").select_one("span").text.strip()

        crawler_content(tmpUrl,article_dict,ip)
        time.sleep(random.randint(0,2))
        aList.append(article_dict)
    print page
    return True

for i in range(0,10):
    aList = []
    queue = Queue();

    beginPage = 1+250*i
    endPage = 251+250*i

    for j in range(beginPage,endPage):
        queue.put(j)

    s1 = datetime.now()
    try:
        #設定THREAD數量及執行的FUNCTION
        threads = map(lambda i: Thread(target=worker), xrange(NUM_THREADS))
        #啟動THREAD
        map(lambda th: th.start(), threads)
        map(lambda th: th.join(), threads)
    except:
        print "thread error"
    finally:
        s2 = datetime.now()
        encodedjson = json.dumps(aList, ensure_ascii=False)
        with open("E:\\PixnetRestaurantCrawler"+str(beginPage)+"_"+str(endPage)+".json", "w") as f:
            f.write(encodedjson.encode("utf-8"))
            f.close()
        print "All - "+str(i)+" Finish "+str(s2-s1)+"!!"
