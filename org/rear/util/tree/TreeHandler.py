# coding=utf-8

"""
树结构业务处理类, 该类函数负责进行数据库事务提交
"""

import sys
from org.rear.util.db.handler.BaseHandler import BaseHandler

from org.rear.util.tree.TreeData import TreeData


class TreeHandler(BaseHandler):
    def addTreeNode(self, tree_code, node_code, parent_node):
        """
        新增树节点
        :param tree_code: str, 树代码
        :param node_code: str, 节点代码
        :param parent_node: str, 父节点代码
        :return: touple, 新节点的编号及末端编号
        """
        d = self.getData(TreeData)
        n1, n2 = d.addTreeNode(tree_code, node_code, parent_node)
        d.commit()
        return n1, n2

    def getTreeNodeByCode(self, tree_code, node_code):
        """
        根据节点代码查询节点对象
        :param tree_code: str, 树代码
        :param code: str, 节点代码
        :param status: str, 查询状态, 为''空字符串时表示不查询状态
        :return: TreeNode, 树节点对象实例
        """
        d = self.getData(TreeData)
        r = d.getTreeNodeByCode(tree_code, node_code)
        return r

    def getAllDescendants(self, tree_code, parent_node):
        """
        查询获得父节点的所有子节点
        :param tree_code: str, 树代码
        :param parent_node: str, 父节点
        :param status: str, 查询状态, 为''空字符串时表示不查询状态
        :return: list, 所有子节点列表
        """
        d = self.getData(TreeData)
        l = d.getAllDescendants(tree_code, parent_node)
        return l

    def getDirectDescendants(self, tree_code, parent_node, status='A'):
        """
        查询获得父节点的直属子节点
        :param tree_code: str, 树名
        :param parent_node: str, 父节点代码
        :param status: str, 查询状态, 为''空字符串时表示不查询状态
        :return: list, 父节点的直属子节点列表
        """
        d = self.getData(TreeData)
        l = d.getDirectDescendants(tree_code, parent_node, status)
        return l

    def getLastOrthology(self, tree_code, parent_node):
        """
        查询父节点最末端的直接子节点
        :param tree_code: str, 树名
        :param parent_node: str, 父节点代码
        :param status: str, 查询状态, 为''空字符串时表示不查询状态
        :return: TreeNode, 父节点最右边的直接子节点, 如果没有返回None
        """
        d = self.getData(TreeData)
        n = d.getLastOrthology(tree_code, parent_node)
        return n

    def getTree(self, params, status='A'):
        """
        根据树代码或者树名模糊查询获得树数据
        :param params: json, 树代码和树名({'tree_code':str, 'name':str})
        :param status: str, 树状态, 'A'-有效, 'I'-无效
        :return: list 树列表
        """
        d = self.getData(TreeData)
        t = d.getTree(params, status)
        return t

    def getTreeNodeData(self, d, tree_code, node_code, status='A'):
        """
        回溯遍历获得查询节点为顶点的子树
        :param d: TreeData, 树结构数据操作类实例,事务处理用
        :param tree_code: str, 树代码
        :param node_code: str, 节点代码
        :param status: str, 查询状态, 为''空字符串时表示不查询状态
        :return: josn, {'node_code': str, 'children':[]}
        """
        node_data = {}
        node_data['node_code'] = node_code
        n = d.getTreeNodeByCode(tree_code, node_code)
        if (n):
            m = d.getRefDescrByCode(tree_code, node_code)
            if (m):
                node_data['name'] = m
            c = d.getDirectDescendants(tree_code, node_code, status)
            children = []
            if (len(c)>0):
                for e in c:
                    n = self.getTreeNodeData(d, tree_code, e.node_code, status)
                    children.append(n)
            if (len(children)>0):
                node_data['children'] = children
        return node_data

    def getTreeData(self, params, status='A'):
        """
        根据树代码或者树名模糊查询获得树数据
        :param params: json, 树代码和树名({'tree_code':str, 'name':str})
        :param status: str, 树状态, 'A'-有效, 'I'-无效
        :return: list 树列表
        """
        d = self.getData(TreeData)
        lt = []
        l = d.getTree(params)
        if len(l) > 0:
            for t in l:
                e = {}
                e['tree_code'] = t.tree_code
                e['name'] = t.name
                e['ref_table'] = t.ref_table
                e['ref_code'] = t.ref_code
                e['ref_descr'] = t.ref_descr
                e['status'] = True if t.status == 'A' else False
                r = d.getTreeRoot(t.tree_code, status)
                if (r):
                    n = self.getTreeNodeData(d, t.tree_code, r.node_code)
                    e['node'] = [n]
                lt.append(e)
        return lt

    def listTrees(self, status='A'):
        """
        查询返回所有树的信息列表
        :param status: str, 查询状态, 为''空字符串时表示不查询状态
        :return: list 所有树的列表
        """
        d = self.getData(TreeData)
        l = d.listTrees(status)
        return l

    def listRefNodes(self, ref_table, ref_code, ref_descr):
        """
        查询返回树的关联表内的数据
        :param ref_table: str, 关联表名
        :param ref_code: str, 关联表代码列名
        :param ref_descr: str, 关联表描述列列名
        :return: list, 关联表内数据列表
        """
        d = self.getData(TreeData)
        n = d.listRefNodes(ref_table, ref_code, ref_descr)
        l = []
        for e in n:
            l.append({'code': e[0], 'name': e[1]})
        return l

    def recursiveAddNode(self, d, tree_code, parent_code, node):
        """
        递归遍历子树, 在树中新增上的子树所有节点
        :param d: TreeData, 树结构数据操作类实例,事务处理用
        :param tree_code: str, 树节点代码
        :param parent_code: str, 父节点代码
        :param node: json, 待插入子树({'node_code':str, 'children':[]})
        :return: 无返回值
        """
        if node['node_code'] == '':
            return
        d.addTreeNode(tree_code, node['node_code'], parent_code)
        if 'children' in node:
            for e in node['children']:
                self.recursiveAddNode(d, tree_code, node['node_code'], e)

    def updateTreeData(self, data):
        """
        全量覆盖更新树数据
        :param data: 树信心
        :return: 无返回
        """
        d = self.getData(TreeData)
        tree_code = data['tree_code']
        name = data['name']
        ref_table = data['ref_table']
        ref_code = data['ref_code']
        ref_descr = data['ref_descr']
        status = 'A' if (data['status'] == True) else 'I'
        t = d.getTreeByCode(tree_code, status="")
        if t:
            d.updateTree(tree_code, name, ref_table, ref_code, ref_descr, status)
        else:
            d.addTree(tree_code, name, ref_table, ref_code, ref_descr, status)
        if 'node' in data:
            node = data['node']
            d.delTreeNodesByTreeCode(tree_code)
            self.recursiveAddNode(d, tree_code, '', node)
        d.commit()