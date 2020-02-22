#!flask/bin/python
# coding=utf-8

from flask import Blueprint, send_file, abort, request

from org.rear.authorization.auth import rbacChecked, jwtCodeRequired
from org.rear.datatool.table.TableHandler import TableHandler
from org.rear.util.app import packageResponse, packageDate, packageTimeStamp

datatool_bp = Blueprint('DataTool', __name__)


@datatool_bp.route('/updateTable', methods=['POST'])
@rbacChecked
@jwtCodeRequired
def updateTable():
    """
    更新数据表信息
    :return: json, {'data': r}, r为0表示更新成功, 否则为更新失败
    """
    data = request.get_json()
    if data:
        h = TableHandler()
        r = h.updateTableData(data)
    return packageResponse({'data': r})

@datatool_bp.route('/tables', methods=['GET'])
@rbacChecked
@jwtCodeRequired
def listTables():
    """
    向客户端返回所有数据表的列表
    :return: json, {'data': [{'name': str, 'descr': str, 'status': str}]}
    """
    h = TableHandler()
    l = h.listTables(status='')
    return packageResponse({'data': [{'name': e.table_name, 'descr': e.descr, 'status': e.status} for e in l]})

@datatool_bp.route('/table',methods=['GET'])
@rbacChecked
@jwtCodeRequired
def getTableData():
    """
    向客户端返回根据代码和名称模糊查询的数据表列表()
    :return: {'data': []}
    """
    args = request.args
    params = {'name':'', 'descr':''}
    if 'name' in args:
        params['name'] = args['name']
    else:
        params['name'] = ''
    if 'descr' in args:
        params['descr'] = args['descr']
    else:
        params['descr'] = ''
    h = TableHandler()
    l = h.getTableData(params, status='')
    return packageResponse({'data': l})

@datatool_bp.route('/refTable', methods=['GET'])
@rbacChecked
@jwtCodeRequired
def getRefTableData():
    """
    向客户端返回数据库映射获得的数据库表列表
    :return: {'data': []}
    """
    h = TableHandler()
    l = h.reflectTables()
    return packageResponse({'data': l})


@datatool_bp.route('/createTable', methods=['POST'])
@rbacChecked
@jwtCodeRequired
def createTable():
    """
    在数据库中创建数据实体表
    :return: json, {'data': r}, r为0表示创建成功, 否则为创建失败
    """
    data = request.get_json()
    h = TableHandler()
    r = h.createTable(data)
    return packageResponse({'data': r})

@datatool_bp.route('/dumpTable', methods=['POST'])
@rbacChecked
@jwtCodeRequired
def dumpTable():
    """
    将数据写入数据库实体表
    :return: json, 返回插入结果和提示信息,({'data': {'code': str, 'text': str})
    """
    data = request.get_json()
    h = TableHandler()
    i, r = h.dumpTable(data)
    return packageResponse({'data': {'code': i, 'text': str(r)}})
