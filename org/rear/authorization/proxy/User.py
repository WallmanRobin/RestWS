# coding=utf-8

"""
用户代理业务交易类
"""

from org.rear.authorization.rbac.Role.RoleHandler import RoleHandler
from org.rear.authorization.rbac.User.UserHandler import UserHandler
from org.rear.util.list import eliminateListDups


class UserProxy:
    def __init__(self, user_data, key=''):
        """
        用户代理类初始化函数
        :param user_data: UserModel, 用户示例
        :param key: str, 用户的安全密钥
        """
        self.key = key
        if user_data:
            self.user_data = user_data
            self.user_code = self.user_data.user_code
        else:
            self.user_data = None
            self.user_code = 'anonymous'
        self.roles = self.getRoles()
        self.viewroute = self.getUserViewroute()
        self.endpoint = self.getUserEndpoint()

    def setUserRoles(self, roles):
        """
        设置用户的角色列表
        :param roles: list, 用户的角色列表
        :return: 没有返回值
        """
        self.roles = roles

    def getRoles(self):
        """
        获得对象的角色列表
        :return: list, 对象的角色列表
        """
        h = UserHandler()
        r = RoleHandler()
        roles = h.getUserRolesByCode(self.user_code)
        all_roles = roles.copy()
        for e in roles:
            all_roles.extend(r.getAllDescendantsByCode(e.role_code))
        return all_roles

    def getUserEndpoint(self):
        """
        获得对象有权访问的后台服务列表
        :return: list, 对象有权访问的后台服务列表
        """
        ep = []
        if self.roles and len(self.roles) > 0:
            h = RoleHandler()
            for e in self.roles:
                r = h.getEndpointByRole(e.role_code)
                for ee in r:
                    ep.append({'endpoint': ee.endpoint, 'method': ee.method})
        return eliminateListDups(ep)

    def getUserViewroute(self):
        """
        获得对象有权访问的前台菜单列表
        :return: list, 对象有权访问的前台菜单列表
        """
        vr = []
        if self.roles and len(self.roles) > 0:
            h = RoleHandler()
            for e in self.roles:
                r = h.getViewrouteByRole(e.role_code)
                for ee in r:
                    vr.append({'viewroute': ee.viewroute, 'leaf': ee.leaf})
        return eliminateListDups(vr)
