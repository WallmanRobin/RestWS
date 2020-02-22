# coding=utf-8

"""
运动员数据模型类
"""

from sqlalchemy import Column, Date, INTEGER, Index, String, VARCHAR, text, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Player(Base):
    __tablename__ = 'player'

    player_code = Column(String(10, 'utf8mb4_unicode_ci'), primary_key=True, nullable=False)
    name = Column(String(50, 'utf8mb4_unicode_ci'), nullable=False)
    al_name = Column(String(50, 'utf8mb4_unicode_ci'), nullable=False)
    uniform_number = Column(String(12, 'utf8mb4_unicode_ci'), nullable=False)
    comment = Column(String(1024, 'utf8mb4_unicode_ci'), nullable=False)
    birthday = Column(Date)
    status = Column(String(1, 'utf8mb4_unicode_ci'), nullable=False)
    course_count = Column(INTEGER(), nullable=False)
    due_dt = Column(Date)
    group = Column(String(6, 'utf8mb4_unicode_ci'), nullable=False)
    contact_phone = Column(String(32, 'utf8mb4_unicode_ci'), nullable=False)
    contact_name = Column(String(50, 'utf8mb4_unicode_ci'), nullable=False)
    d1 = Column(String(32, 'utf8mb4_unicode_ci'), nullable=False)
    d2 = Column(String(32, 'utf8mb4_unicode_ci'), nullable=False)
    d3 = Column(String(32, 'utf8mb4_unicode_ci'), nullable=False)
    d4 = Column(String(32, 'utf8mb4_unicode_ci'), nullable=False)
    d5 = Column(String(32, 'utf8mb4_unicode_ci'), nullable=False)
    d6 = Column(String(32, 'utf8mb4_unicode_ci'), nullable=False)
    d7 = Column(String(32, 'utf8mb4_unicode_ci'), nullable=False)
    batch_id = Column(
        String(20, 'utf8mb4_unicode_ci'),
        server_default=text("''"),
        nullable=False)

class PlayerAvatar(Base):
    __tablename__ = 'player_avatar'

    player_code = Column(String(10, 'utf8mb4_unicode_ci'), primary_key=True, nullable=False)
    avatar = Column(String(128, 'utf8mb4_unicode_ci'), primary_key=True, nullable=False)


class PlayerOff(Base):
    __tablename__ = 'player_off'

    player_code = Column(String(10, 'utf8mb4_unicode_ci'), primary_key=True, nullable=False)
    start_dt = Column(Date, primary_key=True, nullable=False)
    end_dt = Column(Date, primary_key=True, nullable=False)
    timegroup = Column(String(32, 'utf8mb4_unicode_ci'), nullable=False)
    course_count = Column(INTEGER(), nullable=False)
    type = Column(String(2, 'utf8mb4_unicode_ci'), nullable=False)
    comment = Column(String(256, 'utf8mb4_unicode_ci'), nullable=False)


class PlanTimeline(Base):
    __tablename__ = 'plan_timeline'

    timegroup = Column(String(32, 'utf8mb4_unicode_ci'), primary_key=True, nullable=False)
    descr = Column(String(128, 'utf8mb4_unicode_ci'), nullable=False)
    timeline = Column(String(10, 'utf8mb4_unicode_ci'), nullable=False)
    before = Column(INTEGER(), nullable=False)
    eff_status = Column(String(1, 'utf8mb4_unicode_ci'), nullable=False)
