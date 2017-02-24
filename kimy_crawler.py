# !coding:utf-8
import requests as r
from bs4 import BeautifulSoup as bs
from Queue import Queue
from threading import Thread
import json

NUM_THREADS = 8
baseUrl = "http://fun.kimy.com.tw"
searchUrl = "http://fun.kimy.com.tw/PostList.aspx?CategoryID=0&SearchID=0&AgegroupID=0&AreaID=0&ActivityID=1&TagID=0&TagIDStr=&SortParameter=PostDate%20desc&IsPrizeInPost=0&Page={}"

res = r.get(searchUrl.format(1))
soup = bs (res.text, "lxml")
lastPageNo = int(soup.select_one("#pagerDiv").select_one("#ctl00_ContentPlaceHolder1_inc_content_postList_new_lblPageCount").text)
aList = []

def crawler_content(contentUrl, dict):
    resC = r.get(contentUrl)
    soupC = bs(resC.text, "lxml")
    dict["title"] = soupC.select_one("span.A3 span").text
    dict["date"] = soupC.select_one("span.A1 span").text
    dict["auth"] = soupC.select_one("span.A1 a").text
    tags = soupC.select_one("#ctl00_ContentPlaceHolder1_lblTags").select("a")
    tagText = ""
    for tag in tags:
        tagText += tag.text+","
    if tagText == "":
        return False
    dict["tags"] = tagText
    dict["resp"] = soupC.select_one("#ctl00_ContentPlaceHolder1_lblReadTimes").text
    dict["content"] = soupC.select_one("#postContentDiv").text
    return True

def crawler(page):
    dict = {
        "title":"",
        "content":"",
        "area":"",
        "auth":"",
        "resp":"",
        "date":"",
        "tags":""
    }

    url = searchUrl.format(page)
    res = r.get(url)
    soup = bs(res.text, "lxml")
    articles = soup.select("#ctl00_ContentPlaceHolder1_inc_content_postList_new_dListProduct")[0].select("tr")
    for article in articles:
        try:
            contentUrl = baseUrl + article.select("a")[1]["href"]
            if crawler_content(contentUrl, dict):
                aList.append(dict)
        except:
            pass
    print page

def worker():
    while not queue.empty():
        page = queue.get()
        crawler(page)

for i in range(0,5):
    aList = []
    queue = Queue();

    beginPage = 1+100*i
    endPage = 101+100*i

    for j in range(beginPage,endPage):
        queue.put(j)

    try:

        #設定THREAD數量及執行的FUNCTION
        threads = map(lambda i: Thread(target=worker), xrange(NUM_THREADS))
        #啟動THREAD
        map(lambda th: th.start(), threads)
        map(lambda th: th.join(), threads)
    except:
        print "thread error"
    finally:
        encodedjson = json.dumps(aList, ensure_ascii=False)
        with open("E:\\kimy_"+str(endPage-1)+".json", "w") as f:
            f.write(encodedjson.encode("utf-8"))
            f.close()
        print "All Finish !!"






