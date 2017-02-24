import requests as r
from bs4 import BeautifulSoup as bs

def crawler_content(aUrl):
    print "content......"

def crawler_folder(aUrl):
    res1 = r.get(aUrl)
    soup1 =  bs(res1.text, "lxml")
    articles1 = soup1.select("div.m-ent")
    for article1 in articles1:
        url1 = article1.select_one("a")["href"]
        s = "index.html"
        if url1.__contains__(s):
            crawler_folder(baseUrl+url1)
        else:
            crawler_content(baseUrl+url1)

baseUrl = "https://www.ptt.cc"
searchUrl = "https://www.ptt.cc/man/BabyMother/DD5D/DDD4/DDD7/index.html"
res = r.get(searchUrl)
soup = bs(res.text, "lxml")
articles = soup.select("div.m-ent")

for i in range(2,17):
    article = articles[i]
    tmpUrl = article.select_one("a")["href"]
    url = baseUrl + tmpUrl
    crawler_folder(url)


