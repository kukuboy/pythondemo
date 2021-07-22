# -*- codeing = utf-8 -*-
# @Time : 2021/7/21 11:26
# @Author : 水印红枫
# @Software: PyCharm
import sys

import mysql.connector
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
    begin("https://dy.dytt8.net/html/gndy/dyzz/index.html", "GBK", "https://dy.dytt8.net")


def begin(url, charset, baseurl=""):
    dataList = getData(url, charset)
    bsList = BeautifulSoup(dataList, "html.parser")
    needBody = bsList.find_all('table', class_="tbspan")
    for x in needBody:
        try:
            movie_time = x.find('font').get_text()
            print(movie_time)
            item = x.find('a', class_="ulink")["href"]
            data = getData(baseurl + item, charset)
            bs = BeautifulSoup(data, "html.parser")
            name = bs.find('div', class_="title_all").get_text()
            link = bs.find('a', target="_blank")["href"]
            saveData(name, movie_time, link)
        except Exception as error:
            print(error)
    try:
        nextUrl = bsList.find('a', text="下一页")["href"]
        begin(baseurl + "/html/gndy/dyzz/" + nextUrl, charset, baseurl)
    except Exception as error:
        print(error)


def getData(url, charset="utf-8"):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36"
    }
    req = urllib.request.Request(url=url, headers=headers)
    try:
        response = urllib.request.urlopen(req)
        return response.read().decode(charset)
    except Exception as e:
        if hasattr(e, "reason"):
            print("抓取数据失败的原因是：", e.reason)
        else:
            print("抓取数据位置原因退出")
        sys.exit(0)


def saveData(name, movie_time, link):
    # 保存到mysql
    try:
        print("--------------正在保存", name, "到数据库")
        conn = mysql.connector.connect(
            host='182.92.207.81',
            user='root',
            passwd='root12345',
            port=3306,
            db='myapp',
            auth_plugin='mysql_native_password'
        )
        try:
            cur = conn.cursor()  # 生成游标对象
            cur.execute("select * from movieLink where name = %s", (name,))
            result = cur.fetchall()
            if len(result) == 0:
                cur.execute("insert into movieLink (name, time, link) values (%s, %s, %s)",
                            (name, movie_time, link))
            else:
                cur.execute("update movieLink set link = %s, time = %s where name = %s",
                            (link, movie_time, name))
            cur.close()  # 关闭游标
        finally:
            conn.commit()
            conn.close()  # 关闭连接
    except Exception as error:
        print("保存", name, "到数据库出错，原因为：", error)


if __name__ == "__main__":
    main()
    print("爬取完毕")
