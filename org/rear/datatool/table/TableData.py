# coding=utf-8

"""
数据表操作类, 该类函数不会进行数据库事务提交
"""

import logging
import sys
from flask import current_app
from org.rear.util.db.data.BaseData import BaseData
from sqlalchemy import MetaData, Table, Column, Float, Text, VARCHAR, select, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import aliased

from org.rear import ctx
from org.rear.datatool.table.TableModel import DataTable, DataTableColumn


class TableData(BaseData):
    def __init__(self, session):
        """
        初始化函数, 调用父类初始化函数获得表操作基本函数, 初始化元数据变量, 初始化js2sql的数据类型映射关系
        :param session: 数据库操作会话
        """
        super().__init__(session)
        self.metadata = MetaData(ctx.db_engine)
        self.typeMapping = {'str':'String', 'int':'Integer', 'float': 'Float', 'Decimal':'DECIMAL', 'text':'Text', 'datetime':'DateTime', 'date':'Date'}

    def createTable(self, tableJson):
        """
        根据json数据创建数据库表
        :param tableJson: json 表数据
        :return: int, 0-成功， -1-失败
        """
        r = 0
        try:
            t = Table(tableJson['name'], self.metadata)
            import sqlalchemy
            for e in tableJson['columns']:
                type = getattr(sqlalchemy, e['type'])
                if 'length' in e and int(e['length']) > 0 and 'scale' in e and int(e['scale']) > 0:
                    type = type(int(e['length']), int(e['scale']))
                elif 'length' in e and int(e['length']) > 0:
                    type = type(int(e['length']))
                else:
                    type = type()
                c = Column(name=e['name'], type_=type, nullable=e['nullable'],
                           server_default=e['default'] if 'default' in e else None)
                if 'primary_key' in e:
                    c.primary_key = e['primary_key']
                if 'autoincrement' in e:
                    c.autoincrement = 'auto' if e['autoincrement'] else False
                t.append_column(c)
            self.metadata.drop_all(self.engine)
            self.metadata.create_all(self.engine)
        except Exception as err:
            logger = logging.getLogger('rear')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
            r = -1
        return r

    def getTableByName(self, table_name, status='A'):
        """
        根据表名查询表信息
        :param table_name: str, 表名
        :param status: str, 查询状态, 为''空字符串时表示不查询状态
        :return: DataTable, 返回表信息，失败时返回None
        """
        d = None
        try:
            t = aliased(DataTable, name='t')
            qry = self.session.query(t)
            qry = qry.filter(t.table_name == table_name)
            if status != '':
                qry = qry.filter(t.status == status)
            d = qry.first()
        except Exception as err:
            logger = logging.getLogger(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name)
            logger.error(err)
        return d


    def getTableColumnsByTableName(self, table_name):
        """
        根据表名查询表数据列的列表
        :param table_name: str, 表名
        :return: list, 数据列的列表
        """
        l = []
        try:
            c = aliased(DataTableColumn, name='c')
            qry = self.session.query(c)
            qry = qry.filter(c.table_name == table_name)
            l = qry.all()
        except Exception as err:
            logger = logging.getLogger(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name)
            logger.error(err)
        return l

    def addDataTable(self, table_name, descr='', status='A'):
        """
        新增数据表信息
        :param table_name: str, 表名
        :param descr: str, 描述
        :param status: str, 状态
        :return: int, 返回0表示新增成功, -1表示新增失败
        """
        try:
            dt = DataTable(table_name=table_name, descr=descr, status=status)
            self.addRecord(dt)
        except Exception as err:
            logger = logging.getLogger(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name)
            logger.error(err)
            return -1
        return 0

    def updateDataTableByName(self, table_name, descr='', status='A'):
        """
        更新表信息
        :param table_name: str, 待更新的表名
        :param descr: str, 描述
        :param status: str, 有效状态
        :return: int, 返回0表示新增成功, -1表示新增失败
        """
        try:
            dt = self.session.query(DataTable).filter(DataTable.table_name == table_name)
            if descr != '':
                dt.update({'descr': descr})
            if status != '':
                dt.update({'status': status})
        except Exception as err:
            logger = logging.getLogger(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name)
            logger.error(err)
            return -1
        return 0

    def addDataTableColumn(self, table_name, column_name, type, length=0, scale=0, primary_key=False,
                           nullable=False,
                           autoincrement=False):
        """
        新增数据表的列信息
        :param table_name: str, 表名
        :param column_name: str, 列名
        :param type: str, 列数据类型
        :param length: str, 列数据长度
        :param scale: str, 小数位数
        :param primary_key: str, 是否主键,'Y'是,'N'否
        :param nullable: str, 允许为空,'Y'是,'N'否
        :param autoincrement: str, 自增长, 'Y'是,'N'否
        :return: int, 返回0表示新增成功, -1表示新增失败
        """
        try:
            tc = DataTableColumn(table_name=table_name, column_name=column_name, type=type, length=length,
                                 scale=scale, primary_key=primary_key, nullable=nullable,
                                 autoincrement=autoincrement)
            self.addRecord(tc)
        except Exception as err:
            logger = logging.getLogger(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name)
            logger.error(err)
            return -1
        return 0

    def updateDataTableColumnByName(self, table_name, column_name, type='', length=0, scale=0, primary_key=False, nullable=False,
                                    autoincrement=False):
        """
        更新数据表的列信息
        :param table_name: str, 表名
        :param column_name: str, 列名
        :param type: str, 列数据类型
        :param length: str, 列数据长度
        :param scale: str, 小数位数
        :param primary_key: str, 是否主键,'Y'是,'N'否
        :param nullable: str, 允许为空,'Y'是,'N'否
        :param autoincrement: str, 自增长, 'Y'是,'N'否
        :return: int, 返回0表示更新成功, -1表示更新失败
        """
        try:
            tc = self.session.query(DataTableColumn).filter(DataTableColumn.table_name == table_name,
                                                            DataTableColumn.column_name == column_name)
            if type != '':
                tc.update({'type': type})
            if length != 0:
                tc.update({'length': length})
            if scale != 0:
                tc.update({'scale': scale})
            tc.update({'primary_key': primary_key})
            tc.update({'nullable': nullable})
            tc.update({'autoincrement': autoincrement})
        except Exception as err:
            logger = logging.getLogger(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name)
            logger.error(err)
            return -1
        return 0

    def delTableColumnsByName(self, table_name):
        """
        删除数据表信息
        :param table_name: str, 数据表名
        :return: int, 返回0表示删除成功, -1表示删除失败
        """
        n = 0
        try:
            qry = self.session.query(DataTableColumn).filter(DataTableColumn.table_name == table_name)
            n = qry.delete()
        except Exception as err:
            logger = logging.getLogger(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name)
            logger.error(err)
            return -1
        return n

    def bulkUpdateTableColumns(self, table_name, columns):
        """
        更新数据表列数据
        :param table_name: str, 表名
        :param columns: list, 数据列列表
        :return: int, 返回0表示更新成功, -1表示删除原有数据列失败, -2表示新增数据列失败
        """
        r = self.delTableColumnsByName(table_name)
        if r < 0:
            return -1
        for e in columns:
            r = self.addDataTableColumn(table_name, e['name'], e['type'], int(e['length'] if 'length' in e else 0),
                                        int(e['scale'] if 'scale' in e else 0),
                                    'Y' if ('primary_key' in e and e['primary_key']) else 'N',
                                    'Y' if ('nullable' in e and e['nullable']) else 'N',
                                    'Y' if ('autoincrement' in e and e['autoincrement']) else 'N')
            if r != 0:
                return -2
        return 0

    def getTableLikeName(self, table_name, status='A'):
        """
        根据表名模糊查询数据表
        :param table_name: str, 表名
        :param status: str, 查询状态, 为''空字符串时表示不查询状态
        :return: list, 数据表列表
        """
        l = []
        try:
            dt = aliased(DataTable, name='dt')
            qry = self.session.query(dt)
            qry = qry.filter(dt.table_name.like('%' + table_name + '%'))
            if status != '':
                qry = qry.filter(dt.status == status)
            l = qry.all()
        except Exception as err:
            logger = logging.getLogger(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name)
            logger.error(err)
        return l

    def getTableLikeDescr(self, descr, status='A'):
        """
        根据数据表描述模糊查询数据表
        :param table_name: str, 表名
        :param status: str, 查询状态, 为''空字符串时表示不查询状态
        :return: list, 数据表列表
        """
        l = []
        try:
            dt = aliased(DataTable, name='dt')
            qry = self.session.query(dt)
            qry = qry.filter(dt.descr.like('%' + descr + '%'))
            if status != '':
                qry = qry.filter(dt.status == status)
            l = qry.all()
        except Exception as err:
            logger = logging.getLogger(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name)
            logger.error(err)
        return l

    def listTables(self, status='A'):
        """
        查询所有数据表信息
        :param status: str, 查询状态, 为''空字符串时表示不查询状态
        :return: list, 数据表列表
        """
        l = []
        try:
            qry = self.session.query(DataTable)
            if status != '':
                qry.filter(DataTable.status == status)
            l = qry.all()
        except Exception as err:
            logger = logging.getLogger(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name)
            logger.error(err)
        return l

    def getTableColumnsDataByName(self, table_name):
        """
        查询数据表列信息
        :param table_name: str, 表名
        :return: list, 数据表列的列表
        """
        r = self.getTableColumnsByTableName(table_name)
        rl = []
        for e in r:
            rl.append({'name': e.column_name, 'type': e.type, 'length': e.length, 'scale': e.scale,
                       'primary_key': True if e.primary_key == 'Y' else False,
                       'nullable': True if e.nullable == 'Y' else False,
                       'autoincrement': True if e.autoincrement == 'Y' else False})
        return rl

    def reflectTables(self):
        """
        映射获得当前数据库内的所有表结构信息并返回
        :return: list, [{'name':str, 'descr':str,'status':True, columns:[]}]
        """
        Base = declarative_base()
        Base.metadata.reflect(ctx.db_engine)
        tables = Base.metadata.tables
        tables = dict(tables)
        l = []
        for e in tables.keys():
            t = {'name': e, 'descr': e, 'status': True}
            columns = dict(tables[e].columns)
            cl = []
            for i in columns.keys():
                ci = columns[i]
                type = columns[i].type.python_type.__name__
                type = self.typeMapping[type]
                c = {'name': i, 'type': type}
                c['primary_key'] = columns[i].primary_key
                c['nullable'] = columns[i].nullable
                if type == 'String':
                    c['length'] = columns[i].type.length
                elif type == 'Integer':
                    c['autoincrement'] = True if columns[i].autoincrement == 'auto' or columns[
                        i].autoincrement else False
                elif type == 'Float' or type == 'DECIMAL':
                    c['length'] = columns[i].type.precision
                    c['precision'] = columns[i].type.scale
                c['order'] = ci._creation_order
                cl.append(c)
            if len(cl) > 0:
                cl.sort(key=lambda e: e['order'])
            for e in cl:
                del (e['order'])
            t['columns'] = cl
            l.append(t)
        return l

    def dumpTable(self, dataJson):
        """
        将数据写入指定的数据库表中
        :param dataJson: json, 数据
        :return: touple,(i, text), 成功则返回(0, ''), 失败则返回(1, err)
        """
        try:
            table_name = dataJson['name']
            data = dataJson['data']
            metadata = MetaData(ctx.db_engine)
            table = Table(table_name, metadata, autoload=True)
            if 'truncate' in dataJson and dataJson['truncate']:
                s = table.delete()
                self.session.execute(s)
                s = self.session.execute(table.insert(), data)
            else:
                s = table.select()
                for d in data:
                    se = s
                    for e in table.primary_key.columns:
                        i = getattr(table.c, e.name)
                        se = se.where(i == d[e.name])
                    r = self.session.execute(se)
                    # if dataJson['truncate']:
                    #     self.session.execute(table.delete())
                    if r.rowcount > 0:
                        u = table.update()
                        for e in table.primary_key.columns:
                            i = getattr(table.c, e.name)
                            u = u.where(i == d[e.name])
                        self.session.execute(u, d)
                    else:
                        self.session.execute(table.insert(), d)
        except Exception as err:
            logger = logging.getLogger('rear')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ':' + str(err))
            return -1, err
        return 0, ''