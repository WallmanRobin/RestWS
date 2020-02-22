# coding: utf-8

"""
用户操作类, 该类的函数不会进行数据库事务提交
"""

import logging
import sys
from org.rear.util.db.data.BaseData import BaseData
from sqlalchemy.orm import aliased

from org.rear.authorization.rbac.Role.RoleModel import Role
from org.rear.authorization.rbac.User.UserModel import User, UserRole, UserAvatar, UserWeixin
from org.rear.util.tree.TreeModel import TreeNode


class UserData(BaseData):
    def addUser(self, user_code, name='', password='', hash_code='', phone='', email='', user_type='', status='A'):
        """
        新增用户
        :param user_code: str, 用户代码
        :param name: str, 用户姓名
        :param password: str, 用户密码
        :param hash_code: str, 用户秘钥
        :param phone: str, 手机号码
        :param email: str, 电子邮箱
        :param user_type: str, 用户类型
        :param status: str, 用户状态
        :return: int, 0-新增成功, -1-新增失败
        """
        try:
            user = User(user_code, name, password, hash_code, phone, email, user_type, status)
            self.addRecord(user)
        except Exception as err:
            logger = logging.getLogger('rear')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
            return -1
        return 0

    def getUserLikeCode(self, user_code, status='A'):
        """
        根据用户代码模糊查询用户
        :param user_code: str, 用户代码
        :param status: str, 查询状态, 为''空字符串时表示不查询状态
        :return: list, 返回用户列表
        """
        l = []
        try:
            u = aliased(User, name='u')
            qry = self.session.query(u)
            qry = qry.filter(u.user_code.like('%'+user_code+'%'))
            if status != '':
                qry = qry.filter(u.status == status)
            l = qry.all()
        except Exception as err:
            logger = logging.getLogger('rear')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
        return l

    def getUserLikeName(self, name, status='A'):
        """
        根据用户代码模糊查询用户
        :param name: str, 用户名称
        :param status: str, 查询状态, 为''空字符串时表示不查询状态
        :return: list, 返回用户列表
        """
        l = []
        try:
            u = aliased(User, name='u')
            qry = self.session.query(u)
            qry = qry.filter(u.name.like('%'+name+'%'))
            if status != '':
                qry = qry.filter(u.status == status)
            l = qry.all()
        except Exception as err:
            logger = logging.getLogger('rear')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
        return l

    def getUserByCode(self, user_code, status='A'):
        """
        根据用户代码查询用户
        :param user_code: str, 用户代码
        :param status: str, 查询状态, 为''空字符串时表示不查询状态
        :return: User, 返回用户信息, 查询不到返回None
        """
        d = None
        try:
            u = aliased(User, name='u')
            qry = self.session.query(u)
            qry = qry.filter(u.user_code == user_code)
            if status != '':
                qry = qry.filter(u.status == status)
            d = qry.first()
        except Exception as err:
            logger = logging.getLogger('rear')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
        return d

    def getUserByName(self, name, status='A'):
        """
        根据用户名称查询用户
        :param name: str, 用户名称
        :param status: str, 查询状态, 为''空字符串时表示不查询状态
        :return: User, 返回用户信息, 查询不到返回None
        """
        d = None
        try:
            u = aliased(User, name='u')
            qry = self.session.query(u)
            qry = qry.filter(u.name == name)
            if status != '':
                qry = qry.filter(u.status == status)
            d = qry.first()
        except Exception as err:
            logger = logging.getLogger('rear')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
        return d

    def getUserByHashCode(self, user_code, hash_code, status='A'):
        """
        根据用户代码和秘钥查询用户
        :param user_code: str, 用户名称
        :param hash_code: str, 秘钥
        :param status: str, 查询状态, 为''空字符串时表示不查询状态
        :return: User, 返回用户信息, 查询不到返回None
        """
        d = None
        try:
            u = aliased(User, name='u')
            qry = self.session.query(u)
            qry = qry.filter(u.user_code == user_code, u.hash_code == hash_code)
            if status != '':
                qry = qry.filter(u.status == status)
            d = qry.first()
        except Exception as err:
            logger = logging.getLogger('rear')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
        return d

    def getUserByCodePwd(self, user_code, password, status='A'):
        """
        根据用户代码和密码查询用户
        :param user_code: str, 用户名称
        :param password: str, 秘钥
        :param status: str, 查询状态, 为''空字符串时表示不查询状态
        :return: User, 返回用户信息, 查询不到返回None
        """
        d = None
        try:
            u = aliased(User, name='u')
            qry = self.session.query(u)
            qry = qry.filter(u.user_code == user_code, u.password==password)
            if status != '':
                qry = qry.filter(u.status == status)
            d = qry.first()
        except Exception as err:
            logger = logging.getLogger('rear')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
        return d

    def getDirRolesByCode(self, user_code, status='A'):
        """
        获得用户的角色(不从角色树中继承)
        :param user_code: str, 用户代码
        :param status: str, 查询状态, 为''空字符串时表示不查询状态
        :return: list, 返回角色信息列表
        """
        l = []
        try:
            r = aliased(Role, name='r')
            u = aliased(User, name='u')
            ur = aliased(UserRole, name='ur')

            qry = self.session.query(r)
            qry = qry.filter(u.user_code == user_code, u.user_code == ur.user_code, ur.role_code==r.role_code)
            if status != '':
                qry = qry.filter(r.status == status)
            l = qry.all()
        except Exception as err:
            logger = logging.getLogger('rear')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
        return l

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
        :return: int, 0-更新成功, -1-更新失败
        """
        try:
            u = self.session.query(User).filter(User.user_code == user_code)
            if name != '':
                u.update({'name': name})
            if password != '':
                u.update({'password': password})
            if hash_code != '':
                u.update({'hash_code': hash_code})
            if phone != '':
                u.update({'phone': phone})
            if email != '':
                u.update({'email': email})
            if user_type != '':
                u.update({'user_type': user_type})
            if status != '':
                u.update({'status': status})
        except Exception as err:
            logger = logging.getLogger('rear')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
            return -1
        return 0

    def listUsers(self, status='A'):
        """
        列出所有用户
        :param status: str, 查询状态, 为''空字符串时表示不查询状态
        :return: list, 用户列表
        """
        l = []
        try:
            qry = self.session.query(User)
            if status!='':
                qry.filter(User.status==status)
            l = qry.all()
        except Exception as err:
            logger = logging.getLogger('rear')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
        return l

    def delUserRole(self, user_code):
        """
        删除用户
        :param user_code: str, 要删除的用户的代码
        :return: int, 成功删除的记录数, 删除失败则返回-1
        """
        n = 0
        try:
            qry = self.session.query(UserRole).filter(UserRole.user_code == user_code)
            n = qry.delete()
        except Exception as err:
            logger = logging.getLogger('rear')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
            return -1
        return n

    def addUserRole(self, user_code, role_code):
        """
        新增用户的角色
        :param user_code: str, 用户代码
        :param role_code: str, 新增角色代码
        :return: int, 0-新增成功, -1-新增失败
        """
        try:
            ur = UserRole(user_code=user_code, role_code=role_code)
            self.addRecord(ur)
        except Exception as err:
            logger = logging.getLogger('rear')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
            return -1
        return 0

    def addUserAvatar(self, user_code, avatar):
        """
        新增用户的头像
        :param user_code: str, 用户代码
        :param avatar: str, 头像的相对路径
        :return: int, 0-新增成功, -1-新增失败
        """
        try:
            ur = UserAvatar(user_code=user_code, avatar=avatar)
            self.addRecord(ur)
        except Exception as err:
            logger = logging.getLogger('rear')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
            return -1
        return 0

    def updateAvatarByCode(self, user_code, avatar=''):
        """
        更新用户的头像
        :param user_code: str, 用户代码
        :param avatar: str, 头像的相对路径
        :return: int, 0-更新成功, -1-更新失败
        """
        try:
            u = self.session.query(UserAvatar).filter(UserAvatar.user_code == user_code)
            if avatar != '':
                u.update({'avatar': avatar})
        except Exception as err:
            logger = logging.getLogger('rear')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
            return -1
        return 0

    def getUserAvatarByCode(self, user_code):
        """
        获得用户头像信息
        :param user_code: str, 用户代码
        :return: UserAvatar, 返回用户头像信息, 失败返回None
        """
        d = None
        try:
            u = aliased(UserAvatar, name='u')
            qry = self.session.query(u)
            qry = qry.filter(u.user_code == user_code)
            d = qry.first()
        except Exception as err:
            logger = logging.getLogger('rear')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
        return d

    def bulkUpdateUserRole(self, user_code, role):
        """
        全量覆盖更新用户角色
        :param user_code: str, 用户代码
        :param role: list, 角色列表
        :return: int, 0-更新成功, -1-删除角色失败, -2-新增用户角色失败
        """
        r = self.delUserRole(user_code)
        if r < 0:
            return -1
        for e in role:
            r = self.addUserRole(user_code, e)
            if r != 0:
                return -2
        return 0

    def authenticateUser(self, user_code, pwd, role_code):
        """
        验证用户代码、密码和角色
        :param user_code: str, 用户代码
        :param pwd: str, 用户密码
        :param role_code: 角色代码
        :return: list, 返回查询条件的用户列表
        """
        l = []
        try:
            au = aliased(User, name='au')
            ar = aliased(UserRole, name='ar')
            qry = self.session.query(au)
            qry = qry.filter(au.user_code==user_code, au.password==pwd, ar.role_code==role_code, au.user_code == ar.user_code)
            l = qry.order_by(au.user_id).all()
        except Exception as err:
            logger = logging.getLogger('rear')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
        return l

    def addUserWeixin(self, user_code, openid_mini="", openid_offi="", openid_app="", unionid=""):
        """
        新增用户的微信信息
        :param user_code: str, 用户代码
        :param openid_mini: str, 用户在小程序的openid
        :param openid_offi: str, 用户在公众号的openid
        :param openid_app: str, 用户在app的openid
        :param unionid: str, 用户在微信平台的unionid
        :return: int, 0-新增成功, -1-新增失败
        """
        try:
            ur = UserWeixin(user_code=user_code, openid_mini=openid_mini, openid_offi=openid_offi,
                            openid_app=openid_app, unionid=unionid)
            self.addRecord(ur)
        except Exception as err:
            logger = logging.getLogger('rear')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
            return -1
        return 0

    def updateUserWeixinByCode(self, user_code, openid_mini="", openid_offi="", openid_app="", unionid=""):
        """
        更新用户的微信信息
        :param user_code: str, 用户代码
        :param openid_mini: str, 用户在小程序的openid
        :param openid_offi: str, 用户在公众号的openid
        :param openid_app: str, 用户在app的openid
        :param unionid: str, 用户在微信平台的unionid
        :return: int, 0-新增成功, -1-新增失败
        """
        try:
            u = self.session.query(UserWeixin).filter(UserWeixin.user_code == user_code)
            if openid_mini != '':
                u.update({'openid_mini': openid_mini})
            if openid_offi != '':
                u.update({'openid_offi': openid_offi})
            if openid_mini != '':
                u.update({'openid_app': openid_app})
            if openid_mini != '':
                u.update({'unionid': unionid})
        except Exception as err:
            logger = logging.getLogger('rear')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
            return -1
        return 0
