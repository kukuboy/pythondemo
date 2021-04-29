# -*- codeing = utf-8 -*-
# @Time : 2021/4/29 11:23
# @Author : 水印红枫
# @Software: PyCharm
from appium import webdriver
from appium.webdriver.extensions.android.nativekey import AndroidKey

desired_caps = {
    "platformName": "Android",  # 被测手机是安卓
    "platformVersion": "10",  # 手机安卓版本
    "deviceName": "honor",  # 设备名，安卓手机可以随意填写
    "appPackage": "com.jingdong.app.mall",  # 启动APP Package名称
    "appActivity": ".main.MainActivity",  # 启动Activity名称
    "unicodeKeyboard": True,  # 使用自带输入法，输入中文时填True
    "resetKeyboard": True,  # 执行完程序恢复原来输入法
    "noReset": True,  # 不要重置App
    "newCommandTimeout": 6000,
    "automationName": "UiAutomator2"
    # "app": r"d:\apk\bili.apk",
}

driver = False
try:
    # 连接Appium Server，初始化自动化环境
    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    # 设置缺省等待时间
    driver.implicitly_wait(100)

    # # 如果有`青少年保护`界面，点击`我知道了`
    # iknow = driver.find_elements_by_id("text3")
    # if iknow:
    #     iknow.click()descriptionContains
    # 点击搜索框
    print("点击搜索框")
    driver.find_element_by_android_uiautomator(
        'new UiSelector().className("android.widget.TextView").descriptionContains("搜索框")').click()
    # 点击第一个历史记录
    print("点击第一个历史记录")
    driver.find_element_by_android_uiautomator(
        'new UiSelector().resourceId("com.jd.lib.search.feature:id/a_x")').click()
    # 点击对应的商品
    print("点击对应的商品")
    driver.find_element_by_android_uiautomator(
        'new UiSelector().className("android.widget.TextView").descriptionContains("茅台 飞天酱香型白酒 500ml")').click()
    # 点击购买
    print("点击购买")
    driver.find_element_by_android_uiautomator(
        'new UiSelector().resourceId("com.jd.lib.productdetail.feature:id/add_2_car")').click()
    # 提交订单
    print("提交订单")
    driver.find_element_by_android_uiautomator(
            'new UiSelector().resourceId("com.jd.lib.settlement.feature:id/a2x")').click()
    input('**** Press to quit..')
except Exception as error:
    print("错误是", error)
finally:
    driver.quit()
