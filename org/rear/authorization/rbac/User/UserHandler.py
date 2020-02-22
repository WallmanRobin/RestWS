# coding: utf-8

"""
用户业务处理类, 该类函数负责进行数据库事务提交
"""

import logging
import sys
from org.rear.util.db.handler.BaseHandler import BaseHandler

from org.rear import ctx
from org.rear.authorization.rbac.Role.RoleHandler import RoleHandler
from org.rear.authorization.rbac.User.UserData import UserData
from org.rear.util.md5 import md5_str2hex


class UserHandler(BaseHandler):
    def getUserByCode(self, user_code, status='A'):
        """
        根据用户代码查询用户
        :param user_code: str, 用户代码
        :param status: str, 查询状态, 为''空字符串时表示不查询状态
        :return: User, 返回用户信息, 查询不到返回None
        """
        d = self.getData(UserData)
        u = d.getUserByCode(user_code, status)
        return u

    def getUser(self, params, status='A'):
        """
        更加用户名或者名称模糊查询用户
        :param params: json, 查询用户代码和名字({'user_code': str, 'name': str})
        :param status: str, 查询状态, 为''空字符串时表示不查询状态
        :return: list, 用户数据列表
        """
        user_code = params['user_code']
        name = params['name']
        d = self.getData(UserData)
        r = []
        if user_code and user_code != '':
            r = d.getUserLikeCode(user_code, status)
        elif name and name != '':
            r = d.getUserLikeName(name, status)
        else:
            r = d.listUsers(status)
        return r

    def getUserByHashCode(self, user_code, hash_code, status='A'):
        """
        根据用户代码和秘钥查询用户
        :param user_code: str, 用户名称
        :param hash_code: str, 秘钥
        :param status: str, 查询状态, 为''空字符串时表示不查询状态
        :return: User, 返回用户信息, 查询不到返回None
        """
        d = self.getData(UserData)
        u = d.getUserByHashCode(user_code, hash_code, status)
        return u

    def getUserByCodePwd(self, user_code, password, status='A'):
        """
        根据用户代码和密码查询用户
        :param user_code: str, 用户名称
        :param password: str, 秘钥
        :param status: str, 查询状态, 为''空字符串时表示不查询状态
        :return: User, 返回用户信息, 查询不到返回None
        """
        d = self.getData(UserData)
        u = d.getUserByCodePwd(user_code, password, status)
        return u

    def getUserRolesByCode(self, user_code, status='A'):
        """
        获得用户的角色(不从角色树中继承)
        :param user_code: str, 用户代码
        :param status: str, 查询状态, 为''空字符串时表示不查询状态
        :return: list, 返回角色信息列表
        """
        d = self.getData(UserData)
        ur = d.getDirRolesByCode(user_code, status)
        return ur

    def getUserRolesDataByCode(self, user_code, status='A'):
        """
        获得用户的角色树数据
        :param user_code: str, 用户角色代码
        :param status: str, 查询状态, 为''空字符串时表示不查询状态
        :return: dict, 以角色为顶节点的树列表([{'role_code': str, 'name': str, 'status': boolean, children:[]}])
        """
        d = self.getData(UserData)
        r = d.getDirRolesByCode(user_code, status)
        rl = []
        h = RoleHandler()
        for e in r:
            rl.append(h.getRoleTreeData(e.role_code))
        return rl

    def updateUserByCode(self, user_code, name='', password='', hash_code='', phone='', email='', user_type='',
                         status=''):
        """
        更新用户信息
        :param user_code: str, 用户代码
        :param name: str, 用户姓名
        :param password: str, 用户密码
        :param hash_code: str, 用户秘钥
        :param phone: str, 手机号码
        :param email: str, 电子邮箱
        :param user_type: str, 用户类型
        :param status: str, 用户状态
        :return: int, 0-更新成功, -1-更新失败, -2-提交时失败
        """
        d = self.getData(UserData)
        r = d.updateUserByCode(user_code, name, password, hash_code, phone, email, user_type, status)
        if r == 0:
            try:
                d.commit()
            except Exception as err:
                logger = logging.getLogger('rear')
                logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
                r = -2
        return r

    def getUserData(self, params):
        """
        根据用户代码或者用户名模糊查询用户数据
        :param params: json, 查询用户代码和名字({'user_code': str, 'name': str})
        :return: list, 包含基本信息、角色信息和头像信息的用户数据列表
        """
        l = []
        u = self.getUser(params)
        if len(u) > 0:
            for e in u:
                r = self.getUserRolesDataByCode(e.user_code, status='')
                a = self.getUserAvatarByCode(e.user_code)
                l.append({'user_code': e.user_code, 'name': e.name, 'status': True if e.status == 'A' else False,
                          'password': '', 'phone': e.phone, 'email': e.email, 'avatar': a.avatar if a else '',
                          'role': r})
        return l

    def listUsers(self, status='A'):
        """
        列出所有用户
        :param status: str, 查询状态, 为''空字符串时表示不查询状态
        :return: list, 用户列表
        """
        d = self.getData(UserData)
        l = d.listUsers(status)
        return l

    def updateUserData(self, data):
        """
        更新用户数据(包括用户权限)
        :param data: json, 用户数据({'user_code': str, 'name': str, 'phone':str, 'email': str, 'status': status, role:[]})
        :return: int, 0-更新成功, -1-更新用户信息失败, -2-更新用户角色信息失败, -3-提交时失败
        """
        d = self.getData(UserData)
        user_code = data['user_code']
        name = data['name']
        phone = data['phone']
        email = data['email']
        status = 'A' if data['status'] == True else 'I'
        u = d.getUserByCode(user_code)
        r = 0
        if u:
            r = d.updateUserByCode(user_code, name=name, phone=phone, email=email, status=status)
        else:
            r = d.addUser(user_code, name=name, phone=phone, email=email, status=status)
        if r != 0:
            return -1
        role = [e for e in data['role'] if 'role_code' in e]
        r = d.bulkUpdateUserRole(user_code, [e['role_code'] for e in role])
        if r < 0:
            d.rollback()
            return -2
        try:
            d.commit()
        except Exception as err:
            logger = logging.getLogger('rear')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
            r = -3
        return r

    def setPassword(self, user_code, password):
        """
        设置用户秘钥
        :param user_code: str, 用户代码
        :param password: str, 用户密码
        :return: int, 0-生成成功, -1-写入数据库失败, -2-生成秘钥失败, -3-提交时失败
        """
        r = 0
        key = ctx.appSecretKey + ':' + user_code + ':' + password
        try:
            hashcode = md5_str2hex(key)
        except Exception as err:
            logger = logging.getLogger('rear')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
            return -2
        d = self.getData(UserData)
        r = d.updateUserByCode(user_code=user_code, password=password, hash_code=hashcode)
        if r == 0:
            try:
                d.commit()
            except Exception as err:
                logger = logging.getLogger('rear')
                logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
                r = -3
        return r

    def authenticateUser(self, code, pwd, role):
        """
        验证用户代码、密码和角色
        :param user_code: str, 用户代码
        :param pwd: str, 用户密码
        :param role_code: 角色代码
        :return: list, 返回查询条件的用户列表
        """
        d = self.getData(UserData)
        return d.authenticateUser(code, pwd, role)

    def getUserAvatarByCode(self, code):
        """
        获得用户头像信息
        :param user_code: str, 用户代码
        :return: UserAvatar, 返回用户头像信息, 失败返回None
        """
        d = self.getData(UserData)
        return d.getUserAvatarByCode(code)


    def pushUserAvatar(self, data):
        """
        更新用户头像信息
        :param data: json, 用户头像信息({'user_code': str, 'avatar': str})
        :return: int, 0-更新成功, -1-写入数据库失败, -2-提交时失败
        """
        d = self.getData(UserData)
        user_code = data['user_code'] if 'user_code' in data else ''
        avatar = data['avatar'] if 'avatar' in data else ''
        a = d.getUserAvatarByCode(user_code)
        r = 0
        if a:
            r = d.updateAvatarByCode(user_code, avatar)
        else:
            r = d.addUserAvatar(user_code, avatar)
        if r == 0:
            try:
                d.commit()
            except Exception as err:
                logger = logging.getLogger('rear')
                logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
                r = -2
        return r

    def pushUserWeixin(self, user_code, openid_mini="", openid_offi="", openid_app="", unionid=""):
        """
        新增用户的微信信息
        :param user_code: str, 用户代码
        :param openid_mini: str, 用户在小程序的openid
        :param openid_offi: str, 用户在公众号的openid
        :param openid_app: str, 用户在app的openid
        :param unionid: str, 用户在微信平台的unionid
        :return: int, 0-更新成功, -1-写入数据库失败, -2-提交时失败
        """
        d = self.getData(UserData)
        a = d.getUserWeixinByCode(user_code)
        r = 0
        if a:
            r = d.getUserWeixinByCode(user_code, openid_mini, openid_offi, openid_app, unionid)
        else:
            r = d.getUserWeixinByCode(user_code, openid_mini, openid_offi, openid_app, unionid)
        if r == 0:
            try:
                d.commit()
            except Exception as err:
                logger = logging.getLogger('rear')
                logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
                r = -2
        return r
