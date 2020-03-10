# -*- coding: utf-8 -*-
from crawler_base import four_set_headers_param as set_headers_param
from crawler_base import two_regular_expression as regular_expression
from urllib import request as req
from urllib import parse, error


def zhi_lian_get(keyword):
    """

    :param keyword:
    :return:
    """
    url = r"https://xiaoyuan.zhaopin.com/search/jn=4&"
    regex_str = r'<span class="total"> (\d+) </span>'  # 正则表达式匹配
    data = {
        "kw": keyword
    }
    request = common_request(url, data)
    try:
        response = req.urlopen(request)
        result = regular_expression.regex(str(response.read()), regex_str)
        return result
    except error.HTTPError as e:
        print("网页出错了错误原因：{0}，错误码{1}".format(e.reason, e.code))
    except error.URLError as e:
        print("url出现未知错误错误原因：{0}".format(e.reason))
    except Exception as e:
        print("未知代码错误，错误原因：{0}".format(e))


def common_request(url_, params):
    """ 通用header头参数设置函数

    :param url_: 网页url
    :param params: 需要添加的get参数
    :return: 返回设置好headers的请求对象
    """
    data = parse.urlencode(params)
    url_ = url_ + data
    # 设置headers请求头
    headers = {
        "User-Agent": set_headers_param.set_user_agent("PC"),
        "Content-Type": "text/html; charset=utf-8"
    }
    request = req.Request(url_, headers=headers)
    return request


if __name__ == '__main__':
    print(zhi_lian_get("python"))
