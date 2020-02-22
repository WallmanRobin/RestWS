# coding: utf-8

"""
角色数据模型类
"""

from sqlalchemy import Column, INTEGER, String, text, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Role(Base):
    __tablename__ = 'role'

    role_id = Column(INTEGER(), nullable=False, primary_key=True)
    role_code = Column(String(36, 'utf8mb4_unicode_ci'), nullable=False)
    name = Column(String(50, 'utf8mb4_unicode_ci'), nullable=False)
    status = Column(String(1, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("'A'"))
    lastupdateby = Column(String(12, 'utf8mb4_unicode_ci'), nullable=False)
    lastupdatedt = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

class RoleEndpoint(Base):
    __tablename__ = 'role_endpoint'

    role_code = Column(String(36, 'utf8mb4_unicode_ci'), primary_key=True, nullable=False)
    endpoint = Column(String(256, 'utf8mb4_unicode_ci'), primary_key=True, nullable=False)
    method = Column(String(16, 'utf8mb4_unicode_ci'), primary_key=True, nullable=False)

class RoleViewroute(Base):
    __tablename__ = 'role_viewroute'

    role_code = Column(String(36, 'utf8mb4_unicode_ci'), primary_key=True, nullable=False)
    viewroute = Column(String(256, 'utf8mb4_unicode_ci'), primary_key=True, nullable=False)
    leaf = Column(String(1, 'utf8mb4_unicode_ci'), nullable=False)