# coding=utf-8

"""
树结构数据操作类, 该类函数不会进行数据库事务提交
"""

import logging
import sys
from org.rear.util.db.data.BaseData import BaseData
from sqlalchemy import text
from sqlalchemy.orm import aliased
from sqlalchemy.sql import func

from org.rear.util.tree.TreeModel import TreeNode, Tree


class TreeData(BaseData):
    def __init__(self, connStr, treeName='', nodeList = []):
        """
        初始化函数, 初始化树对象的变量
        :param connStr: str, 数据库链接字符串
        :param treeName: str, 树名
        :param nodeList: list, 树节点列表
        """
        super().__init__(connStr)
        self.nodeList = nodeList
        self.treeName = treeName

    def listTrees(self, status='A'):
        """
        查询返回所有树的信息列表
        :param status: str, 查询状态, 为''空字符串时表示不查询状态
        :return: list 所有树的列表
        """
        qry = self.session.query(Tree)
        if status != '':
            qry = qry.filter(Tree.status==status)
        return qry.all()

    def listRefNodes(self, ref_table, ref_code, ref_descr):
        """
        查询返回树的关联表内的数据
        :param ref_table: str, 关联表名
        :param ref_code: str, 关联表代码列名
        :param ref_descr: str, 关联表描述列列名
        :return: list, 关联表内数据列表
        """
        sql = 'select ' + ref_code +',' + ref_descr + ' from ' + ref_table
        n = []
        try:
            n = self.session.execute(text(sql)).fetchall()
        except Exception as err:
            logger = logging.getLogger(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name)
            logger.error(err)
        return n

    def getTreeLikeCode(self, code, status='A'):
        """
        根据代码模糊查询树数据
        :param code: str, 树代码
        :param status: str, 查询状态, 为''空字符串时表示不查询状态
        :return: list, 树列表
        """
        qry = self.session.query(Tree)
        qry = qry.filter(Tree.tree_code.like('%' + code + '%'))
        if status != '':
            qry = qry.filter(Tree.status==status)
        return qry.all()

    def getTreeLikeName(self, name, status='A'):
        """
        根据名称模糊查询树数据
        :param name: str, 树名称
        :param status: str, 查询状态, 为''空字符串时表示不查询状态
        :return: list, 树列表
        """
        qry = self.session.query(Tree)
        qry = qry.filter(Tree.name.like('%' + name + '%'))
        if status != '':
            qry = qry.filter(Tree.status==status)
        return qry.all()

    def getTreeByCode(self, code, status='A'):
        """
        根据代码查询树数据
        :param code: str, 树代码
        :param status: str, 查询状态, 为''空字符串时表示不查询状态
        :return: Tree, 树对象实例, 无数据时返回None
        """
        qry = self.session.query(Tree)
        qry = qry.filter(Tree.tree_code == code)
        if status != '':
            qry = qry.filter(Tree.status==status)
        return qry.first()

    def getTreeByName(self, name, status='A'):
        """
        根据代码查询树数据
        :param code: str, 树代码
        :param status: str, 查询状态, 为''空字符串时表示不查询状态
        :return: list, 树对象实例列表
        """
        qry = self.session.query(Tree)
        qry = qry.filter(Tree.name == name)
        if status != '':
            qry = qry.filter(Tree.status==status)
        return qry.all()

    def getTreeNodeByCode(self, tree_code, code, status='A'):
        """
        根据节点代码查询节点对象
        :param tree_code: str, 树代码
        :param code: str, 节点代码
        :param status: str, 查询状态, 为''空字符串时表示不查询状态
        :return: TreeNode, 树节点对象实例
        """
        qry = self.session.query(TreeNode)
        qry = qry.filter(TreeNode.tree_code == tree_code, TreeNode.node_code == code)
        if status != '':
            qry = qry.filter(TreeNode.status==status)
        return qry.first()

    def addNode(self, tree_code, node_code, parent_node, node_num, node_num_end, status='A'):
        """
        新增节点数据信息
        :param tree_code: str, 树名称
        :param node_code: str, 节点名称
        :param parent_node: str, 父节点名称
        :param node_num: int, 节点编号
        :param node_num_end: int, 节点末端编号(该节点的子节点的最大编号值)
        :param status: 状态
        :return: int, 0-新增成功, -1-新增失败
        """
        treeNode = TreeNode(
            tree_code = tree_code,
            node_code = node_code,
            parent_node = parent_node,
            node_num = node_num,
            node_num_end = node_num_end,
            status = status)
        try:
            self.addRecord(treeNode)
        except Exception as err:
            logger = logging.getLogger(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name)
            logger.error(err)
            return -1
        return 0

    def updateTreeNode(self,node_id, tree_code='', node_code='', parent_node='', node_num='', node_num_end='', status=''):
        """
        更新节点数据信息
        :param tree_code: str, 树名称
        :param node_code: str, 节点名称
        :param parent_node: str, 父节点名称
        :param node_num: int, 节点编号
        :param node_num_end: int, 节点末端编号(该节点的子节点的最大编号值)
        :param status: 状态
        :return: int, 0-更新成功, -1-更新失败
        """
        try:
            n = self.session.query(TreeNode).filter(
                TreeNode.node_id == node_id)
            if tree_code != '':
                n.update({'tree_code': tree_code})
            if node_code != '':
                n.update({'node_code': node_code})
            if parent_node != '':
                n.update({'parent_node': parent_node})
            if node_num != '':
                n.update({'node_num': node_num})
            if node_num_end != '':
                n.update({'node_num_end': node_num_end})
            if status != '':
                n.update({'status': status})
        except Exception as err:
            logger = logging.getLogger(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name)
            logger.error(err)
            return -1
        return 0

    def getLastOrthology(self, tree_code, parent_node, status='A'):
        """
        查询父节点最末端的直接子节点
        :param tree_code: str, 树名
        :param parent_node: str, 父节点代码
        :param status: str, 查询状态, 为''空字符串时表示不查询状态
        :return: TreeNode, 父节点最右边的直接子节点, 如果没有返回None
        """
        child = aliased(TreeNode, name='child')
        tree = aliased(TreeNode, name='tree')
        sub = self.session.query(func.max(child.node_num).label('maxNum'))
        sub = sub.filter(child.tree_code == tree_code, child.parent_node == parent_node,
                         child.status =='A', ).subquery()
        qry = self.session.query(tree)
        qry = qry.filter(tree.node_code != tree.parent_node, tree.tree_code==tree_code, tree.parent_node==parent_node, tree.node_num==sub.c.maxNum)
        if status != '':
            qry = qry.filter(tree.status == 'A')
        return qry.first()

    def getAllDescendants(self, tree_code, parent_node, status='A'):
        """
        查询获得父节点的所有子节点
        :param tree_code: str, 树代码
        :param parent_node: str, 父节点
        :param status: str, 查询状态, 为''空字符串时表示不查询状态
        :return: list, 所有子节点列表
        """
        child = aliased(TreeNode, name='child')
        tree = aliased(TreeNode, name='tree')

        qry = self.session.query(child)
        qry = qry.filter(child.tree_code == tree_code, child.tree_code == tree.tree_code, tree.node_code == parent_node,
                         child.node_num > tree.node_num, child.node_num <= tree.node_num_end)
        if status != '':
            qry = qry.filter(child.status == status)
        return qry.all()

    def getDirectDescendants(self, tree_code, parent_node, status='A'):
        """
        查询获得父节点的直属子节点
        :param tree_code: str, 树名
        :param parent_node: str, 父节点代码
        :param status: str, 查询状态, 为''空字符串时表示不查询状态
        :return: list, 父节点的直属子节点列表
        """
        tree = aliased(TreeNode, name='tree')
        qry = self.session.query(tree)
        qry = qry.filter(tree.tree_code==tree_code, tree.parent_node==parent_node)
        if status != '':
            qry = qry.filter(tree.status == status)
        return qry.all()

    def addTree(self, tree_code, name='', ref_table='', ref_code='', ref_descr='', status=''):
        """
        增加树数据
        :param tree_code: str, 树代码
        :param name: str, 树名
        :param ref_table: str, 关联表名
        :param ref_code: str, 关联代码列
        :param ref_descr: str, 关联描述列
        :param status: str, 树状态, 'A'-有效, 'I'-无效
        :return: int, 0-新增成功, -1-新增失败
        """
        tree = Tree(
            tree_code = tree_code,
            name = name,
            ref_table = ref_table,
            ref_code = ref_code,
            ref_descr = ref_descr,
            status = status)
        try:
            self.addRecord(tree)
        except Exception as err:
            logger = logging.getLogger(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name)
            logger.error(err)
            return -1
        return 0

    def getTree(self, params, status='A'):
        """
        根据树代码或者树名模糊查询获得树数据
        :param params: json, 树代码和树名({'tree_code':str, 'name':str})
        :param status: str, 树状态, 'A'-有效, 'I'-无效
        :return: list 树列表
        """
        code = params['tree_code']
        name = params['name']
        l = []
        if code and code != '':
            l = self.getTreeLikeCode(code, status)
        elif name and name != '':
            l =  self.getTreeLikeName(name, status)
        return l

    def updateTree(self, tree_code, name='', ref_table='', ref_code='', ref_descr='', status=''):
        """
        更新树数据
        :param tree_code: str, 树代码
        :param name: str, 树名
        :param ref_table: str, 关联表名
        :param ref_code: str, 关联代码列
        :param ref_descr: str, 关联描述列
        :param status: str, 树状态, 'A'-有效, 'I'-无效
        :return: int, 0-更新成功, -1-更新失败
        """
        try:
            t = self.session.query(Tree).filter(
                Tree.tree_code == tree_code)
            if name != '':
                t.update({'name': name})
            if ref_table != '':
                t.update({'ref_table': ref_table})
            if ref_table != '':
                t.update({'ref_code': ref_code})
            if ref_table != '':
                t.update({'ref_descr': ref_descr})
            if status != '':
                t.update({'status': status})
        except Exception as err:
            logger = logging.getLogger(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name)
            logger.error(err)
            return -1
        return 0

    def getRefDescrByCode(self, tree_code, code):
        """
        从树关联表查询关联代码对应的描述
        :param tree_code: str, 树代码
        :param code: str, 关联代码
        :return: str, 关联代码对应的描述
        """
        tree = self.getTreeByCode(tree_code)
        r = None
        if (tree):
            rt = tree.ref_table
            rc = tree.ref_code
            rd = tree.ref_descr

            sql = 'select '+ rd + ' from ' + rt + ' where ' + rc + ' = :code'
            d = self.session.execute(text(sql), {"code": code}).first()
            if (d):
                r = d[0]
        return r

    def getTreeRoot(self, tree_code, status='A'):
        """
        查询获得树的根节点(根节点的parent_node列值为空字符串'')
        :param tree_code: str, 树代码
        :param status: str, 树状态, 'A'-有效, 'I'-无效
        :return: TreeNode, 树的根节点实例
        """
        qry = self.session.query(TreeNode)
        qry = qry.filter(TreeNode.tree_code == tree_code, TreeNode.parent_node == '')
        if status != '':
            qry = qry.filter(TreeNode.status == status)
        return qry.first()

    def delTreeNodesByTreeCode(self, tree_code):
        """
        从树中删除指定树的所有结点
        :param tree_code:
        :return: 无返回值-
 *+
        *"""
        qry = self.session.query(TreeNode).filter(TreeNode.tree_code == tree_code)
        n = qry.delete()
        return n
    
    def addTreeNode(self, tree_code, node_code, parent_node):
        """
        新增树节点
        :param tree_code: str, 树代码
        :param node_code: str, 节点代码
        :param parent_node: str, 父节点代码
        :return: touple, 新节点的编号及末端编号
        """
        lastChild = self.getLastOrthology(tree_code, parent_node)
        parentNode = self.getTreeNodeByCode(tree_code, parent_node)
        if parentNode is not None:
            nodeNum = -1
            nodeNumEnd = -1
            # 父节点有子节点
            if lastChild is not None:
                nodeNum = lastChild.node_num_end + 1
                nodeNumEnd = (nodeNum + parentNode.node_num_end) / 2
                self.addNode(tree_code, node_code, parent_node, nodeNum, nodeNumEnd)
                return nodeNum, nodeNumEnd
            else:
                nodeNum = parentNode.node_num + 1
                nodeNumEnd = (nodeNum + parentNode.node_num_end) / 2
                if nodeNum <= nodeNumEnd:
                    self.addNode(tree_code, node_code, parent_node, nodeNum, nodeNumEnd)
                    return nodeNum, nodeNumEnd
                else:
                    return -1, -1
        else:
            self.addNode(tree_code, node_code, '', 1, 2147483647)
            return 1, 2147483647