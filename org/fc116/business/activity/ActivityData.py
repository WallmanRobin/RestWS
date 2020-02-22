# coding=utf-8

"""
活动数据操作类, 该类函数不会进行数据库事务提交
"""

import logging
import sys
from org.rear.util.db.data.BaseData import BaseData
from sqlalchemy.orm import aliased
from sqlalchemy.sql import func

from org.fc116.business.activity.ActivityModel import ActivityTrans, ActivityTrack


class ActivityData(BaseData):
    def addActivityTrans(self,
                         player_code='',
                         eff_status='A',
                         activity_type='C',
                         trans_type='B',
                         begin_dt='',
                         end_dt='2099-12-31',
                         trans_num=0,
                         unit_price=0,
                         currency='RMB',
                         trans_dt='',
                         batch_id=''):
        """
        新增活动交易记录
        :param player_code: str, 运动员代码
        :param eff_status: str, 交易有效状态, 'A'-有效, 'I'-无效
        :param activity_type: str, 活动类型, '课程类'-C, '活动类'-A, '内部比赛类'-I, '外部比赛类'-M...
        :param trans_type: str, 交易类型, '购买类'-P, '转移类'-T, '赠送类'-F...
        :param begin_dt: str, 开始日期, 活动开始日期
        :param end_dt: str, 结束日期, 活动结束日期
        :param trans_num: int, 交易数量
        :param unit_price: DECIMAL(13, 2), 交易单价
        :param currency: str, 交易货币
        :param trans_dt: str, 交易日期
        :param batch_id: str, 交易批次id
        :return: int, 0-新增成功, 1-新增失败
        """
        r = 0
        try:
            at = ActivityTrans(
                player_code=player_code,
                eff_status=eff_status,
                activity_type=activity_type,
                trans_type=trans_type,
                begin_dt=begin_dt,
                end_dt=end_dt,
                trans_num=trans_num,
                unit_price=unit_price,
                currency=currency,
                trans_dt=trans_dt,
                batch_id=batch_id)
            self.addRecord(at)
        except Exception as err:
            logger = logging.getLogger('fc116')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
            return -1
        return r

    def getActivityTransByPlayerCode(self,
                                   player_code='',
                                   eff_status='A',
                                   activity_type='C'):
        """
        根据运动员代码查询活动交易记录
        :param player_code: str, 运动员代码
        :param eff_status: str, 交易有效状态, 'A'-有效, 'I'-无效
        :param activity_type: str, 活动类型, '课程类'-C, '活动类'-A, '内部比赛类'-I, '外部比赛类'-M...
        :return: list, 活动交易记录列表
        """
        l = []
        try:
            qry = self.session.query(ActivityTrans)
            if eff_status != '':
                qry = qry.filter(ActivityTrans.eff_status == eff_status)
            qry = qry.filter(ActivityTrans.player_code == player_code,
                             ActivityTrans.activity_type == activity_type)
            l = qry.order_by(ActivityTrans.player_code,
                                ActivityTrans.trans_dt.desc()).all()
        except Exception as err:
            logger = logging.getLogger('fc116')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
        return l

    def updateActivityTrans(self,
                            trans_id=0,
                            player_code='',
                            eff_status='',
                            activity_type='C',
                            trans_type='',
                            begin_dt='',
                            end_dt='',
                            trans_num=0,
                            unit_price=0,
                            currency='',
                            trans_dt='',
                            batch_id=''):
        """
        更新指定的活动交易记录
        :param trans_id: int, 活动交易id
        :param player_code: str, 运动员代码
        :param eff_status: str, 交易有效状态, 'A'-有效, 'I'-无效
        :param activity_type: str, 活动类型, '课程类'-C, '活动类'-A, '内部比赛类'-I, '外部比赛类'-M...
        :param trans_type: str, 交易类型, '购买类'-P, '转移类'-T, '赠送类'-F...
        :param begin_dt: str, 开始日期, 活动开始日期
        :param end_dt: str, 结束日期, 活动结束日期
        :param trans_num: int, 交易数量
        :param unit_price: DECIMAL(13, 2), 交易单价
        :param currency: str, 交易货币
        :param trans_dt: str, 交易日期
        :param batch_id: str, 交易批次id
        :return: int, 0-更新成功, 1-更新失败
        """
        try:
            at = self.session.query(ActivityTrans).filter(
                ActivityTrans.trans_id == trans_id)
            if player_code != '':
                at.update({'player_code': player_code})
            if eff_status != '':
                at.update({'eff_status': eff_status})
            if activity_type != '':
                at.update({'activity_type': activity_type})
            if trans_type != '':
                at.update({'trans_type': trans_type})
            if begin_dt != '':
                at.update({'begin_dt': begin_dt})
            if end_dt != '':
                at.update({'end_dt': end_dt})
            if trans_num != 0:
                at.update({'trans_num': trans_num})
            if unit_price != 0:
                at.update({'unit_price': unit_price})
            if currency != '':
                at.update({'currency': currency})
            if trans_dt != '':
                at.update({'trans_dt': trans_dt})
            if batch_id != '':
                at.update({'batch_id': batch_id})
        except Exception as err:
            logger = logging.getLogger('fc116')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
            return -1
        return 0

    def addActivityTrack(self,
                         activity_type='C',
                         player_code='',
                         track_dt='',
                         eff_status='A',
                         track_num=0,
                         location='',
                         enroll_status='A',
                         attend_status='A',
                         accomp_status='A',
                         batch_id=''):
        """
        新增活动记录信息
        :param activity_type: str, 活动类型, '课程类'-C, '活动类'-A, '内部比赛类'-I, '外部比赛类'-M...
        :param player_code: str, 运动员代码
        :param track_dt: str, 记录日期, 活动记录日期
        :param eff_status: str, 交易有效状态, 'A'-有效, 'I'-无效
        :param track_num: int, 活动时数
        :param location: str, 地点
        :param enroll_status: 预约状态, 'A'-有效, 'I'-无效
        :param attend_status: 出席状态, 'A'-有效, 'I'-无效
        :param accomp_status: 完成状态, 'A'-有效, 'I'-无效
        :param batch_id: str, 交易批次id
        :return: int, 0-新增成功, 1-新增失败
        """
        try:
            c = ActivityTrack(
                activity_type=activity_type,
                player_code=player_code,
                track_dt=track_dt,
                eff_status=eff_status,
                track_num=track_num,
                location=location,
                enroll_status=enroll_status,
                attend_status=attend_status,
                accomp_status=accomp_status,
                batch_id=batch_id)
            self.addRecord(c)
        except Exception as err:
            logger = logging.getLogger('fc116')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
            return -1
        return 0


    def getActivityTrackByPlayerCode(self,
                                   player_code='',
                                   eff_status='A',
                                   activity_type='C',
                                   rownum=0):
        """
        根据运动员代码查询运动员活动参加情况，按记录日期倒序排列
        :param player_code: 运动员代码
        :param eff_status: 活动记录有效状态, 'A'-有效, 'I'-无效
        :param activity_type: str, 活动类型, '课程类'-C, '活动类'-A, '内部比赛类'-I, '外部比赛类'-M...
        :param rownum: 返回记录条数
        :return: list, 运动员活动参加情况数组
        """
        l = []
        try:
            qry = self.session.query(ActivityTrack)
            if eff_status != '':
                qry = qry.filter(ActivityTrack.eff_status == eff_status)
            qry = qry.filter(ActivityTrack.player_code == player_code,
                             ActivityTrack.activity_type == activity_type)
            qry = qry.order_by(ActivityTrack.player_code,
                                ActivityTrack.track_dt.desc())
            if rownum>0:
                qry = qry.limit(rownum)
            l = qry.all()
        except Exception as err:
            logger = logging.getLogger('fc116')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
        return l

    def updateActivityTrack(self,
                           track_id=0,
                           activity_type='C',
                           player_code='',
                           track_dt='',
                           eff_status='A',
                           track_num=0,
                           location='',
                           enroll_status='A',
                           attend_status='A',
                           accomp_status='A',
                           batch_id=''):
        """
        更新运动员活动参与情况
        :param track_id: int 记录id
        :param activity_type: str, 活动类型, '课程类'-C, '活动类'-A, '内部比赛类'-I, '外部比赛类'-M...
        :param player_code: str, 运动员代码
        :param track_dt: str, 记录日期, 活动记录日期
        :param eff_status: str, 交易有效状态, 'A'-有效, 'I'-无效
        :param track_num: int, 活动时数
        :param location: str, 地点
        :param enroll_status: str, 预约状态, 'A'-有效, 'I'-无效
        :param attend_status: str, 出席状态, 'A'-有效, 'I'-无效
        :param accomp_status: str, 完成状态, 'A'-有效, 'I'-无效
        :param batch_id: str, 交易批次id
        :return: int, 0-更新成功, 1-更新失败
        """
        try:
            at = self.session.query(ActivityTrack).filter(
                ActivityTrack.track_id == track_id)
            if activity_type != '':
                at.update({'activity_type': activity_type})
            if player_code != '':
                at.update({'player_code': player_code})
            if track_dt != '' or track_dt is None:
                at.update({'track_dt': track_dt})
            if eff_status != '':
                at.update({'eff_status': eff_status})
            if track_num != '':
                at.update({'track_num': track_num})
            if location != '':
                at.update({'location': location})
            if enroll_status != '':
                at.update({'enroll_status': enroll_status})
            if attend_status != '':
                at.update({'attend_status': attend_status})
            if accomp_status != '':
                at.update({'accomp_status': accomp_status})
            if batch_id != '':
                at.update({'batch_id': batch_id})
        except Exception as err:
            logger = logging.getLogger('fc116')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
            r = -1
        return 0

    def getActivityTransSumByPlayerCode(self,
                                    player_code='',
                                    trans_type='B',
                                    activity_type='C'):
        """
        根据运动员代码查询运动员获得的类型活动总数
        :param player_code: 运动员代码
        :param trans_type: str, 交易类型, '购买类'-P, '转移类'-T, '赠送类'-F...
        :param activity_type: str, 活动类型, '课程类'-C, '活动类'-A, '内部比赛类'-I, '外部比赛类'-M...
        :return: int 活动总数，如果返回-1，说明查询失败
        """
        r = -1
        try:
            at = aliased(ActivityTrans, name='at')
            qry = self.session.query(func.sum(at.trans_num).label("trans_num"))
            qry = qry.filter(at.player_code == player_code, at.eff_status == 'A',
                             at.trans_type == trans_type,
                             at.activity_type == activity_type)
            qry = qry.group_by(at.player_code)
            r = qry.first()
        except Exception as err:
            logger = logging.getLogger('fc116')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
        return r

    def getActivityTrackCountByPlayerCode(self, player_code='', type='C'):
        """
        根据运动员代码查询运动员参与的类型活动总数
        :param player_code: str, 运动员代码
        :param type: str, 活动类型, '课程类'-C, '活动类'-A, '内部比赛类'-I, '外部比赛类'-M...
        :return: int 活动总数，如果返回-1，说明查询失败
        """
        r = -1
        try:
            at = aliased(ActivityTrack, name='at')
            qry = self.session.query(func.sum(at.track_num).label("track_num"))
            if type != '':
                qry = qry.filter(at.activity_type == type)
            qry = qry.filter(at.eff_status == 'A', at.player_code == player_code)
            qry = qry.group_by(at.player_code)
            r = qry.first()
        except Exception as err:
            logger = logging.getLogger('fc116')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
        return r

    def getActivityFreeSumByPlayerCode(self, player_code):
        """
        根据运动员代码查询运动员获赠的某类型活动总数
        :param player_code: str, 运动员代码
        :return: int 活动总数，如果返回-1，说明查询失败
        """
        r = -1
        try:
            at = aliased(ActivityTrans, name='at')
            qry = self.session.query(func.sum(at.trans_num).label("num_present"))
            qry = qry.filter(at.eff_status == 'A', at.activity_type == 'F',
                             at.player_code == player_code)
            qry = qry.group_by(at.player_code)
            r = qry.first()
        except Exception as err:
            logger = logging.getLogger('fc116')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
        return r

    def truncateActivityTrack(self):
        """
        清空活动记录表
        :return: 0-删除成功, -1-删除失败
        """
        try:
            self.session.query(ActivityTrack).delete()
        except Exception as err:
            logger = logging.getLogger('fc116')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
            r = -1
        return 0
