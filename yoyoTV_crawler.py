# !coding:utf-8
import requests as r
from bs4 import BeautifulSoup as bs

baseUrl = "https://zh.wikipedia.org/zh-tw/%E6%9D%B1%E6%A3%AE%E5%B9%BC%E5%B9%BC%E5%8F%B0%E5%8B%95%E7%95%AB%E7%AF%80%E7%9B%AE%E5%88%97%E8%A1%A8"

res = r.get(baseUrl)
soup = bs(res.text, "lxml")

nameList = []
articles = soup.select_one("#mw-content-text").select("ul")
for article in articles:
    contents = article.select("li")
    for content in contents:
        s = content.text.encode("utf-8")
        if s.__contains__("《"):
            ss = s.split("《")[1].split("》")[0].strip()
            if ss.__contains__("（"):
                ss = ss.split("（")[0].strip()
            if ss.__contains__("("):
                ss = ss.split("(")[0].strip()
            nameList.append(ss+"\n")

with open("E:/yoyo.txt","w") as f:
    for item in nameList:
        f.write(item)

