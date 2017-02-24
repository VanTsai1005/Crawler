# !coding:utf-8
import requests as r
from bs4 import BeautifulSoup as bs
import json

# 搜尋內文時，合併URL用
originUrl = "http://www.ptt.cc"
# 一開始尋找最新頁碼用
firstURL = "https://www.ptt.cc/bbs/BabyMother/index.html"
# 有頁碼後搜尋用
searchUrl = "https://www.ptt.cc/bbs/BabyMother/index{}.html"

# 先開一個容器裝每個文章DICT
aList = []

res = r.get(firstURL)
soup = bs(res.text,"lxml")
# 找到最新頁碼
pageNo =  int(soup.select_one(".btn-group-paging").select("a")[1]["href"].split("index")[1].split(".h")[0])+1

# 傳入URL，抓內文用。
def getContent(linkUrl):
    res1 = r.get(linkUrl)
    soup1 = bs(res1.text,"lxml")
    content1 = soup1.select_one("#main-content").text.strip()
    return content1

# 從第一頁掃到最新頁
for page in range(pageNo+1-10,pageNo+1):
    print page
    url = searchUrl.format(page)
    res = r.get(url)
    soup = bs(res.text, "lxml")
    articles = soup.select(".r-ent")

    # 搜尋每頁的文章內容並存成DICT
    for article in articles:
        try:
            # 存內容的DICT
            article_dict = {
                "title": "",
                "catogory": "",
                "nrec": "",
                "date": "",
                "author": "",
                "content": ""
            }

            s = article.select_one("a").text;
            tmpUrl = article.select_one("a")["href"]
            # 合併內文頁的URL
            contentUrl = originUrl + tmpUrl

            article_dict["title"] = s.split("]")[1].strip()
            article_dict["catogory"] = s.split("]")[0].split("[")[1].strip()
            article_dict["nrec"] = article.select_one("div.nrec").select_one("span").text.strip()
            article_dict["date"] = article.select_one("div.date").text.strip()
            article_dict["author"] = article.select_one("div.author").text.strip()
            # 呼叫抓內文的METHOD，回傳出文章內容
            article_dict["content"] = getContent(contentUrl)
            # 加到容器裡  方便最後輸出
            aList.append(article_dict)
        except:
            pass

# 迴圈全部跑完後，到最外層將所有文章輸出
encodedjson = json.dumps(aList,ensure_ascii=False)
with open("E:\\test.json", "w") as f:
    f.write(encodedjson.encode("utf-8"))
    f.close()