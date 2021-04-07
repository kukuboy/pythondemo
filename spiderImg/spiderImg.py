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
import os


# findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S) # re.S让.包含换行符
# src = re.findall(findImgSrc, html)[0]

def main():
    img = []
    for i in range(1, 2):
        try:
            print("--------------------开始爬取第%d页-----------------" % i)
            baseurl = "https://www.mzitu.com/page/" + str(i) + "/"
            dataList = getData(baseurl)
            bs = BeautifulSoup(dataList, "html.parser")
            needBody = bs.find("ul", id="pins").find_all("li")
            for x in needBody:
                try:
                    item = dict()
                    item["href"] = x.a["href"]
                    item["imgSrc"] = []
                    item["imgSrc"].append(x.a.img["data-original"])
                    getImgArray(item["href"], item["href"], item["imgSrc"])
                    item["title"] = x.span.a.get_text()
                    item["time"] = x.find(class_="time").get_text()
                    print("正在爬取---------------------")
                    img.append(item)
                except Exception as error:
                    print(error)
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
        response = urllib.request.urlopen(req, timeout=10)
        data = response.read().decode("utf-8")
    except Exception as e:
        if hasattr(e, "reason"):
            print(e.reason)
    return data


def getImgArray(href, source, data):
    print("寻找%s的子链接--------%d" % (source, len(data)))
    try:
        if not source:
            source = href
        dataList = getData(href)
        bs = BeautifulSoup(dataList, "html.parser")
        needBody = bs.find("div", class_="main-image").p.a
        data.append(needBody.img["src"])
        if source in needBody["href"]:
            getImgArray(needBody["href"], source, data)
    except Exception as error:
        print("获取系列图片出错，原因为：", error, href)


def saveData(data, name):
    # 保存到json
    try:
        print("---------------正在保存到json")
        f = open("./" + name + ".json", "w", encoding="utf-8")
        try:
            val = dict()
            val["time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            val["author"] = "水印红枫"
            val["data"] = data
            # ensure_ascii=True：默认输出ASCLL码，如果把这个该成False,就可以输出中文。
            # indent:参数根据数据格式缩进显示，读起来更加清晰。
            # skipkeys：默认值是False，如果dict的keys内的数据不是python的基本类型(str,unicode,int,long,float,bool,None)，设置为False时，就会报TypeError的错误。此时设置成True，则会跳过这类key 。
            # sort_keys = True:是告诉编码器按照字典排序(a到z)输出。如果是字典类型的python对象，就把关键字按照字典排序。
            # separators: 是分隔符的意思，参数意思分别为不同dict项之间的分隔符和dict项内key和value之间的分隔符，把：和，后面的空格都除去了。
            # check_circular：如果check_circular为false，则跳过对容器类型的循环引用检查，循环引用将导致溢出错误(或更糟的情况)。
            # allow_nan：如果allow_nan为假，则ValueError将序列化超出范围的浮点值(nan、inf、-inf)，严格遵守JSON规范，而不是使用JavaScript等价值(nan、Infinity、-Infinity)。
            # default：default(obj) 是一个函数，它应该返回一个可序列化的obj版本或引发类型错误。默认值只会引发类型错误。
            f.write(json.dumps(val, ensure_ascii=False, indent=2))
        finally:
            f.close()
    except Exception as error:
        print("保存到文件出错，原因为：", error)
    # 保存到excel
    try:
        print("--------------正在保存到excel")
        workBook = xlwt.Workbook(encoding="utf-8")
        try:
            workSheet = workBook.add_sheet(name, cell_overwrite_ok=True)
            col = ["详情地址", "图片地址", "图片标题", "图片时间"]
            for i in range(0, 4):
                workSheet.write(0, i, col[i])
            x = 1
            for item in data:
                y = 0
                for val in item.values():
                    if y == 1:
                        workSheet.write(x, y, json.dumps(val))
                    else:
                        workSheet.write(x, y, val)
                    y += 1
                x += 1
        finally:
            workBook.save("./" + name + ".xls")
    except Exception as error:
        print("保存到excel出错，原因为：", error)
    # 保存到文件

    print("---------------正在保存到文件")
    header = {"Authorization": "Bearer fklasjfljasdlkfjlasjflasjfljhasdljflsdjflkjsadljfljsda",
              "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36"}  # 设置http header
    for items in data:
        i = 1
        try:
            for item in items["imgSrc"]:

                print("--------------正在第%d个图片%s" % (i, item))
                rep = urllib.request.Request(item, headers=header)
                response = urllib.request.urlopen(rep, timeout=10)
                if response.getcode() == 200:
                    os.makedirs("./" + name + "/" + items["title"], exist_ok=True)
                    with open("./" + name + "/" + items["title"] + "/" + str(i) + ".jpg", "wb+") as f:
                        f.write(response.read())  # 将内容写入图片
                i += 1
        except Exception as error:
            print("保存到文件出错，原因为：", error)
    # 保存到mysql
    try:
        print("--------------正在保存到数据库")
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
                    cur.execute("insert into img (title, href, imgSrc, time) values (%s, %s, %s, %s)",
                                (i["title"], i["href"], json.dumps(i["imgSrc"]), i["time"]))
                else:
                    cur.execute("update img set imgSrc = %s where href = %s",
                                (json.dumps(i["imgSrc"]), i["href"]))
            cur.close()  # 关闭游标
        finally:
            conn.commit()
            conn.close()  # 关闭连接
    except Exception as error:
        print("保存到数据库出错，原因为：", error)


if __name__ == "__main__":
    main()
    print("爬取完毕")
