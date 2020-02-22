# coding=utf-8

"""
数据表数据模型类
"""

from sqlalchemy import Column, Date, Integer, Index, String, VARCHAR, text, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DataTable(Base):
    __tablename__ = 'data_table'

    table_name = Column(String(128, 'utf8mb4_unicode_ci'), primary_key=True, nullable=False)
    descr = Column(String(255, 'utf8mb4_unicode_ci'), nullable=False)
    status = Column(String(1, 'utf8mb4_unicode_ci'), server_default=text("'A'"))

class DataTableColumn(Base):
    __tablename__ = 'data_tablecolumns'

    table_name = Column(String(128, 'utf8mb4_unicode_ci'),primary_key=True,  nullable=False)
    column_name = Column(String(128, 'utf8mb4_unicode_ci'),primary_key=True, nullable=False)
    type = Column(String(32, 'utf8mb4_unicode_ci'), nullable=False)
    length = Column(Integer(), nullable=False)
    scale = Column(Integer(), nullable=False)
    primary_key = Column(String(1, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("'N'"))
    nullable = Column(String(1, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("'N'"))
    autoincrement = Column(String(1, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("'N'"))