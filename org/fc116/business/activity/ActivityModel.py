# coding=utf-8

"""
活动数据模型类
"""

from sqlalchemy import Column, Date, INTEGER, Index, String, DECIMAL, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ActivityTrack(Base):
    __tablename__ = 'activity_track'
    __table_args__ = (Index('IDX1_ACTIVITY', 'activity_type', 'player_code',
                            'track_dt', 'eff_status', 'location'), )

    track_id = Column(INTEGER(), primary_key=True)
    activity_type = Column(
        String(1, 'utf8mb4_unicode_ci'),
        nullable=False,
        server_default=text("'C'"))
    player_code = Column(String(10, 'utf8mb4_unicode_ci'), nullable=False)
    track_dt = Column(Date, nullable=False)
    eff_status = Column(
        String(1, 'utf8mb4_unicode_ci'),
        nullable=False,
        server_default=text("'A'"))
    track_num = Column(INTEGER(), nullable=False)
    location = Column(String(128, 'utf8mb4_unicode_ci'), nullable=False)
    enroll_status = Column(
        String(1, 'utf8mb4_unicode_ci'),
        nullable=False,
        server_default=text("'A'"))
    attend_status = Column(
        String(1, 'utf8mb4_unicode_ci'),
        nullable=False,
        server_default=text("'A'"))
    accomp_status = Column(
        String(1, 'utf8mb4_unicode_ci'),
        nullable=False,
        server_default=text("'A'"))
    batch_id = Column(
        String(20, 'utf8mb4_unicode_ci'),
        server_default=text("''"),
        nullable=False)


class ActivityTrans(Base):
    __tablename__ = 'activity_trans'
    __table_args__ = (Index('IDX_PLAYER_ACTIVITY', 'player_code',
                            'activity_type'), )

    trans_id = Column(INTEGER(), primary_key=True)
    player_code = Column(String(10, 'utf8mb4_unicode_ci'), nullable=False)
    eff_status = Column(
        String(1, 'utf8mb4_unicode_ci'),
        nullable=False,
        server_default=text("'A'"))
    activity_type = Column(
        String(1, 'utf8mb4_unicode_ci'),
        nullable=False,
        server_default=text("'C'"))
    trans_type = Column(
        String(1, 'utf8mb4_unicode_ci'),
        nullable=False,
        server_default=text("'B'"))
    begin_dt = Column(Date)
    end_dt = Column(Date, server_default=text("'2099-12-31'"))
    trans_num = Column(INTEGER(), nullable=False, server_default=text("'0'"))
    unit_price = Column(DECIMAL(13, 2), nullable=False, server_default=text("'0'"))
    currency = Column(
        String(6, 'utf8mb4_unicode_ci'),
        nullable=False,
        server_default=text("'RMB'"))
    trans_dt = Column(Date)
    batch_id = Column(
        String(20, 'utf8mb4_unicode_ci'),
        server_default=text("''"),
        nullable=False)