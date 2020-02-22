# coding=utf-8

import base64
import importlib
import json
import jwt
import logging
import time
from flask import current_app
from flask import session, request
from functools import wraps
from org.rear.authorization.proxy.User import UserProxy

from org.rear import ctx
from org.rear.authorization.rbac.User.UserHandler import UserHandler


def genJWTCode(user_code):
    """
    生成jwt密钥
    :param user_code: str, 用户代码
    :return: str, 生成的用户代码
    """
    p = {'iss': ctx.jwtIss, 'nbf': int(time.time()), 'user_code': user_code}
    lt = ctx.jwtLifeTime
    if lt != '-1':
        p['exp'] = int(time.time() + lt)
    jwt_code = str(jwt.encode(p, ctx.appSecretKey, ctx.jwtAlgorithm), 'utf-8')
    return jwt_code


def genLoginToken(user_code):
    """
    生成登录后的密钥
    :param user_code: str, 用户代码
    :param token: str,
    :return:
    """
    t = ctx.authType
    if t == 'jwt':
        return genJWTCode(user_code)
    else:
        return ''


def verifyFormKey(request):
    """
    校验从登录网页表格中的用户密码信息
    :param request: request, 登陆请求引用
    :return: UserProxy, 登录校验的结果用户, 校验失败返回None
    """
    user_code = request.args.get('user')
    pwd = request.args.get('pwd')
    h = UserHandler()
    d = h.getUserByCodePwd(user_code, pwd)
    if d:
        u = UserProxy(d, '0')
        return u
    return None


def verifyBasicKey(request):
    """
    校验 http basic auth登录
    :param request: 登陆请求引用
    :return: UserProxy, 登录校验的结果用户, 校验失败返回None
    """
    key = request.headers.get('Authorization')
    if key:
        key = key.replace('Basic ', '', 1)
        try:
            api_key = str(base64.b64decode(key), 'utf-8')
            upwd = api_key.split(':')
            if len(upwd) >= 2:
                h = UserHandler()
                d = h.getUserByCodePwd(upwd[0], upwd[1])
                if d:
                    u = UserProxy(d, '1')
                    return u
        except Exception as e:
            print(e)
    return None


def verifyMD5Key(request):
    """
    校验MD5密钥登录
    :param request: 登陆请求引用
    :return: UserProxy, 登录校验的结果用户, 校验失败返回None
    """
    param_name = ctx.loginParamName
    json = request.get_json()
    key = json[param_name]
    if key:
        api_key = str(base64.b64decode(key), 'utf-8')
        upwd = api_key.split(':')
        if len(upwd) >= 3 and ctx.appSecretKey == upwd[0]:
            h = UserHandler()
            d = h.getUserByHashCode(upwd[1], upwd[2])
            if d:
                token = genLoginToken(d.user_code)
                u = UserProxy(d, token)
                logger = logging.getLogger('rear')
                logger.info(d.name + '(' + d.user_code + ')已登入。')
                return u
    return None

def getLoginFunc():
    """
    从配置信息中获得登录校验函数
    :return: 校验函数的路径和名称
    """
    l = ctx.loginFunc
    r = []
    for e in l:
        r.append(e.split(':'))
    return r

def execLoginFunc(request):
    """
    执行配置信息中的登录校验函数
    :param request: 登陆请求引用
    :return: UserProxy, 登录校验的结果用户, 校验失败返回None
    """
    l = getLoginFunc()
    for e in l:
        m = importlib.import_module(e[0])
        f = getattr(m, e[1])
        r = f(request)
        if r:
            return r
    return None

def jwtCodeRequired(func):
    """
    前置jwt密钥校验函数语法糖, 检查当前用户是否持有有效的jwt密钥
    :param func: 待执行函数
    :return: 前置jwt密钥校验函数
    """
    @wraps(func)
    def decorated_jwt(*args, **kwargs):
        header_name = ctx.jwtHeaderName
        key = request.headers.get(header_name)
        if key:
            up = ctx.getSessionUserInfo()
            if up:
                if key != up.key:
                    return '秘钥与服务器不一致！', 401
            else:
                return '登录超时，根据秘钥无法找到在线用户！', 401
        return func(*args, **kwargs)
    return decorated_jwt

def rbacChecked(func):
    """
    角色权限校验函数语法糖, 检查当前用户是否有限期执行该函数
    :param func: 待执行函数
    :return: 角色权限校验函数
    """
    @wraps(func)
    def decorated_rbac(*args, **kwargs):
        r = ''
        up = ctx.getSessionUserInfo()
        if not up:
            r = '闲置已超时' + str(ctx.sessionLifeTime) + '秒，您目前是匿名身份。'
            return r, 403
        if request.method != 'OPTIONS':
            if up.roles.count(ctx.rootRole) == 0 and up.user_code != ctx.rootUser:
                fn = ''
                for k in ctx.current_app.view_functions:
                    if ctx.current_app.view_functions[k].__name__ == func.__name__ and ctx.current_app.view_functions[
                        k].__module__ == func.__module__:
                        fn = k
                        break
                e = {'endpoint': fn, 'method': request.method}
                if e not in up.endpoint:
                    r = r + '您未被授权使用该功能，请和管理员联系！'
                    return r , 403
        return func(*args, **kwargs)
    return decorated_rbac
