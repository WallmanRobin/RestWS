# coding=utf-8

"""
图片常用的操作函数
"""

import os

from org.rear.util import cfg


def loadCartoonPortraits():
    """
    获得系统中卡通头像的所有图片
    :return: list, 卡通头像所有图片的路径列表
    """
    l = []
    base = cfg.portraitBase()
    base = base + '/cartoon/'
    dir = os.listdir(base)

    for e in dir:
        if os.path.isfile(base + e):
            l.append(e)
    return l