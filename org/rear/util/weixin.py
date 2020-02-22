# coding=utf-8

import urllib3

from org.rear import ctx

"""
微信服务常用的操作函数
"""

import requests


def getOpenid(code):
    """
    获得微信用户的openid
    :param code: str, 微信小程序登录登录后得到的用户码
    :return: str, openid字符串，失败返回空字符串''
    """
    j = getWeixinId(code)
    return j


def getWeixinId(code):
    """
    获得微信用户的OpenId、UnionId、Session_key
    :param code: str, 微信小程序登录登录后得到的用户码
    :return: {"openid":"OPENID","session_key":"SESSIONKEY","unionid":"UNIONID"}
    """
    c = ctx.weiXinConf
    req_params = {
        'appid': c['appid'],
        'secret': c['appsecret'],
        'js_code': code,
        'grant_type': 'authorization_code'
    }
    result = requests.get(c['appurl'],
                          params=req_params,
                          timeout=3,
                          verify=c['api_pem'] if (
                                      'api_pem' in c and c['api_pem'] != '') else urllib3.disable_warnings() == True)
    j = result.json()
    return j
