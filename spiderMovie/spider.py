# -*- codeing = utf-8 -*-
# @Time : 2021/3/23 14:50
# @Author : 水印红枫
# @Software: PyCharm

from bs4 import BeautifulSoup  # 网页解析获取数据
import re  # 正则表达式，进行文字匹配
import urllib.request, urllib.error, urllib.parse  # 指定url获取网络数据
import xlwt  # 进行excel操作
import sqlite3  # 进行数据库操作
import json
import time
# findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S) # re.S让.包含换行符
# src = re.findall(findImgSrc, html)[0]

def main():
    movieTop250 = []
    for i in range(0, 1):
        baseurl = "https://movie.douban.com/top250?start=" + str(i * 25)
        dataList = getData(baseurl)
        bs = BeautifulSoup(dataList, "html.parser")
        needBody = bs.find_all('div', class_="item")
        for x in needBody:
            try:
                item = dict()
                item["href"] = x.a["href"]
                item["imgSrc"] = x.a.img["src"]
                item["title"] = x.find(class_="hd").a.get_text()
                item["introduction"] = x.find(class_="bd").p.get_text()
                item["rateNum"] = x.find(class_="rating_num").get_text()
                item["evaluation"] = x.find(class_="star").find(class_=False, content=False).get_text()
                item["tip"] = x.find(class_="inq").get_text()
                movieTop250.append(item)
                print(item["title"])
            except Exception as error:
                print(error)
    saveName = "豆瓣电影top250"
    saveData(movieTop250, saveName)


def getData(url):
    # params = bytes(urllib.parse.urlencode({"hellw": "world"}), encoding="utf-8")
    # response = urllib.request.urlopen("http://httpbin.org/post", data=params)
    # print(response.read().decode('utf-8'))
    data = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36"
    }
    req = urllib.request.Request(url=url, headers=headers)
    try:
        response = urllib.request.urlopen(req)
        data = response.read().decode("utf-8")
    except Exception as e:
        if hasattr(e, "reason"):
            print(e.reason)
    return data


def saveData(data, name):
    try:
        f = open(name+".json", "w", encoding="utf-8")
        try:
            val = dict()
            val["time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            val["author"] = "水印红枫"
            val["data"] = data
            f.write(json.dumps(val, ensure_ascii=False, indent=2))
        finally:
            f.close()
    except Exception as error:
        print("保存到文件出错，原因为：", error)
    try:
        try:
            workBook = xlwt.Workbook(encoding="utf-8")
            workSheet = workBook.add_sheet("豆瓣电影top250", cell_overwrite_ok=True)
            for key in data[0].keys():
                print(key)
        finally:
            workBook.save(name+".xls")
    except Exception as error:
        print("保存到excel出错，原因为：", error)


if __name__ == "__main__":
    main()
    print("爬取完毕")
