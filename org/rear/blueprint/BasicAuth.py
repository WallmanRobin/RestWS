# coding=utf-8

from flask import Blueprint
from flask import session, abort, request

from org.rear.authorization.auth import jwtCodeRequired, rbacChecked
from org.rear.authorization.rbac.Role.RoleHandler import RoleHandler
from org.rear.authorization.rbac.User.UserHandler import UserHandler
from org.rear.util.app import packageResponse

basicAuth_bp = Blueprint('BasicAuth', __name__)

@basicAuth_bp.route('/userInfo',methods=['GET'])
@rbacChecked
@jwtCodeRequired
def userInfo():
    """
    向客户端返回用户权限信息
    :return:
    """
    if 'current_user_proxy' in session:
        up = session['current_user_proxy']
        if up:
            h = UserHandler()
            a = h.getUserAvatarByCode(up.user_code)
            return packageResponse({'data':{'roles':[e.role_code for e in up.roles], 'name':up.user_data.name, 'avatar': a.avatar if a else 'common/portrait.gif', 'introduction':up.user_data.name+'('+up.user_code+')'}})
    return '登录超时，根据秘钥无法找到在线用户！', 401


@basicAuth_bp.route('/roleRoutes',methods=['Post'])
@rbacChecked
@jwtCodeRequired
def getRoleRoutes():
    """
    向客户端返回角色的前置菜单列表
    :return: json, {'data': []}
    """
    h = RoleHandler()
    data = request.get_json()
    a = []
    if data:
        for e in data:
            r = h.getViewrouteByRole(e)
            if r:
                a.extend([e.viewroute for e in r])
    return packageResponse({'data': a})
