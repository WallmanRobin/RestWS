# coding=utf-8

from flask import Blueprint
from flask import request

from org.rear.authorization.auth import jwtCodeRequired, rbacChecked
from org.rear.util.app import packageResponse
from org.rear.util.tree.TreeHandler import TreeHandler

tree_bp = Blueprint('Tree', __name__)

@tree_bp.route('/getTree',methods=['GET'])
@rbacChecked
@jwtCodeRequired
def getTree():
    """
    向客户端返回根据代码和名称模糊查询获得的树列表
    :return: json, {'data': []}
    """
    args = request.args
    params = {'tree_code':'', 'name':''}
    if 'tree_code' in args:
        params['tree_code'] = args['tree_code']
    if 'name' in args:
        params['name'] = args['name']
    h = TreeHandler()
    return packageResponse({'data': h.getTreeData(params)})

@tree_bp.route('/listTrees',methods=['GET'])
@rbacChecked
@jwtCodeRequired
def listTrees():
    """
    向客户端返回所有树的列表
    :return: json, {'data': [{'tree_code':str, 'name':str}]}
    """
    h = TreeHandler()
    t = h.listTrees(status='')
    return packageResponse({'data': [{'tree_code':e.tree_code, 'name':e.name} for e in t]})

@tree_bp.route('/listNodes',methods=['GET'])
@rbacChecked
@jwtCodeRequired
def listNodes():
    """
    向客户端返回树的所有关联信息列表
    :return: json, {'data': []}
    """
    args = request.args
    ref_table = ""
    ref_code = ""
    ref_descr = ""
    if 'ref_table' in args:
        ref_table = args['ref_table']
    if 'ref_code' in args:
        ref_code = args['ref_code']
    if 'ref_descr' in args:
        ref_descr = args['ref_descr']
    h = TreeHandler()
    l = h.listRefNodes(ref_table, ref_code, ref_descr)
    return packageResponse({'data': l}) if len(l) > 0 else ('没有找到关联表的数据，请确认关联表和列信息正确！', 500)

@tree_bp.route('/updateTree', methods=['POST'])
@rbacChecked
@jwtCodeRequired
def updateTree():
    """
    更新树数据
    :return: json, 无意义
    """
    data = request.get_json()
    if data:
        h = TreeHandler()
        h.updateTreeData(data)
    return packageResponse({'data':{}})