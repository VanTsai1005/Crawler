#coding:utf-8
import requests as r
from bs4 import	BeautifulSoup
import json

Basic_URL = "http://www.atmovies.com.tw"
URL = Basic_URL + "/movie/next/0//"

res = r.get(URL)
soup =BeautifulSoup(res.text, 'lxml')

comingMovie = soup.select_one('div.content').select(".filmNextListAll")
print len(comingMovie)

comingMovieList = []

for item in comingMovie:
    comingMovie_dict = {
        "movieTitle":"",
        "movieURL":""
    }
    comingMovie_dict["movieTitle"] = item.select_one('a').text
    comingMovie_dict["movieURL"] = Basic_URL + item.select_one('a')['href']
    comingMovieList.append(comingMovie_dict)

encodedjson = json.dumps(comingMovie_dict, ensure_ascii=False)
with open("E:\\ios.json", "w") as f:
    f.write(encodedjson.encode("ISO-8859-1").strip())
    f.close()
