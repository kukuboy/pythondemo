# -*- codeing = utf-8 -*-
# @Time : 2021/3/23 14:50
# @Author : 水印红枫
# @Software: PyCharm

from bs4 import BeautifulSoup  # 网页解析获取数据
import re  # 正则表达式，进行文字匹配
import urllib.request, urllib.error, urllib.parse  # 指定url获取网络数据
import xlwt  # 进行excle操作
import sqlite3  # 进行数据库操作
import json
import time


def main():
    movieTop250 = []
    for i in range(0, 10):
        baseurl = "https://movie.douban.com/top250?start=" + str(i * 25)
        dataList = getData(baseurl)
        bs = BeautifulSoup(dataList, "html.parser")
        needBody = bs.find_all(class_="item")
        for x in needBody:
            try:
                item = dict()
                item["href"] = x.a["href"]
                item["imgSrc"] = x.a.img["src"]
                item["title"] = x.find(class_="hd").a.get_text()
                item["introduction"] = x.find(class_="bd").p.get_text()
                item["rateNum"] = x.find(class_="rating_num").get_text()
                item["evaluation"] = x.find(class_="star").get_text()
                item["tip"] = x.find(class_="inq").get_text()
                movieTop250.append(item)
                print(item["title"])
            except Exception as error:
                print(error)
    saveUrl = "./豆瓣电影top250.json"
    saveData(movieTop250, saveUrl)


def getData(url):
    # params = bytes(urllib.parse.urlencode({"hellw": "world"}), encoding="utf-8")
    # response = urllib.request.urlopen("http://httpbin.org/post", data=params)
    # print(response.read().decode('utf-8'))
    data = []
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "bid=aM3-vjepH1w; ll='118237'; ap_v=0,6.0; __utma=30149280.2089052912.1616481086.1616481086.1616481086.1; __utmc=30149280; __utmz=30149280.1616481086.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=223695111.1339687591.1616481086.1616481086.1616481086.1; __utmc=223695111; __utmz=223695111.1616481086.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __yadk_uid=bu6RZRutYXflxTfuSdh8H7mFL3bL7oy3; _vwo_uuid_v2=D6D8C56B4D9FB491C9C5B44E08234CDF4|30e256e911c9a9ba4e44cf70e4816988; __gads=ID=fe0768f08887dfb4-22733963c4c60021:T=1616481116:RT=1616481116:S=ALNI_MbDdbeBbCeL0au65abrmnZQWtssng; _pk_id.100001.4cf6=7699b2376cffe289.1616481086.1.1616481171.1616481086.",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3861.400 QQBrowser/10.7.4313.400"
    }
    req = urllib.request.Request(url=url, headers=headers)
    try:
        response = urllib.request.urlopen(req)
        data = response.read().decode("utf-8")
    except Exception as e:
        if hasattr(e, "reason"):
            print(e.reason)
    return data


def saveData(data, path):
    f = open(path, "w", encoding="utf-8")
    val = dict()
    val["time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    val["author"] = "水印红枫"
    val["data"] = data
    f.write(json.dumps(val, ensure_ascii=False, indent=2))
    f.close()


if __name__ == "__main__":
    main()
