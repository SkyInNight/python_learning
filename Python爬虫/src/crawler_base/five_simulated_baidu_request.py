# -*- coding: utf-8 -*-
from urllib import request as req
# Python3中解码编码模块放入parse中，Python2中直接调用urllib
import urllib.parse
import urllib.error


def bai_du_get(keyword_):
    url = r"http://www.baidu.com/s"
    data = {
        "ie": "UTF-8",
        "wd": keyword_
    }
    data = urllib.parse.urlencode(data)
    url = url + "?" + data
    try:
        response = req.urlopen(url)
        return response.read(1000)
    except urllib.error.HTTPError as e:
        print("网页出错了错误原因：{0}，错误码{1}".format(e.reason, e.code))
    except urllib.error.URLError as e:
        print("url出现未知错误错误原因：{0}".format(e.reason))


if __name__ == '__main__':
    keyword = "有道"
    print(bai_du_get(keyword))
