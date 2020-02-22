# coding=utf-8

"""
配置文件的常用操作函数, 这里的所有函数调用都会在org.rear.RearContext中被反射为RearContext类的属性
"""

import json
import os
import platform
from os import path


def cfgEnv():
    rootfile = cfgRootUrl()
    with open(rootfile, 'r') as f:
        return json.load(f)['environment']


def cfgRootUrl():
    """
    从当前目录回溯找到根配置文件
    :return: str, 根配置文件的路径
    """
    d = __file__
    for i in range(4):
        d = path.dirname(d)
    cfgfile = os.path.join(d, 'root.json')
    if not os.path.isfile(cfgfile):
        cfgfile = 'root.json'
    return cfgfile


def cfgUrl():
    """
    从当前目录回溯找到配置文件
    :return: str, 配置文件的路径
    """
    o = cfgEnv()
    f = 'config.json' + '.' + o
    d = __file__
    for i in range(4):
        d = path.dirname(d)
    cfgfile = os.path.join(d, f)
    if not os.path.isfile(cfgfile):
        cfgfile = f
    return cfgfile


def dbConf():
    """
    读取配置文件中配置的数据库部分的配置信息
    :return: Dict, 数据库配置信息的json对象
    """
    cfgfile = cfgUrl()
    with open(cfgfile, 'r') as f:
        j = json.load(f)
        if 'database' in j:
            return j['database']
    return None


def weiXinConf():
    """
    读取配置文件中配置的微信服务部分的配置信息
    :return: Dict, 微信服务配置信息的json对象
    """
    cfgfile = cfgUrl()
    with open(cfgfile, 'r') as f:
        j = json.load(f)
        if 'weixin' in j:
            return j['weixin']
    return ''


def appSecretKey():
    """
    读取配置文件中配置的服务器安全秘钥信息
    :return: str, 服务器安全秘钥字符串
    """
    cfgfile = cfgUrl()
    with open(cfgfile, 'r') as f:
        j = json.load(f)
        if 'authorization' in j and 'secret_key' in j['authorization']:
            return j['authorization']['secret_key']
    return ''


def authType():
    """
    读取配置文件中配置的服务器认证类型信息
    :return: str, 服务器认证类型信息, 目前是jwt
    """
    cfgfile = cfgUrl()
    with open(cfgfile, 'r') as f:
        j = json.load(f)
        if 'authorization' in j and 'auth_type' in j['authorization']:
            return j['authorization']['auth_type']
    return ''


def sessionCfg():
    """
    读取配置文件中配置的服务器session配置节点
    :return: json, 服务器session配置节点
    """
    cfgfile = cfgUrl()
    with open(cfgfile, 'r') as f:
        j = json.load(f)
        if 'session' in j:
            return j['session']
    return None


def jwtLifeTime():
    """
    读取配置文件中配置的服务器jwt秘钥的有效时间
    :return: str, 服务器jwt秘钥的有效时间, 单位是秒
    """
    cfgfile = cfgUrl()
    with open(cfgfile, 'r') as f:
        j = json.load(f)
        if 'authorization' in j and 'jwt_life_time' in j['authorization']:
            return j['authorization']['jwt_life_time']
    return -1


def loginParamName():
    """
    读取配置文件中配置的客户端传递登录校验密钥的参数名
    :return: str, 客户端传递登录校验密钥的参数名
    """
    cfgfile = cfgUrl()
    with open(cfgfile, 'r') as f:
        j = json.load(f)
        if 'authorization' in j and 'loginParam' in j['authorization']:
            return j['authorization']['loginParam']
    return ''


def loginFunc():
    """
    读取配置文件中配置的登录校验函数
    :return: str, 登录校验函数
    """
    cfgfile = cfgUrl()
    with open(cfgfile, 'r') as f:
        j = json.load(f)
        if 'authorization' in j and 'loginFunc' in j['authorization']:
            return j['authorization']['loginFunc']
    return ''


def jwtIss():
    """
    读取配置文件中配置的服务器jwt发行单位的信息
    :return: str, 服务器jwt发现单位的名称
    """
    cfgfile = cfgUrl()
    with open(cfgfile, 'r') as f:
        j = json.load(f)
        if 'authorization' in j and 'jwt_iss' in j['authorization']:
            return j['authorization']['jwt_iss']
    return ''


def jwtAlgorithm():
    """
    读取配置文件中配置的服务器jwt的加密方法
    :return: str, 服务器jwt的加密方法
    """
    cfgfile = cfgUrl()
    with open(cfgfile, 'r') as f:
        j = json.load(f)
        if 'authorization' in j and 'jwt_algorithm' in j['authorization']:
            return j['authorization']['jwt_algorithm']
    return ''


def jwtHeaderName():
    """
    读取配置文件中配置的客户端传输jwt值时的键值名
    :return: str, 客户端传输jwt值时的键值名
    """
    cfgfile = cfgUrl()
    with open(cfgfile, 'r') as f:
        j = json.load(f)
        if 'authorization' in j and 'jwt_header_name' in j['authorization']:
            return j['authorization']['jwt_header_name']
    return ''


def rootRole():
    """
    读取配置文件中配置的根角色名
    :return: str, 根角色名
    """
    cfgfile = cfgUrl()
    with open(cfgfile, 'r') as f:
        j = json.load(f)
        if 'authorization' in j and 'root_role' in j['authorization']:
            return j['authorization']['root_role']
    return ''


def rootUser():
    """
    读取配置文件中配置的根用户名
    :return: str, 根用户名
    """
    cfgfile = cfgUrl()
    with open(cfgfile, 'r') as f:
        j = json.load(f)
        if 'authorization' in j and 'root_user' in j['authorization']:
            return j['authorization']['root_user']
    return ''


def portraitBase():
    """
    读取配置文件中配置的头像文件根目录
    :return: str, 头像文件根目录
    """
    cfgfile = cfgUrl()
    with open(cfgfile, 'r') as f:
        j = json.load(f)
        if 'image' in j and 'portrait' in j['image']:
            return j['image']['portrait']
    return ''


def smtpConf():
    """
    读取配置文件中配置的smtp服务器信息
    :return: json, smtp服务器信息节点
    """
    cfgfile = cfgUrl()
    with open(cfgfile, 'r') as f:
        j = json.load(f)
        if 'smtp' in j:
            return j['smtp']
    return None


def mailConf():
    """
    读取配置文件中配置的邮件收发用户信息
    :return: json, 邮件收发用户信息节点
    """
    cfgfile = cfgUrl()
    with open(cfgfile, 'r') as f:
        j = json.load(f)
        if 'mail' in j:
            return j['mail']
    return None


def xlsConf():
    """
    读取配置文件中配置的Excel信息
    :return: json, Excel配置信息节点
    """
    cfgfile = cfgUrl()
    with open(cfgfile, 'r') as f:
        j = json.load(f)
        if 'xls' in j:
            return j['xls']
    return None
