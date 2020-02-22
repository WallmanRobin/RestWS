# coding: utf-8

"""
业务处理工厂类的基类, 定义了业务处理工厂常用的函数
"""

class BaseHandlerFactory:
    def createHandler(self, handlerClass):
        """
        创建生成业务处理类实例
        :param handlerClass: class, 业务处理类
        :return: instance,  业务处理类实例
        """
        return handlerClass()
