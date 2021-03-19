# -*- codeing = utf-8 -*-
# @Time : 2021/3/12 11:29
# @Author : 水印红枫
# @Software: PyCharm

# print("hello,world")
# print("这种标准化输出")
# age = 10
# print("这是变量：", age)
# print("这是格式化输出，我的年龄是：%d岁" % age)
# print("我的名字是%s，我的国籍是%s" % ("张三", "中国"))
# print("www", "baidu", "com")
# print("www", "baidu", "com", sep=".")
# print("hello", end="")
# print("world", end="\t")
# print("python", end="\n")
# print("nice to meet you")

# password = input("请输入密码：")
# print("你输入的密码是：", password)

# a = 10
# print(type(a))
#
# b = input("请输入：")
# b = int(b)
# print(type(b))

# if 0 and 1 > 0:
#     print(true)
# elif 1:
#     print("elif")
# else:
#     print(false)
# print("end")

# import random
#
# print(random.randint(0, 3))

#
# for i in range(1, 15, 3):
#     print(i)

# arr = ["aa", "bb"]
# for i in range(len(arr)):
#     print(arr[i])
#
# i = 0
# while i < len(arr):
#     print(arr[i])
#     i += 1
# else:
#     print(i)

# word1 = '这是一个句子'
# word2 = "这又是一个句子"
# word3 = """
#        这是好几个句子
# 这个是好几个句子
# """
# print(word1, word2, word3)

# my_str = "i'm a string"
# print(my_str[0:7:2])  # [起始位置：结束位置：步进值]
# print(my_str[0::2])
# print(my_str[::2])


# print("hello\tworld")
# print(r"hello\tworld")


# nameList = [1,'aa']
# print(type(nameList[0]),type(nameList[1])) #数组中可以同时存在不同的类型
#
# nameList.append("bb") # 增加数据
# nameList.extend(['cc','dd',"ee"]) #数据相连
# nameList.insert(1,"我是被insert进来的") # 在对应位置插入数据
# del nameList[0] # 删除指定的元素
# print("我就是被弹出并删除的那个：",nameList.pop()) #弹出并删除最后一个元素
# print("我就是被移出来的那个：cc",nameList.remove('cc')) #弹出并删除最后一个元素,如果有多个，默认删除第一个
# print(nameList)
# print("‘aa’是不是在数组中：",'aa' in nameList)
# print("‘aa’是不是不在数组中：",'aa' not in nameList)
# print("‘aa’在数组中指定范围中的位置：", nameList.index('aa',0,len(nameList))) #找不到会报错
# print("统计‘aa’在数组中出现的次数",nameList.count('aa'))
#
# nameList.reverse() #反转
# nameList.sort() # 排序

'''
tup1=() # 元组不能更改，可以相加放在新元组中，del可以删除整个元组
tup2=(20)
tup3=(20,)
print(type(tup1),type(tup2),type(tup3))
'''

# people={"name":"wuyanzu"}
# # print(people["aaa"]) #会报错
# print(people.get('aaa',"默认值为none"))

# del(people["name"]) #删除操作 del(people)可删除整个字典

# print(people.clear()) # 清空

# people={"name":"wuyanzu", "age":18}
# print(people.keys())
# print(people.values())
# print(people.items())
#
# for key,value in people.items():
#     print(key,value)
#
# myList = ["1","2","3"]
# print(enumerate(myList))
# for index,value in enumerate(myList):
#     print(index,value)

# def math (a,b):
#     return a//b,a*b
# a = int(input("请输入你的值："))
# b = int(input("请输入你的值："))
# c,d = math(a,b)
# print("%d和%d的商是：%d,积是：%d"%(a,b,c,d))

a = 100
def change():
     a=300


def change1():
    global a
    a = 400
change1()
change()
print(a)

