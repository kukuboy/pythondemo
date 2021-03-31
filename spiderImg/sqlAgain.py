# -*- codeing = utf-8 -*-
# @Time : 2021/3/31 13:34
# @Author : 水印红枫
# @Software: PyCharm

import xlrd  # 进行excel操作
import mysql.connector  # 进行数据库操作


def main():
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
            wordbook = xlrd.open_workbook("图片地址.xls")
            table = wordbook.sheet_by_name("图片地址")
            nrows = table.nrows
            cur = conn.cursor()  # 生成游标对象
            for i in range(1, nrows):
                cur.execute("select * from img where href = %s", (table.cell(i, 0).value,))
                result = cur.fetchall()
                if len(result) == 0:
                    cur.execute("insert into img (href, imgSrc, title, time) values (%s, %s, %s, %s)",
                                (table.cell(i, 0).value, table.cell(i, 1).value, table.cell(i, 2).value, table.cell(i, 3).value))
                else:
                    cur.execute("update img set imgSrc = %s where href = %s",
                                (table.cell(i, 1).value, table.cell(i, 0).value))
            cur.close()  # 关闭游标
        finally:
            conn.commit()
            conn.close()  # 关闭连接
    except Exception as error:
        print("保存到数据库出错，原因为：", error)


if __name__ == "__main__":
    main()
    print("程序结束")
