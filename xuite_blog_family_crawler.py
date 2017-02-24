#! coding: utf-8

import time
from datetime import datetime
from selenium import webdriver
from Queue import Queue
from threading import Thread

NUM_THREADS = 4
aList = []
queue = Queue()
for i in range(2016,2005,-1):
    for j in range(12,0,-1):
        if j > 9:
            s = str(i)+"/"+str(j)
        else:
            s = str(i)+"/0"+str(j)
        queue.put(s)

def crawler(searchText):
    driver = webdriver.Remote("http://localhost:9515", webdriver.DesiredCapabilities.CHROME)
    driver.get("https://blog.xuite.net/")
    time.sleep(2)
    driver.find_element_by_id("header-search-input").send_keys(u"親子民宿 "+searchText)
    driver.find_element_by_id("header-search-submit").click()

    for i in range(2,11):
        time.sleep(0.5)
        urls = driver.find_elements_by_class_name("gsc-result")
        for url in urls:
            a = url.find_element_by_css_selector("a.gs-title")
            aList.append(a.get_attribute("href")+"\n")

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        pages = driver.find_elements_by_css_selector("div.gsc-cursor-page")
        time.sleep(0.5)
        chk = False
        for page in pages:
            try:
                if int(page.text) == i:
                    page.click()
                    chk = True
                    break;
            except:
                print "error "+searchText+" - "+page
                pass

        if chk == False:
            break

    print searchText
    driver.close()

def worker():
    while not queue.empty():
        sText=queue.get()
        crawler(sText)

s1 = datetime.now()
# 設定THREAD數量及執行的FUNCTION
threads = map(lambda i: Thread(target=worker), xrange(NUM_THREADS))
#啟動THREAD
map(lambda th: th.start(), threads)
map(lambda th: th.join(), threads)

with open("E:/urls.txt","w") as f:
    for item in aList:
        f.write(item)

s2 = datetime.now()

print "All  Finish "+str(s2-s1)+"!!"


