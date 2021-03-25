# -*- codeing = utf-8 -*-
# @Time : 2021/3/25 14:55
# @Author : 水印红枫
# @Software: PyCharm
from bs4 import BeautifulSoup  # 网页解析获取数据
import re  # 正则表达式，进行文字匹配
import urllib.request, urllib.error, urllib.parse  # 指定url获取网络数据
import xlwt  # 进行excel操作
import mysql.connector  # 进行数据库操作
import json
import time


# findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S) # re.S让.包含换行符
# src = re.findall(findImgSrc, html)[0]

def main():
    img = []
    for i in range(1, 100):
        baseurl = "https://www.mzitu.com/page/" + str(i) + "/"
        dataList = getData(baseurl)
        bs = BeautifulSoup(dataList, "html.parser")
        needBody = bs.find("ul", id="pins").find_all("li")
        for x in needBody:
            try:
                item = dict()
                item["href"] = x.a["href"]
                item["imgSrc"] = x.a.img["src"]
                item["title"] = x.span.a.get_text()
                item["time"] = x.find(class_="time").get_text()
                img.append(item)
            except Exception as error:
                print(error)
    saveName = "图片地址"
    saveData(img, saveName)


def getData(url):
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
    # 保存到文件
    try:
        f = open("./" + name + ".json", "w", encoding="utf-8")
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
    # 保存到excel
    try:
        try:
            workBook = xlwt.Workbook(encoding="utf-8")
            workSheet = workBook.add_sheet(name, cell_overwrite_ok=True)
            col = ["详情地址", "图片地址", "图片标题", "图片时间"]
            for i in range(0, 4):
                workSheet.write(0, i, col[i])
            x = 1
            for item in data:
                y = 0
                for val in item.values():
                    workSheet.write(x, y, val)
                    y += 1
                x += 1
        finally:
            workBook.save("./" + name + ".xls")
    except Exception as error:
        print("保存到excel出错，原因为：", error)
    # 保存到mysql
    try:
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
            for i in data:
                cur.execute("select * from img where href = %s", (i["href"],))
                result = cur.fetchall()
                if len(result) == 0:
                    s = cur.execute("insert into img (title, href, imgSrc, time) values (%s, %s, %s, %s)", (i["title"], i["href"], i["imgSrc"], i["time"]))
            cur.close()  # 关闭游标
        finally:
            conn.commit()
            conn.close()  # 关闭连接
    except Exception as error:
        print("保存到数据库出错，原因为：", error)


if __name__ == "__main__":
    main()
    print("爬取完毕")
