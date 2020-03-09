# -*- coding: utf-8 -*-
# 导入正则表达式模块
import re


def test_regex():
    """ 正则表达式测试

    :return: 输出测试串结果
    """
    test_str = r'<div data-num="131221" class="allNumBox j_allNumBox">'  # 测试数据
    # 正则表达式匹配
    regex_str = r'<div data-num="(\d+)" class="allNumBox j_allNumBox">'
    result = re.compile(regex_str, re.I)  # 预编译，re.I 不分大小写
    result = result.findall(test_str)  # 查找全部匹配串，并返回列表
    print(result)


def regex(text, regex_str):
    """ 获取智联招聘网中的职位信息

    :param regex_str: 正则表达式匹配规则
    :param text: 需要匹配的文本
    :return: 职位信息
    """
    result = re.compile(regex_str, re.I)  # 预编译，re.I 不分大小写
    return result.findall(text)


def url_regex(url):
    """ 验证输入数据中是否存在非法字符串
    :param url: 输入的url
    :return：如果url合法则返回True，如果url非法为False
    """
    regex_ = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        # domain...
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    url_list = regex_.findall(url)
    if len(url_list) > 0:
        return True
    else:
        return False


if __name__ == '__main__':
    test_regex()
