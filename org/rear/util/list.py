# coding: utf-8

"""
list常用的操作函数
"""

def eliminateListDups(l):
    """
    删除列表中重复的元素
    :param l: list, 待处理的列表
    :return: list, 已去重的列表
    """
    a = []
    for e in l:
        if not e in a:
            a.append(e)
    return a