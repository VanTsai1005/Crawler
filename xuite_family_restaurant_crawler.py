#! coding:utf-8
#!from xuite_family_restaurant

import requests as r
import json
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from threading import Thread

def crawler_content(URL):
    res1 = r.get("http://yo.xuite.net"+URL)
    res1.encoding = 'utf-8'
    soup1 = BeautifulSoup(res1.text, 'lxml')

    article_dict = {
        'auth':"",
        'resp':"",
        'tags':"",
        'area':'',
        'title':'',
        'date':'',
        'content':''
    }

    try:
        article_dict["resp"] = int(soup1.select_one("#element-data-page-view").select_one("span.element-data-page-view-detail").text)
        #抓auth
        article_dict['auth'] = soup1.select_one("#element-owner-name").text
        #抓title
        # print soup.select_one('.titlename').text
        article_dict['title'] = soup1.select_one('#element-info-title').text

        #抓日期
        dt = soup1.select_one('#element-data-update-date').select_one(".element-data-update-date-detail").text
        date= datetime(int(dt[0:4]), int(dt[5:7]), int(dt[8:10]))
        # print datetime.strftime(date, '%Y-%m-%d')
        article_dict['date'] = datetime.strftime(date, '%Y-%m-%d')

        #抓文
        # "str" 前面加 u 成了unicode 編碼
        areaList = [u"新北",u"台北",u"桃園",u"新竹",u"苗栗",u"台中",u"南投",u"嘉義",u"台南",u"雲林",u"高雄",u"屏東",u"台東",u"花蓮",u"宜蘭",u"澎湖"]
        if soup1.select_one('#element-describe-content').text.strip():
            content = soup1.select_one('#element-describe-content').text.strip()
            # print content
            article_dict['content'] = content
            #抓地區
            for i in range(0,len(areaList)):
                area = areaList[i]
                #area = areaList[i].decode("utf-8")     # 轉回unicode 編碼
                if content.__contains__(area):
                    # print area
                    article_dict['area'] = area
                    break;
        else:
            dict["content"] = ""
    except:
        pass
    articleList.append(article_dict)

#step 1 :
url = ('http://yo.xuite.net/info/search.php?keyword=%E8%A6%AA%E5%AD%90&c=TWN00000&p={}')
NUM_THREADS = 8
articleList = []

from Queue import Queue
queue = Queue()

for page in range(1,31):
    queue.put(page)

def worker():
    while not queue.empty():
        page=queue.get()
        crawler(page)

def crawler(page):
    # print "c page {}".format(url.format(page))
    res = r.get(url.format(page))
    # print "result {}".format(res)
    soup = BeautifulSoup(res.text, 'lxml')
    articles = soup.select('li.componet-element-item')
    for entry in range(0,len(articles)):
        article = articles[entry]
        article_url = article.select('a')[0]['href']
        crawler_content(article_url)
        # print article_url
    print page


s1 = datetime.now()
try:
    # 設定THREAD數量及執行的FUNCTION
    threads = map(lambda i: Thread(target=worker), xrange(NUM_THREADS))
    # 啟動THREAD
    map(lambda th: th.start(), threads)
    map(lambda th: th.join(), threads)
except:
    print "thread error"
finally:
    s2 = datetime.now()
    xuite_family_restaurant = json.dumps(articleList, ensure_ascii=False)
    with open('E:/xuite_family_restaurant.json', 'a') as f:
        f.write(xuite_family_restaurant.encode('utf-8'))
        f.close()
    print "All Finish " + str(s2 - s1) + "!!"

