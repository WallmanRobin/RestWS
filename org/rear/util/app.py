# coding=utf-8

"""
系统常用的操作函数
"""

import json
import logging
import sys
from flask import request


def packageResponse(o, cb="callback"):
    """
    封装返回的json对象, 自动判断采用是否采用jsonp的组装方式
    :param o: Dict或者List, 要封装的列表或字典类对象
    :param cb: str, jsonp的封装回调函数名
    :return: str, 封装返回的json字符串
    """
    c = request.args.get(cb)
    if c is not None:
        return c + '(' + json.dumps(o) + ')'
    else:
        return json.dumps(o)

def packageDate(e):
    """
    将日期类型转变为格式字符串, 如果是None返回空字符串''
    :param e: Date(sys.modules[__name__] + '.' + __name__ + ': '+ err)日期类型对象
    :return: str, 日期格式的字符串
    """
    try:
        return '' if e is None else e.strftime("%Y-%m-%d")
    except Exception as err:
        logger = logging.getLogger('rear')
        logger.error(sys.modules[__name__] + '.' + __name__ + ': ' + err)
    return ''

def packageTimeStamp(e):
    """
    将时间戳类型转变为格式字符串, 如果是None返回空字符串''
    :param e: Timestamp, 时间戳类型对象
    :return: str, 时间戳格式的字符串
    """
    try:
        return '' if e is None else e.strftime("%Y-%m-%d %H:%M:%S")
    except Exception as err:
        logger = logging.getLogger('rear')
        logger.error(sys.modules[__name__] + '.' + __name__ + ': ' + err)
    return ''