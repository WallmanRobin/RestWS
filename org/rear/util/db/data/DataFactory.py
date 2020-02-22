# coding=utf-8

"""
所有数据工厂类的基类, 定义了数据库配置信息操作常用的变量和函数
"""

import json
from flask import app, current_app
from sqlalchemy.orm import sessionmaker, scoped_session

from org.rear import ctx


class BaseDataFactory:
    def __init__(self):
        """
        初始化函数
        """
        self.dbstr = ''

    def createData(self, dataClass):
        """
        创建生成数据操作类对象实例
        :param dataClass: class, 数据操作类
        :return: instance, 数据操作类实例
        """
        session = scoped_session(sessionmaker(bind=ctx.db_engine))
        return dataClass(session())
