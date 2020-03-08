# -*- coding: utf-8 -*-
# 导入selenium测试模块
# 需要自行下载安装pip install selenium
from selenium import webdriver
from crawler_base import regular_expression
from selenium.common import exceptions
import os


""" firefox browser_driver
"""
# 这里使用可以直接被selenium调用的firefox引擎进行无页面启动
options = webdriver.FirefoxOptions()
options.add_argument('--headless')
browser_driver = webdriver.Firefox(
    executable_path=os.getcwd() + r"/driver/geckodriver.exe",  # 这里必须要是绝对路径
    firefox_binary=r"C:\Program Files\Mozilla Firefox\firefox.exe",
    options=options)


""" edge_driver
# edge浏览器版本 17.17134
browser_driver = webdriver.Edge(executable_path="driver/MicrosoftWebDriver.exe")
"""

""" chrome_driver
# chrome_driver需要对应chrome浏览器的版本
options = webdriver.ChromeOptions()
options.add_argument('--headless')
# 设置chromium浏览器位置
options.binary_location = r'C:\Program Files (x86)\Microsoft\Edge Beta\Application\msedge.exe'
browser_driver = webdriver.Chrome(executable_path=os.getcwd()+r"/driver/msedgedriver.exe", options=options)
"""


def browser_get(url_, regex_str_=None, data_=None):
    """ 调用模拟浏览器爬虫

    :param data_: url后需要添加的参数,字典类型传入
    :param url_: 需要爬取的网页url
    :param regex_str_: 正则表达式匹配规则
    :return: 返回爬取结果
    """
    # 判断输入的url是否合法
    if not regular_expression.url_regex(url_):
        return "输入非法url"
    # 1. 将附加的属性值加入url中
    if data_ is not None:
        for key in data_:
            url_ += "&" + key + "=" + data_[key]
    try:
        browser_driver.get(url_)
        print("正在爬取的url为：" + browser_driver.current_url)
        # 2. 判断是否需要进行正则表达式匹配
        if regex_str is None:
            result = browser_driver.page_source
        else:
            result = regular_expression.regex(
                browser_driver.page_source, regex_str_)
        return result
    except exceptions.TimeoutException as e:
        print(e)
        return "TimeoutException"
    except exceptions.ErrorInResponseException as e:
        print(e)
        return "UnknownMethodException"
    except exceptions.WebDriverException as e:
        print(e)
        return "WebDriverException"


def get_city_page_num(city_):
    """ 获取马蜂窝上一个城市的景点页数

    :param city_: 城市名
    :return: 返回景点总共页数
    """
    url_city = "http://www.mafengwo.cn/search/q.php?"
    regx = r'data-page="(\d+)" rel="nofollow">末页</a>'  # 设置用于获取页数的正则表达式
    data_ = {
        "t": "pois",
        "p": "1",
        "q": city_,  # 设置要查询的城市参数
        "kt": "1"
    }
    result = browser_get(url_=url_city, regex_str_=regx, data_=data_)
    return result[0]


if __name__ == '__main__':
    # var reg = /^(http[s]?:\/\/)?([^\/]+)(.*)/ url正则表达式
    # 1. 获取智联招聘网站招聘岗位信息
    url = "https://xiaoyuan.zhaopin.com/search/jn=4"
    data = {"kw": "java"}
    regex_str = r'<span class="total"> (\d+) </span>'  # 正则表达式匹配
    text = browser_get(url_=url, regex_str_=regex_str, data_=data)
    print(text)
    # 2. 获取马蜂窝一个城市的景点个数
    city_list = ['长沙', '衡阳', '湘潭']
    for city in city_list:
        text = get_city_page_num(city)
        print("{0}的景点页数有：{1}".format(city, text))
    browser_driver.close()
    browser_driver.quit()
