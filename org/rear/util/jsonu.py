# coding=utf-8

"""
json常用的操作函数
"""

import json


def obj2Json(obj):
    """
    对象转为json
    :param obj: object, 待转换对象
    :return: json, json类型返回值
    """
    d = obj.__dict__
    j = json.dumps(d)
    return j


def json2Obj(cls, jsonStr):
    """
    json值转为对象实例
    :param cls: class, 要转换的目标对象类
    :param jsonStr: str, 待转换的json值
    :return: object, 对象实例
    """
    jo = json.loads(jsonStr)
    obj = cls()
    # 将字典转化为对象
    obj.__dict__ = jo
    return obj
