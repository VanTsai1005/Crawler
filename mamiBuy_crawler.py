# !coding:utf-8
import requests as r
from bs4 import BeautifulSoup
import re
from threading import Thread
from Queue import Queue
from datetime import datetime
import json
import random


NUM_THREADS = 8
timeoutSec = 6
ipList = []
with open("E:/ips.txt","r") as f:
    for item in f.readlines():
        ipList.append(item)
    f.close()
# 取得mamibuy 親子旅遊總共篇數
URL_index = "https://mamibuy.com.tw/talk/article/"
res = r.get(URL_index)
soup = BeautifulSoup(res.text, 'lxml')
# 找到mamibuy 親子旅遊總共篇數位子
article = soup.select('form div div div div div div a span')[2].text.split(' ')[1]
# 將unicode字元格式轉成int
article_count = int(article)  # 5674
# 算頁數
pages_count = (article_count / 21) - 5 + 1

def worker():
    while not queue.empty():
        page=queue.get()
        crawler(page)

def crawler(page):
    URL_mamibuy_travel = "https://mamibuy.com.tw/talk/article/?cid=9&aid=0&s=1&p={}".format(page)

    nip = random.randint(0, len(ipList)-1)
    ip = ipList.__getitem__(nip).strip()
    # proxy = {"http": "http://{}".format(ip)}
    proxy = {"http": "http://127.0.0.1:8118"}
    url = URL_mamibuy_travel.format(page)
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
            nip = random.randint(0, len(ipList) - 1)
            ip = ipList.__getitem__(nip).strip()
            proxy = {"http": "http://{}".format(ip)}
            pass

    res2 = r.get(URL_mamibuy_travel)
    soup2 = BeautifulSoup(res2.text, 'lxml')
    article_title = soup2.select('form div div div div div div.well')
    for article_title_loop in article_title:
        article_dict = {
            "name":"",
            "area":"",
            "phone":"",
            "address":"",
            "date":"",
            "resp":"",
            "content":"",
            "auth":""
        }
        try:
            comparison_write = article_title_loop.select('a.link-black div.content-info')[0].text.replace(' ', "").split('\n')[1]
            if re.match(r"^20.*", comparison_write) != None:
                date_need_edit = \
                article_title_loop.select('a.link-black div.content-info')[0].text.replace(' ', "").split('\n')[
                    1].replace('/', '-')
                article_dict['date'] = date_need_edit.replace('\r', '').strip()
            else:
                date_string = \
                article_title_loop.select('a.link-black div.article-list-photo img')[0]['data-original'].split('_')[
                    1].split('.jpg')[0]
                article_dict['date'] = date_string[0:4] + '-' + date_string[4:6] + '-' + date_string[6:8]
        except:
            article_dict['date'] = ""

        try:
            article_dict['resp'] = \
            article_title_loop.select('a.link-black div.content-info')[0].text.replace(' ', "").split('\n')[2].replace('\r', '')
        except:
            article_dict['resp'] = ""

        try:
            article_dict['auth'] = article_title_loop.select_one("div.member-profile div span").text
        except:
            article_dict['auth'] = ""

        try:
            article_dict['title'] = article_title_loop.select('a.link-black div.content-title')[0].text
            str_url1 = article_title_loop.select('a')[0]['href'].split('/home/')[1]
            str_url2 = article_title_loop.select('a')[1]['href'].split('article/')[1].split('/')[0]
            url3 = 'http://tw.mamibai.com/html/article/{}'.format(str_url1) + '/{}'.format(str_url2) + '.html'
            article_dict['url'] = url3
            res4 = r.get(url3)
            res4.encoding = "utf-8"
            soup4 = BeautifulSoup(res4.text, 'lxml')
            article_content_bodyDiv = soup4.select('#divContent')
            for article_content_loop in article_content_bodyDiv:
                sstt1 = '$(\"#ifAd\").attr(\"src\", \"http://mamibuy.com.tw/ad/content.aspx?app=\" + util.queryString(\"app\"));'
                sstt2 = "[email protected]/* <![CDATA[ */!function(t,e,r,n,c,a,p){try{t=document.currentScript||function(){for(t=document.getElementsByTagName('script'),e=t.length;e--;)if(t[e].getAttribute('data-cfhash'))return t[e]}();if(t&&(c=t.previousSibling)){p=t.parentNode;if(a=c.getAttribute('data-cfemail')){for(e='',r='0x'+a.substr(0,2)|0,n=2;a.length-n;n+=2)e+='%'+('0'+('0x'+a.substr(n,2)^r).toString(16)).slice(-2);p.replaceChild(document.createTextNode(decodeURIComponent(e)),c)}p.removeChild(t)}}catch(u){}}()/* ]]> */".decode('utf-8')
                sstt3 = "(function(d, s, id) {\r  var js, fjs = d.getElementsByTagName(s)[0];\r  if (d.getElementById(id)) return;\r  js = d.createElement(s); js.id = id;\r  js.src = \"//connect.facebook.net/zh_TW/sdk.js#xfbml=1&version=v2.5\";\r  fjs.parentNode.insertBefore(js, fjs);\r}(document, 'script', 'facebook-jssdk'));\r"
                sstt4 = '$(\"#ifAd\").attr(\"src\", \"http://mamibuy.com.tw/ad/content.aspx?app=\" + util.queryString(\"app\"));'
                test1 = article_content_loop.text.strip().replace("\n", "").replace(sstt1, "").replace(sstt3, "").replace(sstt4, "")
                article_dict['content'] = test1.replace(sstt2, "")
            aList.append(article_dict)
        except:
            pass
    print page

nums = 30
for i in range(8, 9):
    aList = []
    queue = Queue();

    beginPage = 1 + nums * i
    endPage = (nums+1) + nums * i

    for j in range(beginPage, endPage):
        queue.put(j)

    s1 = datetime.now()
    try:
        # 設定THREAD數量及執行的FUNCTION
        threads = map(lambda k: Thread(target=worker), xrange(NUM_THREADS))
        # 啟動THREAD
        map(lambda th: th.start(), threads)
        map(lambda th: th.join(), threads)
    except:
        print "thread error"
    finally:
        s2 = datetime.now()
        encodedjson = json.dumps(aList, ensure_ascii=False)
        with open("E:\\mamibuy" + str(beginPage) + "_" + str(endPage) + ".json", "w") as f:
            f.write(encodedjson.encode("utf-8"))
            f.close()
        print "All - " + str(i) + " Finish " + str(s2 - s1) + "!!"