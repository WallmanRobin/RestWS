# coding=utf-8

"""
树结构数据模型类
"""

from sqlalchemy import Column, Date, INTEGER, Index, String, VARCHAR, text, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Tree(Base):
    __tablename__ = 'tree'

    tree_id = Column(INTEGER(), primary_key=True)
    tree_code = Column(String(50, 'utf8mb4_unicode_ci'), nullable=False)
    name = Column(String(50, 'utf8mb4_unicode_ci'), nullable=False)
    ref_table = Column(String(50, 'utf8mb4_unicode_ci'), nullable=False)
    ref_code = Column(String(50, 'utf8mb4_unicode_ci'), nullable=False)
    ref_descr = Column(String(255, 'utf8mb4_unicode_ci'), nullable=False)
    status = Column(String(1, 'utf8mb4_unicode_ci'), server_default=text("'A'"))

class TreeNode(Base):
    __tablename__ = 'tree_node'

    node_id = Column(INTEGER(), primary_key=True)
    tree_code = Column(String(50, 'utf8mb4_unicode_ci'), nullable=False)
    node_code = Column(String(50, 'utf8mb4_unicode_ci'), nullable=False)
    parent_node = Column(String(50, 'utf8mb4_unicode_ci'), nullable=False)
    node_num = Column(INTEGER(), nullable=False)
    node_num_end = Column(INTEGER(), nullable=False)
    status = Column(String(1, 'utf8mb4_unicode_ci'), server_default=text("'A'"))