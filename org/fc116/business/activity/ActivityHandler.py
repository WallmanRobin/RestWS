# coding=utf-8

"""
活动业务处理类, 该类函数负责进行数据库事务提交
"""

import logging
import sys
from org.rear.util.db.handler.BaseHandler import BaseHandler

from org.fc116.business.activity.ActivityData import ActivityData


class ActivityHandler(BaseHandler):
    def getActivityTrackCountByPlayercode(self,
                                          player_code='',
                                          activity_type='C'):
        """
        根据运动员代码查询运动员参与的类型活动总数
        :param player_code: str, 运动员代码
        :param type: str, 活动类型, '课程类'-C, '活动类'-A, '内部比赛类'-I, '外部比赛类'-M...
        :return: int 活动总数，如果返回-1，说明查询失败
        """
        d = self.__getData(ActivityData)
        return d.getActivityTrackCountByPlayerCode(player_code, activity_type)

    def addActivityTrans(self,
                         player_code=0,
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
        :return: int, 0-新增成功, -1-数据处理时失败,-2提交时失败
        """
        r = -2
        try:
            d = self.getData(ActivityData)
            r = d.addActivityTrans(player_code, eff_status,
                                   activity_type, trans_type,
                                   begin_dt[0:10] if begin_dt != '' else None, end_dt,
                                   trans_num, unit_price, currency,
                                   trans_dt[0:10] if trans_dt != '' else None, batch_id)
            if r == 0:
                d.commit()
            else:
                d.rollback()
        except Exception as err:
            logger = logging.getLogger('fc116')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
            return -2
        return r

    def updateActivityTrans(self,
                            trans_id,
                            player_code=0,
                            eff_status='',
                            activity_type='',
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
        :return: int, 0-新增成功, -1-数据处理时失败,-2提交时失败
        """
        try:
            d = self.getData(ActivityData)
            r = d.updateActivityTrans(trans_id, player_code, eff_status,
                                      activity_type, trans_type, begin_dt, end_dt,
                                      trans_num, unit_price, currency, trans_dt,
                                      batch_id)
            if r == 0:
                d.commit()
            else:
                d.rollback()
            d.commit if r == 0 else d.rollback()
            return r
        except Exception as err:
            logger = logging.getLogger('fc116')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
            return -2

    def getActivityTransByName(self,
                               name='',
                               eff_status='A',
                               activity_type='C'):
        """
        根据球员姓名查询球员活动交易记录
        :param name: str, 球员姓名
        :param eff_status: str, 交易有效状态
        :param activity_type: str, 活动类型, '课程类'-C, '活动类'-A, '内部比赛类'-I, '外部比赛类'-M...
        :return: list, 球员活动交易记录列表
        """
        d = self.getData(ActivityData)
        l = self.getPlayerByName(name)
        ll = []
        for e in l:
            ll.extend(
                d.getActivityTransByPlayerCode(e.player_code, eff_status,
                                               activity_type))
        return ll

    # 新增活动参与情况信息
    # param activity_type: string 活动类型
    # param player_code: string 运动员代码
    # param track_dt: string 参与日期
    # param eff_status: string 生效状态
    # param track_num: int 参与课时
    # param location: string 地点
    # param enroll_status: string 报名状态
    # param attend_status: string 出席状态
    # param accomp_status: string 完成状态
    # param batch_id: string 批量ID
    # return int: 新增记录条数
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
            d = self.getData(ActivityData)
            r = d.addActivityTrack(activity_type, player_code,
                                   track_dt[0:10] if track_dt != '' else None, eff_status,
                                   track_num, location, enroll_status,
                                   attend_status, accomp_status, batch_id)
            if r == 0:
                d.commit()
            else:
                d.rollback()
            return r
        except Exception as err:
            logger = logging.getLogger('fc116')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
            return -2

    def addActivityTracks(self,
                          activityTracks):
        """
        新增球员活动记录情况列表
        :param activityTracks: dict, 球员活动记录情况列表
        :return: int, 新增成功记录条数, 返回-1表示新增失败(全体回滚)
        """
        r = -1
        t = 0
        d = self.getData(ActivityData)
        if len(activityTracks) > 0:
            for e in activityTracks:
                try:
                    t = d.addActivityTrack(player_code=e['player_code'],
                                           track_dt=e['track_dt'],
                                           track_num=e['track_num'],
                                           location=e['location'],
                                           batch_id=e['batch_id'])
                    if t != 0:
                        break
                except Exception as err:
                    logger = logging.getLogger('fc116')
                    logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
                    d.rollback()
                    return -1
            if t == 0:
                try:
                    d.commit()
                except Exception as err:
                    logger = logging.getLogger('fc116')
                    logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
                    return -1
            else:
                d.rollback()
        return len(activityTracks)

    def getActivityTrackByPlayerCode(self,
                                     player_code='',
                                     eff_status='A',
                                     activity_type='C',
                                     rownum=0):
        """
        根据球员代码查询运动员活动参与情况
        :param player_code: str, 球员代码
        :param eff_status: str, 活动有效状态, 'A'-有效, 'I'-无效
        :param activity_type: str, 活动类型, '课程类'-C, '活动类'-A, '内部比赛类'-I, '外部比赛类'-M...
        :param rownum: int, 返回记录条数, 0表示全返回
        :return: list, 运动员活动参与情况列表
        """
        d = self.getData(ActivityData)
        return d.getActivityTrackByPlayerCode(player_code, eff_status,
                                              activity_type, rownum)

    def getActivityTrackByName(self,
                               name='',
                               eff_status='A',
                               activity_type='C',
                               rownum=0):
        """
        根据球员姓名查询运动员活动参与情况
        :param name: str, 球员姓名
        :param eff_status: str, 活动有效状态, 'A'-有效, 'I'-无效
        :param activity_type: str, 活动类型, '课程类'-C, '活动类'-A, '内部比赛类'-I, '外部比赛类'-M...
        :param rownum: int, 返回记录条数, 0表示全返回
        :return: list, 运动员活动参与情况列表
        """
        d = self.getData(ActivityData)
        l = self.getPlayerByName(name)
        ll = []
        for e in l:
            ll.extend(
                self.getActivityTrackByPlayerCode(e.player_code, eff_status,
                                                  activity_type, rownum))
        return ll

    # 更新活动参与情况
    # param trans_id: int 交易id
    # param player_code: string 运动员代码
    # param eff_status: string 生效状态
    # param activity_type: string 活动类型, C课程M外部赛P内部赛
    # param trans_type: string 活动交易类型, B购买T转移P赠送
    # param begin_dt: string 活动开始日期
    # param end_dt：string 活动结束日期
    # param trans_num: int 交易数量
    # param unit_price：int 价格
    # param currency： string 货币
    # param trans_dt： string 交易日期
    # param batch_id: string 批量id
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
        try:
            d = self.getData(ActivityData)
            r = d.updateActivityTrack(track_id, activity_type, player_code,
                                      track_dt, eff_status, track_num, location,
                                      enroll_status, attend_status, accomp_status,
                                      batch_id)
            if r == 0:
                d.commit()
            else:
                d.rollback()
            return r
        except Exception as err:
            logger = logging.getLogger('fc116')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
            return -2

    def truncateActivityTrack(self):
        """
        清空活动记录表
        :return: 0-删除成功, -1-删除失败, -2-提交时失败
        """
        d = self.getData(ActivityData)
        try:
            r = d.truncateActivityTrack()
            if r == 0:
                d.commit()
            else:
                d.rollback()
            return r
        except Exception as err:
            logger = logging.getLogger('fc116')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
            return -2
