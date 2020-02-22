# coding=utf-8

"""
md5常用的操作函数
"""

import hashlib


def md5_str2hex(str):
    """
    对字符串进行MD5加密
    :param str: str, 待加密字符串
    :return: 已加密字符串
    """
    h = hashlib.md5()
    h.update(str.encode(encoding='utf-8'))
    return h.hexdigest()