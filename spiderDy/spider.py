# -*- codeing = utf-8 -*-
# @Time : 2021/7/21 11:26
# @Author : 水印红枫
# @Software: PyCharm

from bs4 import BeautifulSoup  # 网页解析获取数据
import urllib.request  # 指定url获取网络数据
from conf.db import my_connector

# findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S) # re.S让.包含换行符
# src = re.findall(findImgSrc, html)[0]
conn = my_connector()


def main():
    begin("https://dy.dytt8.net/html/gndy/dyzz/index.html", "GBK", "https://dy.dytt8.net")


def begin(url, charset, baseurl=""):
    dataList = getData(url, charset)
    bsList = BeautifulSoup(dataList, "html.parser")
    needBody = bsList.find_all('table', class_="tbspan")
    movie_list = []
    for x in needBody:
        try:
            movie_item = dict()
            movie_item["movie_time"] = x.find('font').get_text()
            item = x.find('a', class_="ulink")["href"]
            data = getData(baseurl + item, charset)
            if not data:
                continue
            bs = BeautifulSoup(data, "html.parser")
            movie_item["name"] = bs.find('div', class_="title_all").get_text()
            movie_item["link"] = bs.find('a', target="_blank")["href"]
            movie_list.append(movie_item)
        except Exception as error:
            print(error)
    saveData(movie_list)
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
        print("爬取", url, "页面")
        try:
            return urllib.request.urlopen(req).read().decode(charset)
        except Exception as error:
            print(url, error)
            return urllib.request.urlopen(req).read()
    except Exception as e:
        if hasattr(e, "reason"):
            print("抓取数据失败的原因是：", e.reason)
        else:
            print("抓取数据位置原因退出")
        # sys.exit(0)


def saveData(movie_list):
    # 保存到mysql
    cur = conn.cursor()
    try:
        for x in movie_list:
            try:
                print("正在保存", x["name"], "到数据库")
                cur.execute("select * from movieLink where name = %s", (x["name"],))
                result = cur.fetchall()
                if len(result) == 0:
                    cur.execute("insert into movieLink (name, time, link) values (%s, %s, %s)",
                                (x["name"], x["movie_time"], x["link"]))
                else:
                    cur.execute("update movieLink set link = %s, time = %s where name = %s",
                                (x["link"], x["movie_time"], x["name"]))
            except Exception as error:
                print("保存", x["name"], "到数据库出错，原因为：", error)
    except Exception as error:
        print("保存列表", movie_list, "到数据库出错，原因为：", error)
    finally:
        cur.close()
        conn.commit()


if __name__ == "__main__":
    main()
    conn.close()  # 关闭连接
    print("爬取完毕")
