# coding=utf-8

"""
运动员数据操作类, 该类函数不会进行数据库事务提交
"""

import logging
import sys
from org.rear.util.db.data.BaseData import BaseData
from sqlalchemy import or_, text

from org.fc116.business.player.PlayerModel import Player, PlayerAvatar, PlayerOff, PlanTimeline


class PlayerData(BaseData):
    def addPlayer(self,
                  player_code='',
                  name='',
                  al_name='',
                  uniform_number='',
                  comment='',
                  birthday='',
                  status='',
                  course_count=-9999999,
                  due_dt='',
                  group='',
                  contact_phone='',
                  contact_name='',
                  d1='',
                  d2='',
                  d3='',
                  d4='',
                  d5='',
                  d6='',
                  d7='',
                  batch_id=''):
        """
        新增运动员信息
        :param player_code: str, 运动员代码
        :param name: str, 运动员姓名
        :param al_name: str, 运动员第二姓名
        :param uniform_number: str, 球衣号码
        :param comment: str, 备注
        :param birthday: str, 运动员生日, YYYY-MM-DD的格式字符串
        :param status: str, 运动员有效状态, 'A'-有效, 'I'-无效
        :param course_count: int, 剩余课程时数
        :param due_dt: str, 有效截止日
        :param group: str, 所属组别
        :param contact_phone: str, 联系人电话
        :param contact_name: str, 联系人姓名
        :param d1: str, 周一活动情况
        :param d2: str, 周二活动情况
        :param d3: str, 周三活动情况
        :param d4: str, 周四活动情况
        :param d5: str, 周五活动情况
        :param d6: str, 周六活动情况
        :param d7: str, 周日活动情况
        :param batch_id: str, 记录批号情况
        :return: int 0-新增成功，-1-新增失败
        """
        try:
            p = Player(
                player_code=player_code,
                name=name,
                al_name=al_name,
                uniform_number=uniform_number,
                comment=comment,
                birthday=birthday,
                status=status,
                course_count=course_count,
                due_dt=due_dt,
                group=group,
                contact_phone=contact_phone,
                contact_name=contact_name,
                d1 = d1,
                d2 = d2,
                d3 = d3,
                d4 = d4,
                d5 = d5,
                d6 = d6,
                d7 = d7,
                batch_id=batch_id)
            self.addRecord(p)
        except Exception as err:
            logger = logging.getLogger('fc116')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
            return -1
        return 0

    def updatePlayer(self,
                     player_code='',
                     name='',
                     al_name='',
                     uniform_number='',
                     comment='',
                     birthday='',
                     status='',
                     course_count=-999999,
                     due_dt='',
                     group='',
                     contact_phone='',
                     contact_name='',
                     batch_id=''):
        """
        更新运动员信息
        :param player_code: str, 运动员代码
        :param name: str, 运动员姓名
        :param al_name: str, 运动员第二姓名
        :param uniform_number: str, 球衣号码
        :param comment: str, 备注
        :param birthday: str, 运动员生日, YYYY-MM-DD的格式字符串
        :param status: str, 运动员有效状态, 'A'-有效, 'I'-无效
        :param course_count: int, 剩余课程时数
        :param due_dt: str, 有效截止日
        :param group: str, 所属组别
        :param contact_phone: str, 联系人电话
        :param contact_name: str, 联系人姓名
        :param d1: str, 周一活动情况
        :param d2: str, 周二活动情况
        :param d3: str, 周三活动情况
        :param d4: str, 周四活动情况
        :param d5: str, 周五活动情况
        :param d6: str, 周六活动情况
        :param d7: str, 周日活动情况
        :param batch_id: str, 记录批号情况
        :return: int 0-更新成功，-1-更新失败
        """
        try:
            p = self.session.query(Player).filter(Player.player_code == player_code)
            if name != '':
                p.update({'name': name})
            if al_name != '':
                p.update({'al_name': al_name})
            if uniform_number != '':
                p.update({'uniform_number': uniform_number})
            if comment != '':
                p.update({'comment': comment})
            if birthday is not None and birthday != '':
                p.update({'birthday': birthday})
            if status != '':
                p.update({'status': status})
            if course_count != -999999:
                p.update({'course_count': course_count})
            if due_dt is not None and due_dt != '':
                p.update({'due_dt': due_dt})
            if group != '':
                p.update({'group': group})
            if contact_phone != '':
                p.update({'contact_phone': contact_phone})
            if contact_name != '':
                p.update({'contact_name': contact_name})
            if batch_id != '':
                p.update({'batch_id': batch_id})
        except Exception as err:
            logger = logging.getLogger('fc116')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
            return -1
        return 0

    def getPlayerByPlayerCode(self, player_code):
        """
        根据运动员代码查询运动员信息
        :param player_code: str，运动员代码
        :return: List, Player列表
        """
        l = []
        try:
            qry = self.session.query(Player)
            if player_code != '':
                qry = qry.filter(Player.player_code == player_code)
            l = qry.order_by(Player.player_code).all()
        except Exception as err:
            logger = logging.getLogger('fc116')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
        return l

    def getPlayerByName(self, name):
        """
        根据运动员姓名查询运动员信息
        :param name: str，运动员姓名
        :return: list, Player列表(重名情况)
        """
        l = []
        try:
            qry = self.session.query(Player).filter(Player.name == name)
            l = qry.order_by(Player.player_code).all()
        except Exception as err:
            logger = logging.getLogger('fc116')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
        return l

    def getPlayerLikeName(self, name):
        """
        根据运动员姓名模糊查询运动员信息
        :param name: name: str，运动员姓名
        :return: list, Player列表
        """
        l = []
        try:
            qry = self.session.query(Player).filter(or_(Player.name.like('%'+name+'%'), Player.al_name.ilike('%'+name+'%')))
            l = qry.order_by(Player.player_code).all()
        except Exception as err:
            logger = logging.getLogger('fc116')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
        return l

    def getPlayerByUniformNumber(self, uniform_number):
        """
        根据运动员球衣号码查询运动员信息
        :param uniform_number: str，运动员球衣号码
        :return: list, Player列表
        """
        l = []
        try:
            qry = self.session.query(Player).filter(Player.uniform_number == uniform_number)
            l = qry.order_by(Player.player_code).all()
        except Exception as err:
            logger = logging.getLogger('fc116')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
        return l

    def getPlayerByPlan(self, d):
        """
        根据周一到周日的训练计划查询运动员
        :param d: str，d1-d7(周一至周日)
        :return: list 当日参与训练的运动员列表
        """
        l = []
        try:
            s = d + "<>''"
            qry = self.session.query(Player).filter(text(s))
            l = qry.order_by(text(d), Player.player_code).all()
        except Exception as err:
            logger = logging.getLogger('fc116')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
        return l

    def getPlayerByContactPhone(self, phone):
        """
        根据联系人电话查询运动员
        :param phone: str, 联系人电话
        :return: list 该联系人关联的运动员列表
        """
        l = []
        try:
            qry = self.session.query(Player).filter(Player.contact_phone == phone)
            l = qry.all()
        except Exception as err:
            logger = logging.getLogger('fc116')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
        return l

    def addPlayerAvatar(self, player_code, avatar):
        """
        新增运动员头像
        :param player_code: 运动员代码
        :param avatar: str, 运动员头像图片相对路径
        :return: int 0-新增成功，-1-新增失败
        """
        try:
            ur = PlayerAvatar(player_code=player_code, avatar=avatar)
            self.addRecord(ur)
        except Exception as err:
            logger = logging.getLogger('fc116')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
            return -1
        return 0

    def updateAvatarByCode(self, player_code, avatar=''):
        """
        更新运动员头像
        :param player_code: 运动员代码
        :param avatar: str, 运动员头像图片相对路径
        :return: int, 0-更新成功，-1-更新失败
        """
        try:
            u = self.session.query(PlayerAvatar).filter(PlayerAvatar.player_code == player_code)
            if avatar != '':
                u.update({'avatar': avatar})
        except Exception as err:
            logger = logging.getLogger('fc116')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
            return -1
        return 0


    def getPlayerAvatarByCode(self, player_code):
        """
        根据运动员代码获得运动员头像信息
        :param player_code: 运动员代码
        :return: PlayerAvatar, 运动员头像对象示例, 失败返回None
        """
        d = None
        try:
            qry = self.session.query(PlayerAvatar)
            qry = qry.filter(PlayerAvatar.player_code == player_code)
            d = qry.first()
        except Exception as err:
            logger = logging.getLogger('fc116')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
        return d

    def addPlayerOff(self, player_code, start_dt, end_dt, timegroup, course_count, type='', comment=''):
        """
        新增假期申请
        :param player_code: 运动员代码
        :param start_dt: date, 假期开始日
        :param end_dt: date, 假期结束日
        :param timegroup: str, 请假时间
        :param course_count: int, 请假课时
        :param type: str, 假期类型
        :param comment: str, 备注
        :return: int 0-新增成功，-1-新增失败
        """
        try:
            po = PlayerOff(player_code=player_code, start_dt=start_dt, end_dt=end_dt, timegroup=timegroup,
                           course_count=course_count, type=type, comment=comment)
            self.addRecord(po)
        except Exception as err:
            logger = logging.getLogger('fc116')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
            return -1
        return 0

    def updatePlayerOffByCode(self, player_code, start_dt='', end_dt='', timegroup='A', course_count=0, type='',
                              comment=''):
        """
        更新假期申请
        :param player_code: 运动员代码
        :param start_dt: date, 假期开始日
        :param end_dt: date, 假期结束日
        :param timegroup: str, 请假时间
        :param course_count: int, 请假课时
        :param type: str, 假期类型
        :param comment: str, 备注
        :return: int, 0-更新成功，-1-更新失败
        """
        try:
            po = self.session.query(PlayerOff).filter(PlayerOff.player_code == player_code)
            if start_dt != '':
                po.update({'start_dt': start_dt})
            if start_dt != '':
                po.update({'end_dt': end_dt})
            if start_dt != '':
                po.update({'timegroup': timegroup})
            if start_dt != '':
                po.update({'course_count': course_count})
            if start_dt != '':
                po.update({'type': type})
            if start_dt != '':
                po.update({'comment': comment})
        except Exception as err:
            logger = logging.getLogger('fc116')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
            return -1
        return 0

    def getPlayerOffByCode(self, player_code, rownum=0):
        """
        根据运动员代码获得假期申请信息
        :param player_code: 运动员代码
        :return: List, 假期申请列表, 失败返回空列表
        """
        l = []
        try:
            qry = self.session.query(PlayerOff)
            qry = qry.filter(PlayerOff.player_code == player_code)
            if rownum > 0:
                qry = qry.limit(rownum)
            l = qry.all()
        except Exception as err:
            logger = logging.getLogger('fc116')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
        return l

    def addPlanTimeline(self, timegroup, descr="", timeline="", before="", eff_status="A"):
        """
        新增请假时间规则
        :param timegroup: str, 请假时间
        :param descr: str, 时间描述信息（上午、中午、下午）
        :param timeline: str, 上课时间
        :param before: int, 提前请假时间
        :return: int 0-新增成功，-1-新增失败
        """
        try:
            tl = PlanTimeline(timegroup=timegroup, descr=descr, timeline=timeline, before=before, eff_status=eff_status)
            self.addRecord(tl)
        except Exception as err:
            logger = logging.getLogger('fc116')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
            return -1
        return 0

    def updatePlanTimeLine(self, timegroup, descr="", timeline="", before="", eff_status="Y"):
        """
        更新请假时间规则
        :param timegroup: str, 请假时间
        :param descr: str, 时间描述信息（上午、中午、下午）
        :param timeline: str, 上课时间
        :param before: int, 提前请假时间
        :return: int 0-更新成功，-1-新增失败
        """
        try:
            tl = self.session.query(PlanTimeline).filter(PlanTimeline.timegroup == timegroup)
            if descr != '':
                tl.update({'descr': descr})
            if timeline != '':
                tl.update({'timeline': timeline})
            if before != '':
                tl.update({'before': before})
            if eff_status != '':
                tl.update({'eff_status': eff_status})
        except Exception as err:
            logger = logging.getLogger('fc116')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
            return -1
        return 0

    def getPlanTimeLine(self, timegroup="", eff_status=""):
        """
        查询请假时间规则
        :param player_code: 运动员代码
        :return: List, 请假时间规则列表, 失败返回空列表
        """
        l = []
        try:
            qry = self.session.query(PlanTimeline)
            if timegroup != "":
                qry = qry.filter(PlanTimeline.timegroup == timegroup)
            if eff_status != "":
                qry = qry.filter(PlanTimeline.eff_status == eff_status)
            l = qry.all()
        except Exception as err:
            logger = logging.getLogger('fc116')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
        return l

    def truncatePlayer(self):
        """
        清空运动员记录表
        :return: 0-删除成功, -1-删除失败
        """
        try:
            self.session.query(Player).delete()
        except Exception as err:
            logger = logging.getLogger('fc116')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
            r = -1
        return 0

    def truncatePlanTimeline(self):
        """
        清空运动员记录表
        :return: 0-删除成功, -1-删除失败
        """
        try:
            self.session.query(PlanTimeline).delete()
        except Exception as err:
            logger = logging.getLogger('fc116')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
            r = -1
        return 0
