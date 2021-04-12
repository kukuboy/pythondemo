# -*- codeing = utf-8 -*-
# @Time : 2021/4/12 13:17
# @Author : 水印红枫
# @Software: PyCharm

import pandas
import string

# 数组方式存入
p1 = pandas.Series([1, 2], index=list('ad'))
# print(type(p1), p1, sep="\n")
# 字典方式存入
p2_dict = {"name": "张三", "age": 18, "sex": "man"}
p2 = pandas.Series(p2_dict)
# print(p2)
p3 = pandas.Series([1, 2, 3, 4, 5], index=list(string.ascii_uppercase[5:10]))
# print(p3)
# 更改dtype
p3.astype(float)
# print(p3)

# 可通过索引或位置取值
print(p2[0], p2["name"], p2[0:2], p2[["age", "sex"]])
