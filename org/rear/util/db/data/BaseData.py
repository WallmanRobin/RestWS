# coding=utf-8

"""
所有数据操作类的基类, 定义了数据库操作常用的函数
"""

import sys
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker

from org.rear import ctx


class BaseData:
    def __init__(self, session):
        """
        初始化函数,生成并存储数据库引擎和会话
        :param session: 数据库链接session
        """
        self.session = session

    def commit(self):
        """
        提交实例中现有的数据写入操作
        :return: 无返回值
        """
        self.session.commit()

    def rollback(self):
        """
        回滚实例中现有的数据写入操作
        :return: 无返回值
        """
        self.session.rollback()

    def addRecord(self, obj):
        """
        新增一条记录
        :param obj: 待写入数据库的模型数据实例
        :return:
        """
        self.session.add(obj)