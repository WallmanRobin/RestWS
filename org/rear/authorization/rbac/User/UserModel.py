# coding: utf-8

"""
用户数据模型类
"""

from sqlalchemy import Column, Date, INTEGER, Index, String, VARCHAR, text, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    user_id = Column(INTEGER(), primary_key=True)
    user_code = Column(String(12, 'utf8mb4_unicode_ci'), nullable=False)
    name = Column(String(50, 'utf8mb4_unicode_ci'), nullable=False)
    password = Column(String(128, 'utf8mb4_unicode_ci'), nullable=False)
    hash_code = Column(String(128, 'utf8mb4_unicode_ci'), nullable=False)
    phone = Column(String(32, 'utf8mb4_unicode_ci'), nullable=False)
    email = Column(String(32, 'utf8mb4_unicode_ci'), nullable=False)
    user_type = Column(String(1, 'utf8mb4_unicode_ci'), nullable=False)
    status = Column(String(1, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("'A'"))
    lastupdatedt = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

class UserRole(Base):
    __tablename__ = 'user_role'

    user_code = Column(String(12, 'utf8mb4_unicode_ci'), primary_key=True, nullable=False)
    role_code = Column(String(36, 'utf8mb4_unicode_ci'), primary_key=True, nullable=False)

class UserAvatar(Base):
    __tablename__ = 'user_avatar'

    user_code = Column(String(12, 'utf8mb4_unicode_ci'), primary_key=True, nullable=False)
    avatar = Column(String(128, 'utf8mb4_unicode_ci'), primary_key=True, nullable=False)


class UserWeixin(Base):
    __tablename__ = 'user_weixin'

    user_code = Column(String(12, 'utf8mb4_unicode_ci'), primary_key=True, nullable=False)
    openid_mini = Column(String(64, 'utf8mb4_unicode_ci'), nullable=False)
    openid_offi = Column(String(64, 'utf8mb4_unicode_ci'), nullable=False)
    openid_app = Column(String(64, 'utf8mb4_unicode_ci'), nullable=False)
    unionid = Column(String(64, 'utf8mb4_unicode_ci'), nullable=False)
