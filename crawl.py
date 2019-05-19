#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# @Author   :triangle
# @Time     :2019/5/16 12:36
# @Filename :crawl.py
import time
import random

import requests
from pyquery import PyQuery as pq
import re
from pymongo import MongoClient
from fontchange import fontchange
from selenium import webdriver


headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
}
# 不带上Cookie就访问不了这个页面
cookie = "ssuid=5460794600; TYCID=8e812900709811e981ff6337f67db989; undefined=8e812900709811e981ff6337f67db989; _ga=GA1.2.1167793852.1557213616; aliyungf_tc=AQAAAMQM0GUD/wsAUdBJ3+3KqQjhhWOQ; csrfToken=Cow1m4r11ST6053UYYnxe0oi; bannerFlag=undefined; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1557980813,1558008942,1558013493,1558144360; RTYCID=ac0d009d136c4000a843080efb0cc0f0; _gid=GA1.2.396743236.1558241394; CT_TYCID=daf9d61812644d78af0d9d5419ec85f6; token=828ac00d056f4bd68c9348f1eb6cff26; _utm=ba115a58442c4883a925779f9bd64307; tyc-user-info=%257B%2522claimEditPoint%2522%253A%25220%2522%252C%2522myAnswerCount%2522%253A%25220%2522%252C%2522myQuestionCount%2522%253A%25220%2522%252C%2522signUp%2522%253A%25220%2522%252C%2522explainPoint%2522%253A%25220%2522%252C%2522privateMessagePointWeb%2522%253A%25220%2522%252C%2522nickname%2522%253A%2522%25E7%2599%25BD%25E8%25B5%25B7%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522privateMessagePoint%2522%253A%25220%2522%252C%2522state%2522%253A%25220%2522%252C%2522announcementPoint%2522%253A%25220%2522%252C%2522isClaim%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522discussCommendCount%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%25220%2522%252C%2522onum%2522%253A%25220%2522%252C%2522claimPoint%2522%253A%25220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzQyMjgyMDcyMSIsImlhdCI6MTU1ODI0NjY3OCwiZXhwIjoxNTg5NzgyNjc4fQ.6dcss-7AgCney5sDfYRkhzRazpBp6HhnSX128mGhkdXR3AnKcrpT7JE_SnC76G6UhDYL3aMPBp6biqIiYJKYvg%2522%252C%2522pleaseAnswerCount%2522%253A%25220%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252213422820721%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzQyMjgyMDcyMSIsImlhdCI6MTU1ODI0NjY3OCwiZXhwIjoxNTg5NzgyNjc4fQ.6dcss-7AgCney5sDfYRkhzRazpBp6HhnSX128mGhkdXR3AnKcrpT7JE_SnC76G6UhDYL3aMPBp6biqIiYJKYvg; cloud_token=b949726f8dda430fb00216b0c8d733c8; cloud_utm=518b7c064dd848029a2a32fc6bb37bf6; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1558254034"

# 将上面哪个cookie转化成字典类型
cookie_dict = {i.split("=")[0]:i.split("=")[-1] for i in cookie.split("; ")}

conn = MongoClient("localhost", 27017)
db = conn['tianyancha']


def login():
    url = "www.tianyancha.com/login"
    driver = webdriver.Chrome()

def get_url(url,page):
    url= "https://www.tianyancha.com/search/p1?key=知乎"
    response = requests.get(url, headers=headers, cookies=cookie_dict)
    if response.status_code == 200:
        doc = pq(response.text)
        items = doc("#web-content > div > div.container-left > div.search-block.header-block-container > div.result-list.sv-search-container > div").items()
        data = {}
        for item in items:
            #利用图片的填充文本获取公司名字
            img = item("div > div.left-item > div > div.logo.-w88 > img")
            data['name'] = img.attr("alt").replace("<em>", "").replace("</em>", "")
            # 获取公司url
            a = item("div > div.content > div.header > a")
            data['url'] = a.attr("href")
            yield data
            # 北京知乎科技有限责任公司 https: // www.tianyancha.com / company / 32656967
    else:
        return None

def get_page(url):
    response = requests.get(url,headers=headers)
    if response.status_code == 200:
        print(response.text)
        doc = pq(response.text)
        str1 = doc('.tyc-num').text()
        if str1:
            str1 = fontchange(str1)
        else:
            text = doc("_container_baseInfo > table.table.-striped-col.-border-top-none.-breakall").text()
            print(text)


def savetomongo(keyword, data):
    dataset = db[keyword]
    dataset.update_one({"name": data['name']},{'$set':data}, True)


if __name__ == "__main__":
    keyword = '知乎'
    #未登录只允许查5页内容 input("请输入需要爬取的页数：") input("请输入要查找的公司关键字：")
    page = ''
    for data in get_url(keyword,page):
        time.sleep(5)
        savetomongo(keyword,data)
        get_page(data["url"])



