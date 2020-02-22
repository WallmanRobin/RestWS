#!flask/bin/python
# coding=utf-8
import hashlib
from flask_httpauth import HTTPBasicAuth

from org.rear.authorization.rbac.User.UserHandler import UserHandler


def verify_password_func(username, password):
    if username is None or username.isspace() or len(username)==0 or password is None or password.isspace() or len(password)==0:
        return False;
    #md5代码，启用删掉注释
    sp = hashlib.md5((username+password).encode('utf8')).hexdigest()
    p = get_password_func(username)
    up = hashlib.md5((username+p).encode('utf8')).hexdigest()
    return sp==up
    #简单非MD5测试
    # p = get_password_func(username)
    # return p == password

def get_password_func(username):
    h = UserHandler()
    u = h.getUserByCode(username)
    return u.password

def hash_password_func(username, password):
    # md5代码，启用删掉注释
    #return hashlib.md5(username+password)
    return password

class SysHttpBasicAuth(HTTPBasicAuth):
    def __init__(self, scheme=None, realm=None):
        super().__init__(scheme=None, realm=None)
        super().verify_password(verify_password_func)
        super().get_password(get_password_func)
        super().hash_password(hash_password_func)