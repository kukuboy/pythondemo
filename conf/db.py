# -*- codeing = utf-8 -*-
# @Time : 2021/7/22 13:33
# @Author : 水印红枫
# @Software: PyCharm

import mysql.connector


def my_connector():
    # 保存到mysql
    try:
        print("--------------正在连接到数据库")
        return mysql.connector.connect(
            host='182.92.207.81',
            user='root',
            passwd='root12345',
            port=3306,
            db='myapp',
            auth_plugin='mysql_native_password'
        )
    except Exception as error:
        print("连接数据库出错:", error)
