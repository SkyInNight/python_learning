# -*- coding: utf-8 -*-
# 导入selenium测试模块
# 需要自行下载安装pip install selenium
from selenium import webdriver
from crawler_base import regular_expression
from selenium.common import exceptions
import os


def creat_firefox_webdriver():
    """ firefox browser_driver

    :return :返回webdriver
    """
    # 这里使用可以直接被selenium调用的firefox引擎进行无页面启动
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    browser_driver_ = webdriver.Firefox(
        executable_path=os.getcwd() + r"/driver/geckodriver.exe",  # 这里必须要是绝对路径
        firefox_binary=r"C:\Program Files\Mozilla Firefox\firefox.exe",
        options=options)
    return browser_driver_


def creat_edge_webdriver():
    """ edge_driver
    """
    # edge浏览器版本 17.17134
    browser_driver_ = webdriver.Edge(
        executable_path="driver/MicrosoftWebDriver.exe")
    return browser_driver_


def creat_chrome_webdriver():
    """ chrome_driver
    """
    # chrome_driver需要对应chrome浏览器的版本
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    # 设置chromium浏览器位置
    options.binary_location = r'C:\Program Files (x86)\Microsoft\Edge Beta\Application\msedge.exe'
    browser_driver_ = webdriver.Chrome(
        executable_path=os.getcwd() +
        r"/driver/msedgedriver.exe",
        options=options)
    return browser_driver_


class BrowserCrawler(object):
    def __init__(self, browser_type="firefox"):
        self._browser_type = browser_type
        if self._browser_type == "chrome":
            self._browser_driver = creat_chrome_webdriver()
        elif self._browser_type == "firefox":
            self._browser_driver = creat_firefox_webdriver()
        elif self._browser_type == "edge":
            self._browser_driver = creat_edge_webdriver()

    @property
    def browser_type(self):
        """

        :return: 返回browser_type，字符串类型
        """
        return self._browser_type

    @browser_type.setter
    def browser_type(self, value):
        """ 允许browser_type以属性的方式被外界调用

        :param value: 属性值只能是Edge,FireFox,Chrome
        :return:
        """
        type_list = ['edge', 'chrome', 'firefox']
        if value not in type_list:
            print('不存在{0}的浏览器参数，只允许输入"edge","chrome","firefox"'.format(value))
        else:
            self._browser_type = value

    def quit(self):
        self._browser_driver.quit()

    def browser_get(self, url_, regex_str_=None, data_=None):
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
            self._browser_driver.get(url_)
            print("正在爬取的url为：" + self._browser_driver.current_url)
            # 2. 判断是否需要进行正则表达式匹配
            if regex_str is None:
                result = self._browser_driver.page_source
            else:
                result = regular_expression.regex(
                    self._browser_driver.page_source, regex_str_)
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


def get_city_page_num(city_, browser_crawler_):
    """ 获取马蜂窝上一个城市的景点页数

    :param browser_crawler_: 浏览器爬虫
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
    result = browser_crawler_.browser_get(
        url_=url_city,
        regex_str_=regx,
        data_=data_)
    if len(result) > 0:
        return result[0]
    else:
        return "无法查询页码"


if __name__ == '__main__':
    browser_crawler = BrowserCrawler()
    try:
        # var reg = /^(http[s]?:\/\/)?([^\/]+)(.*)/ url正则表达式
        # 1. 获取智联招聘网站招聘岗位信息
        url = "https://xiaoyuan.zhaopin.com/search/jn=4"
        data = {"kw": "java"}
        regex_str = r'<span class="total"> (\d+) </span>'  # 正则表达式匹配
        text = browser_crawler.browser_get(
            url_=url,
            regex_str_=regex_str,
            data_=data)
        print(text)
        browser_crawler.quit()
        # 2. 获取马蜂窝一个城市的景点个数
        city_list = ['长沙', '衡阳', '湘潭']
        for city in city_list:
            text = get_city_page_num(city, browser_crawler)
            print("{0}的景点页数有：{1}".format(city, text))
    finally:
        browser_crawler.quit()
