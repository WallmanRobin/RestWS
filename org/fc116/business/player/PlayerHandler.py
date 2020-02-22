# coding=utf-8

"""
运动员业务处理类, 该类函数负责进行数据库事务提交
"""
import logging
import sys
from datetime import datetime, timedelta
from org.rear.util.db.handler.BaseHandler import BaseHandler

from org.fc116.business.activity.ActivityHandler import ActivityHandler
from org.fc116.business.player.PlayerData import PlayerData
from org.rear.util.str import trimPhoneNumber


class PlayerHandler(BaseHandler):
    def getPlayerByName(self, name):
        """
        根据运动员姓名查询运动员信息
        :param name: str，运动员姓名
        :return: list, Player对象实例列表(重名情况)
        """
        d = self.getData(PlayerData)
        return d.getPlayerByName(name)

    def getPlayerLikeName(self, name):
        """
        根据运动员姓名模糊查询运动员信息
        :param name: name: str，运动员姓名
        :return: list, Player对象实例列表
        """
        d = self.getData(PlayerData)
        return d.getPlayerLikeName(name)

    def getPlayerByPlan(self, day):
        """
        根据周一到周日的训练计划查询运动员
        :param d: str，d1-d7(周一至周日)
        :return: list 当日参与训练的运动员列表
        """
        da = ['d1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7']
        d = self.getData(PlayerData)
        return d.getPlayerByPlan(da[day])

    def getPlayerByNameOrUniformNumber(self, code):
        """
        根据运动员姓名或球衣号码查询运动员信息
        :param code: str，运动员姓名或者球衣号码
        :return: list, Player对象实例列表
        """
        d = self.getData(PlayerData)
        l = d.getPlayerByUniformNumber(code)
        if len(l) == 0:
            l = d.getPlayerLikeName(code)
        return l

    def getPlayerByContactPhone(self, phone):
        """
        根据联系人电话查询运动员
        :param phone: str, 联系人电话
        :return: list 该联系人关联的运动员列表
        """
        d = self.getData(PlayerData)
        return d.getPlayerByContactPhone(phone)

    def extractPlanData(self, s):
        t = s[0]
        d = self.getData(PlayerData)
        l = d.getPlanTimeLine(t, 'A')
        if len(l) > 0:
            return l[0]
        return None

    def getPlayerCourseCountOfContact(self, phone):
        """
        根据联系人电话查询运动员剩余课程时数和活动情况
        :param phone: 联系人电话
        :return: list, 运动员剩余课程时数和活动情况列表
        """
        d = self.getData(PlayerData)
        pl = []
        if trimPhoneNumber(phone).isdigit():
            pl = self.getPlayerByContactPhone(phone)
        l = []
        ah = ActivityHandler()
        for p in pl:
            tr = ah.getActivityTrackByPlayerCode(player_code=p.player_code,
                                                 rownum=4)
            lt = []
            for t in tr:
                rt = {
                    'track_dt': datetime.strftime(t.track_dt, "%Y-%m-%d"),
                    'track_num': t.track_num,
                    'location': t.location
                }
                lt.append(rt)
            lp = []
            if p.d1 != '':
                tg = self.extractPlanData(p.d1)
                pt = {'plan_dt': '周一', 'timegroup': tg.timegroup, 'plan_descr': tg.descr}
                lp.append(pt)
            if p.d2 != '':
                tg = self.extractPlanData(p.d2)
                pt = {'plan_dt': '周二', 'timegroup': tg.timegroup, 'plan_descr': tg.descr}
                lp.append(pt)
            if p.d3 != '':
                tg = self.extractPlanData(p.d3)
                pt = {'plan_dt': '周三', 'timegroup': tg.timegroup, 'plan_descr': tg.descr}
                lp.append(pt)
            if p.d4 != '':
                tg = self.extractPlanData(p.d4)
                pt = {'plan_dt': '周四', 'timegroup': tg.timegroup, 'plan_descr': tg.descr}
                lp.append(pt)
            if p.d5 != '':
                tg = self.extractPlanData(p.d5)
                pt = {'plan_dt': '周五', 'timegroup': tg.timegroup, 'plan_descr': tg.descr}
                lp.append(pt)
            if p.d6 != '':
                tg = self.extractPlanData(p.d6)
                pt = {'plan_dt': '周六', 'timegroup': tg.timegroup, 'plan_descr': tg.descr}
                lp.append(pt)
            if p.d7 != '':
                tg = self.extractPlanData(p.d7)
                pt = {'plan_dt': '周日', 'timegroup': tg.timegroup, 'plan_descr': tg.descr}
                lp.append(pt)
            lo = []
            to = self.getPlayerOffByCode(p.player_code)
            for t in to:
                lptl = d.getPlanTimeLine(timegroup=t.timegroup)
                plan_descr = ""
                if len(lptl) > 0:
                    plan_descr = lptl[0].descr
                ro = {'start_dt': datetime.strftime(t.start_dt, "%Y-%m-%d"),
                      'end_dt': datetime.strftime(t.end_dt, "%Y-%m-%d"), 'timegroup': t.timegroup,
                      'plan_descr': plan_descr,
                      'course_count': t.course_count, 'comment': t.comment}
                lo.append(ro)
            rp = {
                'player_code': p.player_code,
                'name': p.name,
                'RCC': p.course_count,
                'due_dt': datetime.strftime(p.due_dt, "%Y-%m-%d"),
                'comment': p.comment,
                'track': lt,
                'plan': lp,
                'off': lo
            }
            l.append(rp)
        return l

    def addPlayer(self,
                  player_code='',
                  name='',
                  al_name='',
                  uniform_number='',
                  comment='',
                  birthday='',
                  status='A',
                  course_count=0,
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
        :return: int 0-新增成功，-1-新增失败, -2-提交失败
        """
        try:
            d = self.getData(PlayerData)
            r = d.addPlayer(player_code, name, al_name, uniform_number, comment,
                            birthday[0:10] if birthday != '' else None, status,
                            course_count, due_dt[0:10] if due_dt != '' else None, group,
                            contact_phone, contact_name, d1, d2, d3, d4, d5, d6,
                            d7, batch_id)
            if r == 0:
                d.commit()
            else:
                d.rollback()
            return r
        except Exception as err:
            logger = logging.getLogger('fc116')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
            return -2

    def addPlayers(self,
                   playerList):
        """
        更新运动员列表
        :param playerList: 运动员列表
        :return: int, 成功则返回更新的运动员数量,失败返回-1并全体回滚
        """
        r = 0
        d = self.getData(PlayerData)
        if len(playerList) > 0:
            for e in playerList:
                if e['player_code'] == 'FC00005':
                    pass
                r = d.addPlayer(e['player_code'], e['name'], e['al_name'], e['uniform_number'], e['comment'],
                                e['birthday'][0:10] if e['birthday'] != '' else None, e['status'],
                                e['course_count'], e['due_dt'][0:10] if e['due_dt'] != '' else None, e['group'],
                                e['contact_phone'], e['contact_name'], e['d1'], e['d2'], e['d3'], e['d4'], e['d5'],
                                e['d6'],
                                e['d7'], e['batch_id'])
                if r != 0:
                    break
            if r == 0:
                try:
                    d.commit()
                except Exception as err:
                    logger = logging.getLogger('fc116')
                    logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
                    return -1
            else:
                d.rollback()
                return -1
        return len(playerList)

    def updatePlayer(self,
                     player_code='',
                     name='',
                     al_name='',
                     uniform_number='',
                     comment='',
                     birthday='',
                     status='A',
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
        :return: int 0-更新成功，-1-更新失败, -2-提交失败
        """
        try:
            d = self.getData(PlayerData)
            r = d.updatePlayer(player_code, name, al_name,
                               uniform_number, comment,
                               birthday[0:10] if birthday != '' else None, status,
                               course_count, due_dt if due_dt != '' else None,
                               group, contact_phone, contact_name, batch_id)
            if r == 0:
                d.commit()
            return r
        except Exception as err:
            logger = logging.getLogger('fc116')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
            return -2

    # 清空运动员表
    def truncatePlayer(self):
        """
        清空运动员表数据
        :return: int 0-删除成功，-1-删除失败
        """
        try:
            d = self.getData(PlayerData)
            d.truncatePlayer()
            d.commit()
            return 0
        except Exception as err:
            logger = logging.getLogger('fc116')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
            return -2

    def addPlayerOff(self, player_code, start_dt, end_dt, timegroup, course_count=0, type='', comment=''):
        """
        新增假期申请
        :param player_code: 运动员代码
        :param start_dt: date, 假期开始日
        :param end_dt: date, 假期结束日
        :param timegroup: str, 请假时间
        :param course_count: int, 请假课时
        :param type: str, 假期类型
        :param comment: str, 备注
        :return: int 0-新增成功，-1-新增失败, -2-提交失败
        """
        try:
            d = self.getData(PlayerData)
            r = d.addPlayerOff(player_code, start_dt, end_dt, timegroup, course_count, type, comment)
            if r == 0:
                d.commit()
            else:
                d.rollback()
            return r
        except Exception as err:
            logger = logging.getLogger('fc116')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
            return -2

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
        :return: int 0-更新成功，-1-更新失败, -2-提交失败
        """
        try:
            d = self.getData(PlayerData)
            r = d.updatePlayerOffByCode(player_code, start_dt, end_dt, timegroup, course_count, type, comment)
            if r == 0:
                d.commit()
            return r
        except Exception as err:
            logger = logging.getLogger('fc116')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
            return -2

    def getPlayerOffByCode(self, palyer_code):
        """
        根据运动员代码查询运动员请假信息
        :param player_code: str，运动员代码
        :return: list, PlayerOff列表
        """
        d = self.getData(PlayerData)
        return d.getPlayerOffByCode(palyer_code, rownum=4)

    def validateApplyOff(self, apply_dt, start_dt, timegroup):
        d = self.getData(PlayerData)
        l = d.getPlanTimeLine(timegroup=timegroup)
        if len(l) > 0:
            tl = l[0]
            s = start_dt + " " + tl.timeline
            dt = datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
            dt = dt - timedelta(hours=tl.before)
            now = apply_dt
            print (dt, now)
            return dt > now
        else:
            return False

    def getPlanTimeLineData(self, timegroup="", eff_status=""):
        """
        查询请假时间规则
        :param player_code: 运动员代码
        :return: List, 请假时间规则列表, 失败返回空列表
        """
        d = self.getData(PlayerData)
        l = d.getPlanTimeLine(timegroup, eff_status)
        lo = []
        for e in l:
            lo.append({'timegroup': e.timegroup, 'descr': e.descr, 'timeline': e.timeline, 'before': e.before,
                       'eff_status': e.eff_status})
        return lo

    def addPlanTimelineData(self, l):
        """
        新增请假时间规则
        :param timegroup: str, 请假时间
        :param descr: str, 时间描述信息（上午、中午、下午）
        :param timeline: str, 上课时间
        :param before: int, 提前请假时间
        :return: int 0-新增成功，-1-新增失败, -2-提交失败
        """
        try:
            d = self.getData(PlayerData)
            d.truncatePlanTimeline()
            for e in l:
                r = d.addPlanTimeline(e['timegroup'], e['descr'], e['timeline'], e['before'], e['eff_status'])
                if r != 0:
                    break
            if r == 0:
                d.commit()
            else:
                d.rollback()
            return r
        except Exception as err:
            logger = logging.getLogger('fc116')
            logger.error(self.__class__.__name__ + '.' + sys._getframe().f_code.co_name + ': ' + str(err))
            return -2


if __name__ == "__main__":
    h = PlayerHandler()
    print(h.addPlayerOff('FC00343', '2020-02-13', '2020-02-13', 'A', 1))
