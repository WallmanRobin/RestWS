# coding: utf-8

"""
角色操作类, 该类的函数不会进行数据库事务提交
"""

import logging
import sys
from org.rear.util.db.data.BaseData import BaseData
from sqlalchemy.orm import aliased

from org.rear.authorization.rbac.Role.RoleModel import Role, RoleEndpoint, RoleViewroute
from org.rear.util.tree.TreeModel import TreeNode


class RoleData(BaseData):
    def __init__(self, session):
        super().__init__(session)
        self.tree_code = 'role'

    def addRole(self, role_code, name, lastupdateby='', status='A'):
        """
        新增角色
        :param role_code: str, 角色代码
        :param name: str, 角色名称
        :param lastupdateby: date, 日期字符串, 格式YYYY-MM-DD
        :param status: str, 有效状态, 'A'-有效, 'I'-无效
        :return: int, 0-新增成功, -1-新增失败
        """
        try:
            role = Role(role_code=role_code, name=name, lastupdateby=lastupdateby, status=status)
            self.addRecord(role)
        except Exception as err:
            logger = logging.getLogger('rear')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
            return -1
        return 0

    def updateRole(self, role_code, name, lastupdateby='', status='A'):
        """
        更新角色
        :param role_code: str, 角色代码
        :param name: str, 角色名称
        :param lastupdateby: date, 日期字符串, 格式YYYY-MM-DD
        :param status: str, 有效状态, 'A'-有效, 'I'-无效
        :return: int, 0-更新成功, -1-更新失败
        """
        try:
            qry = self.session.query(Role)
            qry = qry.filter(Role.role_code == role_code)
            qry.update({'name': name})
            if lastupdateby!='':
                qry.update({'lastupdateby': lastupdateby})
            if status != '':
                qry.update({'status': status})
        except Exception as err:
            logger = logging.getLogger('rear')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
            return -1
        return 0

    def listRoles(self, status='A'):
        """
        查询角色列表
        :param status: str, 查询状态, 为''空字符串时表示不查询状态
        :return: list, 角色列表
        """
        l = []
        try:
            qry = self.session.query(Role)
            if status!='':
                qry.filter(Role.status==status)
            l = qry.all()
        except Exception as err:
            logger = logging.getLogger('rear')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
        return l

    def getRoleLikeCode(self, role_code, status='A'):
        """
        根据代码模糊查询角色
        :param role_code: str, 查询角色代码
        :param status: str, 查询状态, 为''空字符串时表示不查询状态
        :return: list, 角色列表
        """
        l = []
        try:
            r = aliased(Role, name='r')
            qry = self.session.query(r)
            qry = qry.filter(r.role_code.like('%'+role_code+'%'))
            if status != '':
                qry = qry.filter(r.status == status)
            l = qry.all()
        except Exception as err:
            logger = logging.getLogger('rear')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
        return l

    def getRoleLikeName(self, name, status='A'):
        """
        根据名称模糊查询角色
        :param name: str, 查询角色名称
        :param status: str, 查询状态, 为''空字符串时表示不查询状态
        :return: list, 角色列表
        """
        l = []
        try:
            r = aliased(Role, name='r')
            qry = self.session.query(r)
            qry = qry.filter(r.name.like('%'+name+'%'))
            if status != '':
                qry = qry.filter(r.status == status)
            l = qry.all()
        except Exception as err:
            logger = logging.getLogger('rear')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
        return l

    def getRoleByCode(self, role_code, status='A'):
        """
        根据角色代码查询获得角色
        :param role_code: str, 查询的角色代码
        :param status: str, 查询状态, 为''空字符串时表示不查询状态
        :return: Role, 角色示例, 失败时返回None
        """
        d = None
        try:
            r = aliased(Role, name='r')
            qry = self.session.query(r)
            qry = qry.filter(r.role_code == role_code)
            if status != '':
                qry = qry.filter(r.status == status)
            d = qry.first()
        except Exception as err:
            logger = logging.getLogger('rear')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
        return d

    def getRoleByName(self, name, status='A'):
        """
        根据名称查询获得角色
        :param role_code: str, 查询的角色代码
        :param status: str, 查询状态, 为''空字符串时表示不查询状态
        :return: Role, 角色示例, 失败时返回None
        """
        d = None
        try:
            r = aliased(Role, name='r')
            qry = self.session.query(r)
            qry = qry.filter(r.name==name)
            if status != '':
                qry = qry.filter(r.status == status)
            d = qry.first()
        except Exception as err:
            logger = logging.getLogger('rear')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
        return d


    def getAllDescendantsByCode(self, role_code, status='A'):
        """
        根据代码查询角色在角色树下各级所有子角色
        :param role_code: str, 角色代码
        :param status: str, 查询状态, 为''空字符串时表示不查询状态
        :return: list, 所有子角色清单, 查询失败返回空列表
        """
        l = []
        try:
            r = aliased(Role, name='r')
            c = aliased(TreeNode, name='child')
            t = aliased(TreeNode, name='tree')
            qry = self.session.query(r)
            qry = qry.filter(r.role_code == c.node_code, t.tree_code == self.tree_code, c.tree_code == t.tree_code, t.node_code == role_code,
                             c.node_num > t.node_num, c.node_num <= t.node_num_end)
            if status != '':
                qry = qry.filter(r.status == status)
            l = qry.all()
        except Exception as err:
            logger = logging.getLogger('rear')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
        return l

    def getParentByCode(self, role_code, status='A'):
        """
        根据代码查询角色在角色树上的父角色
        :param role_code: str, 查询角色
        :param status: str, 查询状态, 为''空字符串时表示不查询状态
        :return: Role, 角色示例, 查询失败返回None
        """
        d = None
        try:
            r = aliased(Role, name='r')
            p = aliased(TreeNode, name='parent')
            c = aliased(TreeNode, name='child')

            qry = self.session.query(r)
            qry = qry.filter(p.node_code==r.role_code, p.tree_code=='role', p.tree_code==self.tree_code, p.tree_code==c.tree_code, c.node_code==role_code, p.node_id==c.parent_node, p.node_id!=p.parent_node)
            if status != '':
                qry = qry.filter(r.status == status)
            d = qry.first()
        except Exception as err:
            logger = logging.getLogger('rear')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
        return d

    def bulkUpdateRoleEndpoint(self, role_code, listRoleEndpoint):
        """
        更新角色的后台服务列表
        :param role_code: str, 角色代码
        :param listRoleEndpoint: list, 后台服务列表
        :return: int, 0-更新成功, -1-更新服务列表时失败, -2-删除角色列表时失败
        """
        r = self.delRoleEndpoint(role_code)
        if r < 0:
            return -2
        for e in listRoleEndpoint:
            r = self.addRoleEndpoint(role_code, e['endpoint'], e['method'])
            if r != 0:
                return r
        return 0

    def bulkUpdateRoleViewroute(self, role_code, listRoleViewroute):
        """
        更新角色的前台菜单列表
        :param role_code: str, 角色代码
        :param listRoleViewroute: list, 前台菜单列表
        :return: int, 0-更新成功, -1-更新菜单列表时失败, -2-删除菜单列表时失败
        """
        r = self.delRoleViewroute(role_code)
        if r < 0:
            return -2
        for e in listRoleViewroute:
            r = self.addRoleViewroute(role_code, e['viewroute'], 'Y' if e['leaf'] else 'N')
            if r != 0:
                return r
        return 0

    def getEndpointByRole(self, role_code):
        """
        根据角色代码查询后台服务列表
        :param role_code: str, 角色代码
        :return: list, 后台服务列表
        """
        l = []
        try:
            r = aliased(RoleEndpoint, name='r')
            qry = self.session.query(r)
            qry = qry.filter(r.role_code == role_code)
            l = qry.all()
        except Exception as err:
            logger = logging.getLogger('rear')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
        return l

    def addRoleEndpoint(self, role_code, endpoint, method='GET'):
        """
        新增角色的后台服务
        :param role_code: str, 角色代码
        :param endpoint: str, 后台服务
        :param method: str, 后台服务访问方法
        :return: int, 0-新增成功, -1-新增失败
        """
        try:
            self.addRecord(RoleEndpoint(role_code=role_code, endpoint=endpoint, method=method))
        except Exception as err:
            logger = logging.getLogger('rear')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
            return -1
        return 0

    def updateRoleEndpoint(self, role_code, endpoint, method='GET'):
        """
        更新角色的后台服务列表
        :param role_code: str, 角色代码
        :param endpoint: str, 后台服务
        :param method: str, 后台服务访问方法
        :return: int, 0-更新成功, -1-更新失败
        """
        try:
            qry = self.session.query(RoleEndpoint).filter(RoleEndpoint.role_code == role_code, RoleEndpoint.endpoint == endpoint)
            qry.update({'method': method})
        except Exception as err:
            logger = logging.getLogger('rear')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
            return -1
        return 0

    def delRoleEndpoint(self, role_code):
        """
        删除角色的后台服务
        :param role_code: str, 查询的角色列表
        :return: int, 成功删除的记录条数, 删除失败返回-1
        """
        n = 0
        try:
            qry = self.session.query(RoleEndpoint).filter(RoleEndpoint.role_code == role_code)
            n = qry.delete()
        except Exception as err:
            logger = logging.getLogger('rear')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
            return -1
        return n

    def getViewrouteByRole(self, role_code):
        """
        根据角色代码查询前台菜单列表
        :param role_code: str, 角色代码
        :return: list, 前台菜单列表
        """
        l = []
        try:
            vr = aliased(RoleViewroute, name='vr')
            qry = self.session.query(vr)
            qry = qry.filter(vr.role_code == role_code)
            l = qry.all()
        except Exception as err:
            logger = logging.getLogger('rear')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
        return l

    def getViewrouteLeafByRole(self, role_code):
        """
        根据角色代码查询前台菜单叶子列表
        :param role_code: str, 角色代码
        :return: list, 前台菜单叶子列表
        """
        l = []
        try:
            vr = aliased(RoleViewroute, name='vr')
            qry = self.session.query(vr)
            qry = qry.filter(vr.role_code == role_code, vr.leaf == 'Y')
            l = qry.all()
        except Exception as err:
            logger = logging.getLogger('rear')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
        return l

    def addRoleViewroute(self, role_code, viewroute, leaf):
        """
        新增角色的前台菜单
        :param role_code: str, 角色代码
        :param viewroute: str, 前台菜单
        :param method: str, 后台服务访问方法
        :return: int, 0-新增成功, -1-新增失败
        """
        try:
            self.addRecord(RoleViewroute(role_code=role_code, viewroute=viewroute, leaf=leaf))
        except Exception as err:
            logger = logging.getLogger('rear')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
            return -1
        return 0

    def delRoleViewroute(self, role_code):
        """
        删除角色的前台菜单
        :param role_code: str, 查询的角色列表
        :return: int, 成功删除的记录条数, 删除失败返回-1
        """
        n = 0
        try:
            r = self.session.query(RoleViewroute).filter(RoleViewroute.role_code == role_code)
            n = r.delete()
        except Exception as err:
            logger = logging.getLogger('rear')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
            return -1
        return n
