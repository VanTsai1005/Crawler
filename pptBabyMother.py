#! coding:utf-8
#Baby Mother PPT

import requests as r
from bs4 import BeautifulSoup

#step:4  定義存為json檔
def full_articles(full_art):
    import json
    ptt_babymother = json.dumps(full_art, ensure_ascii=False)  # 以副檔名.json格式儲存,字典內容 非以 使用 unicode string編碼
    with open('ptt_babymother.json', 'a') as f:  # 寫一個檔案並命名為 ptt_babymother.json ;  ' a'  : 附加,在結尾處寫入資料
        f.write(ptt_babymother.encode('utf-8'))  # 以 utf-8格式寫入資料

# step : 1    定義爬取內文 function
def crawler_content(contentUrl):
    res = r.get(contentUrl)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'lxml')

    article_dict = {
        'board': '',
        'author': '',
        'title': '',
        'datetime': '',
        'web_url': '',
        'content': ''
    }
    content_inside = soup.select_one('#main-content')

    try:
        try:
            if soup.select_one('span.article-meta-value'):
                article_dict['author'] = soup.select('span.article-meta-value')[0].text
                article_dict['board'] = soup.select('span.article-meta-value')[1].text
                article_dict['title'] = soup.select('span.article-meta-value')[2].text.split('[')[1].split(']')[1].strip()
                article_dict['datetime'] = soup.select('span.article-meta-value')[3].text
        except:
            pass

        for web_side in content_inside.select('a'):
            try:
                article_dict['web_url'] = content_inside.select("a")[0]["href"]  # 擷取文章中的網誌連結url
                web_side.extract()  # 刪除文章中的網誌連結url
            except:
                pass

        for del_span in content_inside('span'):
            del_span.extract()
        article_dict['content'] = content_inside.text.replace('--', '').replace('==', '').replace("◆".decode('utf-8'), '').split('From')[0].split()  # 僅保留文章內容

        all_articles.append(article_dict) # dict{}內容,附加進 all_articles = []

        full_articles(all_articles) #跑full_articles( )函數

    except Exception as e:
        print str(e)

# step : ２    定義爬取標題　url  連結 function
def crawler_folder(innerUrl):
    res = r.get(innerUrl)
    soup = BeautifulSoup(res.text, 'lxml')

    articles2 = soup.select('.m-ent')

    for title_list in articles2:
        list_URL = title_list.select("a")[0]["href"] #抓取 url
        web = "index.html"
        if list_URL.__contains__(web):  #所抓到的 url 結尾有 "index.html"  跑函數 crawler_folder( )
            crawler_folder( basic_url +list_URL)
        else:
            crawler_content( basic_url +list_URL) #所抓到的 url 結尾沒有 "index.html"  跑函數 crawler_content( )

        # step : 3 爬網的首頁
basic_url = ('https://www.ptt.cc')
url = (basic_url + '/man/BabyMother/DD5D/DDD4/DDD7/index.html')
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
res = r.get(url, headers=headers)
soup = BeautifulSoup(res.text, 'lxml')
articles = soup.select('.m-ent')

all_articles = []# 將 dict {}內容塞入

for entry in range(0, len(articles)):
    article = articles[entry]
    tmp_RUL = article.select("a")[0]["href"]
    top_URL = basic_url + tmp_RUL
    web_connect = "index.html"
    if top_URL.__contains__(web_connect):
        crawler_folder(top_URL)
    else:
        crawler_content(top_URL)











