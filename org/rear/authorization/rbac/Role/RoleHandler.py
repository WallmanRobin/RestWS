# coding: utf-8

"""
角色业务处理类, 该类函数负责进行数据库事务提交
"""

import logging
import sys
from flask import current_app
from org.rear.util.db.handler.BaseHandler import BaseHandler

from org.rear.authorization.rbac.Role.RoleData import RoleData
from org.rear.util.tree.TreeHandler import TreeHandler


class RoleHandler(BaseHandler):
    def getRoleByCode(self, role_code, status='A'):
        """
        根据角色代码查询获得角色
        :param role_code: str, 查询的角色代码
        :param status: str, 查询状态, 为''空字符串时表示不查询状态
        :return: Role, 角色示例, 失败时返回None
        """
        d = self.getData(RoleData)
        r = d.getRoleByCode(role_code, status)
        return r

    def addRole(self, role_code, name, lastupdatedby='', status='A'):
        """
        新增角色
        :param role_code: str, 角色代码
        :param name: str, 角色名称
        :param lastupdateby: date, 日期字符串, 格式YYYY-MM-DD
        :param status: str, 有效状态, 'A'-有效, 'I'-无效
        :return: int, 0-新增成功, -1-新增失败, -2-提交失败
        """
        d = self.getData(RoleData)
        r = d.addRole(role_code, name, lastupdatedby, status)
        if r != 0:
            return r
        try:
            d.commit()
        except Exception as err:
            logger = logging.getLogger('rear')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
            return -2
        return r

    def updateRole(self, role_code, name, lastupdatedby='', status='A'):
        """
        更新角色
        :param role_code: str, 角色代码
        :param name: str, 角色名称
        :param lastupdateby: date, 日期字符串, 格式YYYY-MM-DD
        :param status: str, 有效状态, 'A'-有效, 'I'-无效
        :return: int, 0-更新成功, -1-更新失败, -2-提交失败
        """
        d = self.getData(RoleData)
        r = d.updateRole(role_code, name, lastupdatedby, status)
        if r != 0:
            return r
        try:
            d.commit()
        except Exception as err:
            logger = logging.getLogger('rear')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
            return -2
        return r

    def updateRoleData(self, data, lastupdateby):
        """
        更新角色，包括角色的后台服务和前台菜单
        :param data: json, 角色数据({'code':str, 'name':str, status:boolean, endpoint:[], viewroute:[]}})
        :param lastupdateby: str, 更新用户
        :return: int, 0-更新成功, -1-更新角色失败, -2-更新后台服务失败, -3-更新前台菜单失败, -4-提交时失败
        """
        d = self.getData(RoleData)
        role_code = data['code']
        name = data['name']
        status = 'A' if data['status']==True else 'I'
        role = d.getRoleByCode(role_code)
        if role:
            r = d.updateRole(role_code, name, lastupdateby, status)
        else:
            r = d.addRole(role_code, name, lastupdateby, status)
        if r != 0:
            return -1
        endpoint = [e for e in data['endpoint'] if 'endpoint' in e]
        r = d.bulkUpdateRoleEndpoint(role_code, endpoint)
        if r != 0:
            d.rollback()
            return -2
        viewroute = [e for e in data['viewroute'] if 'viewroute' in e]
        r = d.bulkUpdateRoleViewroute(role_code, viewroute)
        if r != 0:
            d.rollback()
            return -3
        try:
            d.commit()
        except Exception as err:
            logger = logging.getLogger('rear')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
            return -4
        return r

    def getRole(self, params, status='A'):
        """
        根据代码或者名字模糊查询角色
        :param params: json, 查询角色代码和名字({'code': str, 'name': str})
        :param status: str, 查询状态, 为''空字符串时表示不查询状态
        :return: list, 角色列表
        """
        code = params['code']
        name = params['name']
        d = self.getData(RoleData)
        r = []
        if code and code!='':
            r = d.getRoleLikeCode(code, status)
        elif name and name!='':
            r = d.getRoleLikeName(name, status)
        else:
            r = d.listRoles(status)
        return r

    def listRoles(self, status='A'):
        """
        查询角色列表
        :param status: str, 查询状态, 为''空字符串时表示不查询状态
        :return: list, 角色列表
        """
        d = self.getData(RoleData)
        l = d.listRoles(status)
        return l

    def getRoleTreeData(self, role_code):
        """
        根据角色树, 构建以角色为顶节点的树并返回
        :param role_code: str, 角色代码
        :return: dict, 以角色为顶节点的树({'role_code': str, 'name': str, 'status': boolean, children:[]})
        """
        treeData = {'role_code': '', 'name': '', 'status': ''}
        role = self.getRoleByCode(role_code)
        if role:
            treeData['role_code'] = role_code
            treeData['name'] = role.name
            treeData['status'] = True if role.status=='A' else False
            h = TreeHandler()
            child = h.getDirectDescendants('role', role_code)
            el = []
            for e in child:
                # 逐级逐个子节点递归遍历
                ee = self.getRoleTreeData(e.node_code)
                ee['parent'] = role_code
                el.append(ee)
            if len(el) > 0:
                treeData['children'] = el
        return treeData

    def getRoleData(self, params):
        """
        查询角色数据，包括角色的后台服务和前台菜单
        :param params: json, 查询角色代码和名字({'code': str, 'name': str})
        :return: list, 角色数据([{'role_code': str, 'name': str, 'status': boolean, 'endpoint':[], 'viewroute':[]}])
        """
        role = self.getRole(params)
        l = []
        if len(role) >0 :
            for r in role:
                e = self.getEndpointByRole(r.role_code)
                el =[]
                for ee in e:
                    try:
                        iter_rules = current_app.url_map.iter_rules(ee.endpoint)
                        rl = ''
                        for iter in iter_rules:
                            rl = iter.rule
                            break
                        if rl != '':
                            el.append({'endpoint': ee.endpoint, 'rule': rl, 'method': ee.method})
                    except KeyError:
                        continue
                v = self.getViewrouteByRole(r.role_code)
                vl = [ve.viewroute for ve in v if ve.leaf=='Y']
                l.append({'code': r.role_code, 'name': r.name, 'status': True if r.status=='A' else False, 'endpoint': el, 'viewroute': vl})
        return l

    def getAllDescendantsByCode(self, role_code, status='A'):
        """
        根据代码查询角色在角色树下各级所有子角色
        :param role_code: str, 角色代码
        :param status: str, 查询状态, 为''空字符串时表示不查询状态
        :return: list, 所有子角色清单, 查询失败返回空列表
        """
        d = self.getData(RoleData)
        l = d.getAllDescendantsByCode(role_code, status)
        return l


    def getParentByCode(self, role_code, status='A'):
        """
        根据代码查询角色在角色树上的父角色
        :param role_code: str, 查询角色
        :param status: str, 查询状态, 为''空字符串时表示不查询状态
        :return: Role, 角色示例, 查询失败返回None
        """
        d = self.getData(RoleData)
        p = d.getParentByCode(role_code, status)
        return p

    def getEndpointByRole(self, role_code):
        """
        根据角色代码查询后台服务列表
        :param role_code: str, 角色代码
        :return: list, 后台服务列表
        """
        d = self.getData(RoleData)
        e = d.getEndpointByRole(role_code)
        return e

    def getViewrouteByRole(self, role_code):
        """
        根据角色代码查询前台菜单列表
        :param role_code: str, 角色代码
        :return: list, 前台菜单列表
        """
        d = self.getData(RoleData)
        v = d.getViewrouteByRole(role_code)
        return v

    def getViewrouteLeafByRole(self, role_code):
        """
        根据角色代码查询前台菜单叶子列表
        :param role_code: str, 角色代码
        :return: list, 前台菜单叶子列表
        """
        d = self.getData(RoleData)
        v = d.getViewrouteLeafByRole(role_code)
        return v

    def addRoleEndpoint(self, role_code, endpoint, method='GET'):
        """
        新增角色的后台服务
        :param role_code: str, 角色代码
        :param endpoint: str, 后台服务
        :param method: str, 后台服务访问方法
        :return: int, 0-新增成功, -1-新增失败, -2-提交时失败
        """
        d = self.getData(RoleData)
        r = d.addRoleEndpoint(role_code, endpoint, method)
        if r == 0:
            try:
                d.commit()
            except Exception as err:
                logger = logging.getLogger('rear')
                logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
                return -2
        return r

    def updateRoleEndpoint(self, role_code, endpoint, method='GET'):
        """
        更新角色的后台服务列表
        :param role_code: str, 角色代码
        :param endpoint: str, 后台服务
        :param method: str, 后台服务访问方法
        :return: int, 0-更新成功, -1-更新失败, -2-提交时失败
        """
        d = self.getData(RoleData)
        r = d.updateRoleEndpoint(role_code, endpoint, method)
        if r == 0:
            try:
                d.commit()
            except Exception as err:
                logger = logging.getLogger('rear')
                logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
                return -2
        return r

    def bulkUpdateRoleEndpoint(self, role_code, listRoleEndpoint):
        """
        更新角色的后台服务列表
        :param role_code: str, 角色代码
        :param listRoleEndpoint: list, 后台服务列表
        :return: int, 0-更新成功, -1-更新服务列表时失败, -2-删除角色列表时失败, -3-提交时失败
        """
        d = self.getData(RoleData)
        r = d.bulkUpdateRoleEndpoint(role_code, listRoleEndpoint)
        if r != 0:
            d.rollback()
        else:
            try:
                d.commit()
            except Exception as err:
                logger = logging.getLogger('rear')
                logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
                r = -3
        return r

    def bulkUpdateRoleViewroute(self, role_code, listRoleViewroute):
        """
        更新角色的前台菜单列表
        :param role_code: str, 角色代码
        :param listRoleEndpoint: list, 前台菜单列表
        :return: int, 0-更新成功, -1-更新前台菜单时失败, -2-删除前台菜单时失败, -3-提交时失败
        """
        d = self.getData(RoleData)
        r = d.bulkUpdateRoleViewroute(role_code, listRoleViewroute)
        if r != 0:
            d.rollback()
        else:
            try:
                d.commit()
            except Exception as err:
                logger = logging.getLogger('rear')
                logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
                r = -3
        return r
