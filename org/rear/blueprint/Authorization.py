# coding=utf-8

from flask import Blueprint, current_app
from flask import session, request

from org.rear.authorization.auth import jwtCodeRequired, rbacChecked
from org.rear.authorization.rbac.Role.RoleHandler import RoleHandler
from org.rear.authorization.rbac.User.UserHandler import UserHandler
from org.rear.util.app import packageResponse

authorization_bp = Blueprint('Authorization', __name__)


@authorization_bp.route('/endpoints', methods=['GET'])
@rbacChecked
@jwtCodeRequired
def endpoints():
    """
    向客户端返回所有后台服务
    :return: json, {'data': [{'endpoint': str, 'rule': str, 'methods':str}]}
    """
    r = {'data': []}
    for e in current_app.url_map.iter_rules():
        n = {'endpoint': e.endpoint, 'rule': e.rule,
             'methods': [ee for ee in e.methods if (ee != 'OPTIONS' and ee != 'HEAD')]}
        r['data'].append(n)
    return packageResponse(r)


@authorization_bp.route('/listUsers', methods=['GET'])
@rbacChecked
@jwtCodeRequired
def listUsers():
    """
    向客户端返回所有用户
    :return: json, {'data': [{'user_code': str, 'name': str}]}
    """
    h = UserHandler()
    u = h.listUsers(status='')
    return packageResponse({'data': [{'user_code': e.user_code, 'name': e.name} for e in u]})


@authorization_bp.route('/methods/<string:endpoint>', methods=['GET'])
@rbacChecked
@jwtCodeRequired
def methods(endpoint):
    """
    向客户端返回该后台服务相关的http method
    :param endpoint:str, 后台服务代码
    :return: json, {'data': []}
    """
    r = {'data': []}
    for e in current_app.url_map.iter_rules(endpoint):
        r['data'] = [ee for ee in e.methods if (ee != 'OPTIONS' and ee != 'HEAD')]
    return packageResponse(r)


@authorization_bp.route('/role', methods=['GET'])
@rbacChecked
@jwtCodeRequired
def getRoleData():
    """
    向客户端返回角色数据(包括角色的后台服务和前台菜单)
    :return: json, [{'code': str, 'name': name, 'status': boolean, 'endpoint': [], 'viewroute': []}]
    """
    args = request.args
    params = {'code': '', 'name': ''}
    if 'code' in args:
        params['code'] = args['code']
    if 'name' in args:
        params['name'] = args['name']
    h = RoleHandler()
    return packageResponse({'data': h.getRoleData(params)})


@authorization_bp.route('/roleTreeData/<string:role_code>', methods=['GET'])
@rbacChecked
@jwtCodeRequired
def getRoleTreeData(role_code):
    """
    向客户端返回查询角色的树数据
    :param role_code: str, 角色代码
    :return: json, 以角色为顶节点的树({'data':{'role_code': str, 'name': str, 'status': boolean, children:[]}})
    """
    h = RoleHandler()
    return packageResponse({'data': h.getRoleTreeData(role_code)})


@authorization_bp.route('/updateRole', methods=['POST'])
@rbacChecked
@jwtCodeRequired
def updateRole():
    """
    更新角色数据
    :return: json, {'data':{'code': r}} r为0表示更新成功, 否则表示更新失败
    """
    data = request.get_json()
    if data:
        up = session['current_user_proxy']
        if up:
            h = RoleHandler()
            r = h.updateRoleData(data, up.user_code)
    return packageResponse({'data': {'code': r}}) if r == 0 else ('角色信息更新失败！', 500)


@authorization_bp.route('/roles', methods=['GET'])
@rbacChecked
@jwtCodeRequired
def listRoles():
    """
    向客户端返回所有角色的列表
    :return: json, {'data': [{'role_code': str, 'name': str}]}
    """
    h = RoleHandler()
    l = h.listRoles(status='')
    return packageResponse({'data': [{'role_code': e.role_code, 'name': e.name} for e in l]})


@authorization_bp.route('/user', methods=['GET'])
@rbacChecked
@jwtCodeRequired
def getUserData():
    """
    向客户端返回用户数据
    :return: json, {'data':{'user_code':str, 'name':str, 'status':boolean, 'password':'', 'phone':str, 'email':str, 'avatar':str, 'role':[]}}
    """
    args = request.args
    params = {'user_code': '', 'name': ''}
    if 'user_code' in args:
        params['user_code'] = args['user_code']
    if 'name' in args:
        params['name'] = args['name']
    h = UserHandler()
    return packageResponse({'data': h.getUserData(params)})


@authorization_bp.route('/updateUser', methods=['POST'])
@rbacChecked
@jwtCodeRequired
def updateUser():
    """
    更新用户数据
    :return: json, {'data':{'code': r}} r为0表示更新成功, 否则表示更新失败
    """
    data = request.get_json()
    if data:
        h = UserHandler()
        r = h.updateUserData(data)
    return packageResponse({'data': {'code': r}}) if r == 0 else ('用户信息更新失败！', 500)


@authorization_bp.route('/setPassword', methods=['POST'])
@rbacChecked
@jwtCodeRequired
def setPassword():
    """
    设置用户密码
    :return: json, {'data':{'code': r}} r为0表示设置成功, 否则表示设置失败
    """
    data = request.get_json()
    if data:
        h = UserHandler()
        user_code = data['user_code']
        password = data['password']
        r = h.setPassword(user_code, password)
    return packageResponse({'data': {'code': r}}) if r == 0 else ('密码信息更新失败！', 500)


@authorization_bp.route('/pushUserAvatar', methods=['POST'])
def pushUserAvatar():
    """
    更新用户头像
    :return: json, {'data':{'code': r}} r为0表示更新成功, 否则表示更新失败
    """
    data = request.get_json()
    if data:
        h = UserHandler()
        r = h.pushUserAvatar(data)
    return packageResponse({'data': {'code': r}}) if r == 0 else ('头像信息更新失败！', 500)
