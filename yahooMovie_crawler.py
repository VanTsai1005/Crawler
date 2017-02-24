import requests as r
from bs4 import BeautifulSoup as bs
import json

savePath = "E:/{}"
baseUrl = "https://tw.movies.yahoo.com/movie_comingsoon.html?p={}"

aList = []
for page in range(1,9):
    url = baseUrl.format(page)
    res = r.get(url)
    soup = bs(res.text, "lxml")

    articles = soup.select("div.clearfix.row")
    for article in articles:
        try:
            dict = {
                "title_cn":"",
                "title_en": "",
                "url":"",
                "date":"",
                "expect":""
            }
            dict["title_cn"] =  article.select_one("div.text").select_one("h4 a").text
            dict["title_en"] = article.select_one("div.text").select_one("h5 a").text
            dict["url"] = article.select_one("div.text").select_one("a")["href"]
            dict["date"] = article.select_one("span.date span").text
            dict["expect"] = article.select_one("div.bd.clearfix").text.strip()
            aList.append(dict)
        except:
            pass

for item in aList:
    print item["title_cn"]
    print item["title_en"]
    print item["url"]
    print item["date"]
    print item["expect"]
    print "----------------------------------------------"

encodedjson = json.dumps(aList, ensure_ascii=False)
with open(savePath.format("test.json"), "w") as f:
    f.write(encodedjson.encode("utf-8"))
    f.close()
print "FInish !!"



