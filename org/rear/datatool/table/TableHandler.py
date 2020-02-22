# coding=utf-8

"""
数据表业务处理类, 该类函数负责进行数据库事务提交
"""

import logging
import sys
from org.rear.util.db.handler.BaseHandler import BaseHandler

from org.rear.datatool.table.TableData import TableData


class TableHandler(BaseHandler):
    def createTable(self, tableJson):
        """
        根据json数据创建数据库表
        :param tableJson: json 表数据
        :return: int, 0-成功， -1-失败
        """
        d = self.getData(TableData)
        return d.createTable(tableJson)

    def updateTableData(self, data):
        """
        更新数据表信息(包括列信息)
        :param data: json, 数据表信息
        :return: int, 0-成功， -1-更新数据表信息失败, -2-更新数据表列信息失败, -3-提交时失败
        """
        r = 0
        d = self.getData(TableData)
        table_name = data['name']
        descr = data['descr']
        status = 'A' if data['status'] == True else 'I'
        t = d.getTableByName(table_name, status='')
        if t:
            r = d.updateDataTableByName(table_name, descr, status)
        else:
            r = d.addDataTable(table_name, descr, status)
        if r != 0:
            return -1
        cols = data['columns']
        if cols and len(cols) > 0:
            r = d.bulkUpdateTableColumns(table_name, cols)
        if r != 0:
            d.rollback()
            return -2
        try:
            d.commit()
        except Exception as err:
            logger = logging.getLogger('rear')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
            r = -3
        return r

    def listTables(self, status='A'):
        """
        查询所有数据表信息
        :param status: str, 查询状态, 为''空字符串时表示不查询状态
        :return: list, 数据表列表
        """
        d = self.getData(TableData)
        l = d.listTables(status)
        return l

    def getTableData(self, params, status='A'):
        """
        根据数据表名和描述模糊查询数据表信息(包括数据表列)
        :param params: json, {'name':str,'descr':str}
        :param status: str, 查询状态, 为''空字符串时表示不查询状态
        :return: list, 数据表信息列表
        """
        table_name = params['name']
        descr = params['descr']
        data = []
        l = []
        d = self.getData(TableData)
        if table_name and table_name != '':
            l = d.getTableLikeName(table_name, status)
        elif descr and descr != '':
            l = d.getTableLikeDescr(descr, status)
        else:
            l = d.listTables(status)

        if len(l) > 0:
            for e in l:
              t = {'name': e.table_name, 'descr': e.descr, 'status': True if e.status=='A' else False}
              c = d.getTableColumnsDataByName(e.table_name)
              t['columns'] = c
              data.append(t)
        return data

    def reflectTables(self):
        """
        映射获得当前数据库内的所有表结构信息并返回
        :return: list, [{'name':str, 'descr':str,'status':True, columns:[]}]
        """
        d = self.getData(TableData)
        l = d.reflectTables()
        d.commit()
        return l

    def dumpTable(self, dataJson):
        """
        将数据写入指定的数据库表中
        :param dataJson: json, 数据
        :return: touple,(i, text), 成功则返回(0, ''), 失败则返回(1, err)
        """
        i = 0
        r = ''
        if dataJson:
            d = self.getData(TableData)
            i, r = d.dumpTable(dataJson)
            if i==0:
                d.commit()
            else:
                d.rollback()
        return i, r
