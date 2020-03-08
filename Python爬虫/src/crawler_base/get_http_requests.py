# -*- coding: utf-8 -*-
# 在python3中urllib模块中要用爬虫要调用其中的子模块Request
# python2中直接导入urllib模块即可
# python3中将urllib和urllib2合并到urllib中，urllib3为扩展库添加了多线程安全
from urllib import request, error


def method_read(url_):
    """ 使用read方法爬取网页全部信息

    :param url_: 需要爬取的网页url
    :return: 返回网页全部内容
    """
    response = request.urlopen(url_).read()
    return response


def method_readlines(url_):
    """ 使用read方法爬取网页全部信息

    :param url_: 需要爬取的网页url
    :return: 以每行文字为一个元素，按列表形式返回网页全部内容
    """
    response = request.urlopen(url_).readlines()
    return response


def method_readline(url_):
    """ 按行读取网页信息，并逐行处理网页

    :param url_: 需要爬取的网页url
    :return: 返回网页全部内容
    """
    response = request.urlopen(url_)
    context = ""
    while True:
        line = response.readline()
        if not line:
            break
        context += str(line).strip()
    return context


def get_http(url_, method):
    """ 获取网页全部信息并返回

    :param method: 调用的爬虫方法
    :param url_: 要爬取的网页url
    :return: 返回网页爬取的全部信息
    """
    try:
        response = method(url_)
    except error.HTTPError as e:
        # 打印错误原因
        print(e.reason)
        # 打印错误代码
        print(e.code)
        # 打印响应错误头
        print(e.headers)
        return "HTTPError"
    except error.URLError as e:
        # 打印错误原因，并返回异常内容
        print(e.reason)
        return "URLError"
    else:
        return response


if __name__ == '__main__':
    # urllib在处理https的请求中存在一定的问题，可能需要进行http安全认证，其次和python2.7中的urllib2又有一定的区别
    url = 'http://www.baidu.com'
    text = get_http(url, method_read)
    print("测试read方法返回结果" + str(text))
    text = get_http(url, method_readlines)
    print("测试readlines返回结果" + str(text))
    text = get_http(url, method_readline)
    print("测试readline返回结果" + text)
