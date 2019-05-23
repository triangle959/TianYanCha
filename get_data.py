import json
import re
import random
from time import sleep

import requests
from pymongo import MongoClient
from pyquery import PyQuery as pq
from fontchange import fontchange

res = requests.get('http://106.13.9.45:8007/pop')
proxy = json.loads(res.text)

headers ={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36",
    "Connection": "keep-alive",
    "Host": "www.tianyancha.com"
}

# 不带上Cookie就访问不了这个页面
cookie = "aliyungf_tc=AQAAAIub1w4uFgcAikIYdAQzI8dY9mjU; ssuid=6115264187; bannerFlag=undefined; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1558404890; _ga=GA1.2.418827579.1558404891; _gid=GA1.2.1891485528.1558404891; csrfToken=lpQFxeRdjmGjcXoLdq3aGZsV; TYCID=46901ee07b6e11e9be27abfcc402465e; undefined=46901ee07b6e11e9be27abfcc402465e; RTYCID=3893429da45240babd4ebcf58969d8c0; CT_TYCID=4135fc93e4a744efb4baa63d20fbf539; _gat_gtag_UA_123487620_1=1; token=a2e453b73bdb483689cb1e653afc9501; _utm=ec1d80bc6b174ee0b1244b21be75a067; tyc-user-info=%257B%2522claimEditPoint%2522%253A%25220%2522%252C%2522myAnswerCount%2522%253A%25220%2522%252C%2522myQuestionCount%2522%253A%25220%2522%252C%2522signUp%2522%253A%25220%2522%252C%2522explainPoint%2522%253A%25220%2522%252C%2522privateMessagePointWeb%2522%253A%25220%2522%252C%2522nickname%2522%253A%2522%25E7%2599%25BD%25E8%25B5%25B7%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522privateMessagePoint%2522%253A%25220%2522%252C%2522state%2522%253A%25220%2522%252C%2522announcementPoint%2522%253A%25220%2522%252C%2522isClaim%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522discussCommendCount%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%25224%2522%252C%2522onum%2522%253A%25220%2522%252C%2522claimPoint%2522%253A%25220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzQyMjgyMDcyMSIsImlhdCI6MTU1ODU3NDEyMSwiZXhwIjoxNTkwMTEwMTIxfQ.QtfsbeQnO7hclIN8u91-lGGjpA9IAnGD7oV6iUT6X3L-9MASeA2_sg6n3HY1CMuuEs9sXHQibat0Ovm2WGbgkA%2522%252C%2522pleaseAnswerCount%2522%253A%25220%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252213422820721%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzQyMjgyMDcyMSIsImlhdCI6MTU1ODU3NDEyMSwiZXhwIjoxNTkwMTEwMTIxfQ.QtfsbeQnO7hclIN8u91-lGGjpA9IAnGD7oV6iUT6X3L-9MASeA2_sg6n3HY1CMuuEs9sXHQibat0Ovm2WGbgkA; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1558574102; cloud_token=33904acac4d444f694a3f0512fb7ca64; cloud_utm=c9a3948de7934cd9b148c0fca7ddcac3"
# Hm_lpvt_开头参数不一致
# 将上面哪个cookie转化成字典类型
cookie_dict = {i.split("=")[0]:i.split("=")[-1] for i in cookie.split("; ")}

conn = MongoClient("localhost", 27017)
db = conn['tianyancha']

def crawl_item(keyword):
    for item in db[keyword].find({}):
        sleep(random.randrange(1, 15))
        headers["Referer"] = "https://antirobot.tianyancha.com/captcha/verify?return_url=https%3A%2F%2Fwww.tianyancha.com%2Fcompany%"+ item["url"][35::] +"&rnd="
        response = requests.get(url=item["url"], headers=headers, cookies=cookie_dict)
        doc = pq(response.text)
        str1 = doc('.tyc-num').text()
        if str1:
            print(str1)
            str2 = fontchange(str1)
            print(str2)
        else:
            text2 = doc("#_container_baseInfo .table:nth-child(2)").text().split("\n")
            my_dict = {}
            my_dict["name"] = item["name"]
            for i in range(0, len(text2) - 1, 2):
                my_dict[text2[i]] = text2[i + 1]
            yield my_dict

def savetomongo(keyword, data):
    dataset = db[keyword]
    dataset.update_one({"name": data['name']},{'$set':data}, True)


if __name__ == '__main__':
    keyword = "百度"
    for data in crawl_item(keyword):
        print(data)
        savetomongo(keyword,data)