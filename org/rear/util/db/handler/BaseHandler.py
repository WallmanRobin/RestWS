# coding: utf-8

"""
业务处理类的基类, 定义了业务处理常用的函数
"""

from org.rear.util.db.data.DataFactory import BaseDataFactory

class BaseHandler:
    def getData(self, dataClass):
        """
        获得数据操作类对象实例
        :param dataClass: class, 数据操作类
        :return: instance, 数据操作类实例
        """
        return BaseDataFactory().createData(dataClass)