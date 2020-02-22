# coding=utf-8

from flask import Blueprint
from flask import request
from flask import session, abort

from org.rear.authorization.auth import execLoginFunc
from org.rear.util import cfg
from org.rear.util.app import packageResponse

authorize_bp = Blueprint('Authorize', __name__)

@authorize_bp.route('/logout',methods=['POST'])
def logout():
    """
    用户登出
    :return: touple, 返回文本, 返回值
    """
    session.clear()
    return 'Logout', 200

@authorize_bp.route('/login',methods=['Post'])
def login():
    """
    用户登录
    :return: touple, 返回文本, 返回值
    """
    user_proxy = execLoginFunc(request)
    if user_proxy:
        # session.permanent = True #必须permanent = True, session才生效
        session['current_user_proxy'] = user_proxy
        return packageResponse({'data':{'token': user_proxy.key}})
    else:
        return '登录失败，用户或者密码错误！', 401
