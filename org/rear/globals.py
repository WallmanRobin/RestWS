# coding=utf-8

"""
rear平台环境的上下文类, 共用资源在此统一定义, 避免重复定义浪费资源, 该类还会通过反射将org.rear.uitl.cfg中的配置读取函数映射为类的属性
"""

import platform
import types
from flask import session, current_app
from sqlalchemy import create_engine

from org.rear.util import cfg


class RearContext():
    def __init__(self):
        self.reflectCfgMoudle()
        self.db_engine = self.initDBEngine()
        self.current_app = current_app

    def initDBEngine(self):
        j = self.dbConf
        connStr = j['type'] + '://' + j['user'] + ':' + j['password'] + '@' + j['host'] + ':' + j['port'] + '/' + j[
            'name']
        return create_engine(connStr, pool_size=j["pool_size"], max_overflow=j["max_overflow"],
                             pool_recycle=j["pool_recycle"], echo=True, echo_pool=True)

    def getSessionUserInfo(self):
        if 'current_user_proxy' in session:
            return session['current_user_proxy']
        return None

    def reflectCfgMoudle(self):
        l = dir(cfg)
        for e in dir(cfg):
            f = getattr(cfg, e)
            if isinstance(f, types.FunctionType):
                setattr(self, f.__name__, f())
