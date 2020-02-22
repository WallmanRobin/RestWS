# coding=utf-8

import json
from datetime import datetime
from flask import Blueprint, send_file, abort, request

from org.fc116.business.activity.ActivityHandler import ActivityHandler
from org.fc116.business.player.PlayerHandler import PlayerHandler
from org.rear.authorization.rbac.User.UserHandler import UserHandler
from org.rear.util import xls, weixin
from org.rear.util.app import packageResponse, packageDate, packageTimeStamp

weixin_bp = Blueprint('Weixin', __name__)

@weixin_bp.route('/getPlayerCourseCountByContactPhone/<string:phone>',
           methods=['GET'])
def getPlayerCourseCountByContactPhone(phone):
    """
    根据联系人电话向客户端返回关联的运动员课时和训练计划信息
    :param phone: str, 联系人电话
    :return: json {'CourseCount':[{'player_code':str,'name':str,'RCC':int,'due_dt':str,'comment':str,'track':[],'plan':[]}]}
    """
    h = PlayerHandler()
    l = h.getPlayerCourseCountOfContact(phone)
    if len(l) == 0:
        abort(404)
    return packageResponse({'CourseCount': l})

@weixin_bp.route('/addPlayer', methods=['POST'])
def addPlayer():
    """
    新增运动员信息
    :return: json, {'add': i}, i为0表示新增成功, 其他值表示新增失败
    """
    player_code = request.form.get("player_code")
    name = request.form.get("name")
    al_name = request.form.get("al_name")
    uniform_number = request.form.get("uniform_number")
    comment = request.form.get("comment")
    birthday = request.form.get("birthday")
    status = request.form.get("status")
    course_count = request.form.get("course_count")
    due_dt = request.form.get("due_dt")
    group = request.form.get("group")
    contact_phone = request.form.get("contact_phone")
    contact_name = request.form.get("contact_name")
    d1 = request.form.get("d1")
    d2 = request.form.get("d2")
    d3 = request.form.get("d3")
    d4 = request.form.get("d4")
    d5 = request.form.get("d5")
    d6 = request.form.get("d6")
    d7 = request.form.get("d7")
    batch_id = request.form.get("batch_id")
    h = PlayerHandler()
    i = h.addPlayer(player_code, name, al_name, uniform_number, comment,
                    birthday, status, course_count, due_dt, group,
                    contact_phone, contact_name, d1, d2, d3, d4, d5, d6, d7,
                    batch_id)
    return packageResponse({'add': i})

@weixin_bp.route('/addPlayers', methods=['POST'])
def addPlayers():
    """
    批量新增运动员信息
    :return: json, {'add': r}, r表示新增成功记录数, 其他值表示新增失败(全体回滚)
    """
    str = request.get_data()
    str = str.decode('utf8')
    str.replace('\\n',' ')
    playerList = json.loads(str)
    if playerList and len(playerList) > 0:
        h = PlayerHandler()
        r = h.addPlayers(playerList)
        return packageResponse({'add': r})
    return packageResponse({'add': 0})

def packagePlan(e, d):
    """
    将运动员实例封装为计划json
    :param e: 运动员信息
    :param d: 训练计划时间
    :return: json, 计划json
    """
    return {
        'player_code': e.player_code,
        'name': e.name,
        'al_name': e.al_name,
        'number': e.uniform_number,
        'course1': '',
        'course2': '',
        'd': d
    }

#Player对象封装成字典
def packagePlayer(e):
    return {
        'player_code': e.player_code,
        'name': e.name,
        'al_name': e.al_name,
        'uniform_number': e.uniform_number,
        'comment': e.comment,
        'birthday': packageDate(e.birthday),
        'status': e.status,
        'course_count': e.course_count,
        'due_dt': packageDate(e.due_dt),
        'group': e.group,
        'contact_phone': e.contact_phone,
        'contact_name': e.contact_name,
        'd1': e.d1,
        'd2': e.d2,
        'd3': e.d3,
        'd4': e.d4,
        'd5': e.d5,
        'd6': e.d6,
        'd7': e.d7,
        'batch_id': e.batch_id
    }

@weixin_bp.route('/getPlayerByName/<string:name>', methods=['GET'])
def getPlayerByName(name):
    """
    根据姓名向客户端返回运动员信息列表
    :param name: 运动员姓名
    :return: json, {'list':[]}
    """
    l = []
    h = PlayerHandler()
    ll = h.getPlayerByName(name)
    for e in ll:
        p = packagePlayer(e)
        l.append(p)
    return packageResponse({'list': l})

@weixin_bp.route('/getPlayerByNameOrUniformNumber/<string:code>', methods=['GET'])
def getPlayerByNameOrUniformNumber(code):
    """
    根据联系人电话向客户端返回关联的运动员课时和训练计划信息
    :param phone: str, 联系人电话
    :return: json {'CourseCount':[{'player_code':str,'name':str,'RCC':int,'due_dt':str,'comment':str,'track':[],'plan':[]}]}
    """
    l = []
    h = PlayerHandler()
    ll = h.getPlayerByNameOrUniformNumber(code)
    for e in ll:
        p = packagePlayer(e)
        l.append(p)
    return packageResponse({'list': l})

#param day: int 周几（0-6，周日-周六）
# webservice 根据姓名查询运动员
#返回json数据结构: {'list':[{ player_code: 'xxx', name: 'xxx', number: 'xxx', course1: 'Y', course2: 'N', d: '周一' }]}
@weixin_bp.route('/getPlayerByPlan/<int:day>', methods=['GET'])
def getPlayerByPlan(day):
    """
    根据训练时间返回运动员信息列表
    :param day: int 周几(0-6, 周日-周六)
    :return: json, {'list':[]}
    """
    da = ['d1','d2','d3','d4','d5','d6','d7']
    l = []
    h = PlayerHandler()
    ll = h.getPlayerByPlan(day)
    for e in ll:
        p = packagePlan(e, getattr(e, da[day]))
        l.append(p)
    return packageResponse({'list': l})

@weixin_bp.route('/updatePlayerByPlayerCode', methods=['POST'])
def updatePlayerByPlayerCode():
    """
    更新运动员信息
    :return: json, {'set': i}, i为0表示更新成功
    """
    player_code = request.form.get("player_code")
    name = request.form.get("name")
    al_name = request.form.get("al_name")
    uniform_number = request.form.get("uniform_number")
    comment = request.form.get("comment")
    birthday = request.form.get("birthday")
    status = request.form.get("status")
    course_count = request.form.get("course_count")
    due_dt = request.form.get("due_dt")
    group = request.form.get("group")
    contact_phone = request.form.get("contact_phone")
    contact_name = request.form.get("contact_name")
    batch_id = request.form.get("batch_id")
    h = PlayerHandler()
    i = h.updatePlayer(player_code, name, al_name, uniform_number,
                                   comment, birthday, status, course_count,
                                   due_dt, group, contact_phone, contact_name,
                                   batch_id)
    return packageResponse({'set': i})

@weixin_bp.route('/submitSignInData', methods=['POST'])
def submitSignInData():
    """
    提交球员训练计划信息, 并在服务器缓存生成xls文件
    :return: json,{'submit': 生成的xls文件名}
    """
    json_str = request.form.get("signInData")
    signInData = json.loads(json_str)
    planDate = request.form.get("planDate")
    user = request.form.get("user")
    fn, fd = xls.writeSignInXls(signInData, planDate, user)
    if fd!='':
        #smtp.sendSignInMail(fd, user, planDate)
        return packageResponse({'submit': fn})
    abort(404)

@weixin_bp.route('/authSignInUser/<string:code>/<string:pwd>', methods=['GET'])
def authSignInUser(code, pwd):
    """
    根据用户代码和密码校验用户
    :param code: 用户代码
    :param pwd: 用户密码
    :return: {'authenticated': i}, i为1表示成功, 为0表示失败
    """
    h = UserHandler()
    l = h.authenticateUser(code, pwd, 'B')
    if(len(l)>0):
        return packageResponse({'authenticated':'1'})
    else:
        l = h.authenticateUser(code, pwd, 'A')
        if(len(l)>0):
            return packageResponse({'authenticated':'1'})
    return packageResponse({'authenticated':'0'})

@weixin_bp.route('/truncatePlayer', methods=['POST','DELETE'])
def truncatePlayer():
    """
    清空运动员表信息
    :return: json, {'truncate': 1}
    """
    h = PlayerHandler()
    h.truncatePlayer()
    return packageResponse({'truncate': 1})

@weixin_bp.route('/truncateActivityTrack', methods=['POST','DELETE'])
def truncateActivityTrack():
    """
    清空运动员活动记录表信息
    :return: json, {'truncate': 1}
    """
    h = ActivityHandler()
    h.truncateActivityTrack()
    return packageResponse({'truncate': 1})

@weixin_bp.route('/addActivityTrack', methods=['POST'])
def addActivityTrack():
    """
    新增运动员活动记录信息
    :return: {'add':i}, i为0时表示新增成功, 其余值表示失败
    """
    player_code = request.form.get("player_code")
    track_dt = request.form.get("track_dt")
    track_num = request.form.get("track_num")
    location = request.form.get("location")
    batch_id = request.form.get("batch_id")
    h = ActivityHandler()
    i = h.addActivityTrack(player_code=player_code,
                           track_dt=track_dt,
                           track_num=track_num,
                           location=location,
                           batch_id=batch_id)
    return packageResponse({'add': i})


@weixin_bp.route('/addActivityTracks', methods=['POST'])
def addActivityTracks():
    """
    批量新增运动员活动记录信息
    :return: {'add':r}, r为更新成功记录条数, -1表示失败
    """
    str = request.get_data()
    str = str.decode('utf8')
    str.replace('\\n', ' ')
    activityTracks = json.loads(str)
    if activityTracks and len(activityTracks) > 0:
        h = ActivityHandler()
        r = h.addActivityTracks(activityTracks)
        return packageResponse({'add': r})
    return packageResponse({'add': 0})

@weixin_bp.route('/downloadCachedXls/<string:fn>', methods=['GET'])
def downloadCahchedXls(fn):
    """
    下载缓存的xls文件
    :param fn: 文件名
    :return: 文件的二进制数据流
    """
    fd = xls.getCachedXlsFileDir(fn)
    return send_file(fd)


@weixin_bp.route('/getOpenid/<string:code>', methods=['GET'])
def getOpenid(code):
    """
    根据获得用户的OpenId,Session_key和UnionId(open.weixin.qq.com中注册为开发者且认证才能获得UnionId)
    :param code: code
    :return: {"openid":"OPENID"}
    """
    s = weixin.getOpenid(code)
    if s == '':
        abort(404)
    return packageResponse({'openid': s})


@weixin_bp.route('/addPlayerOff', methods=['POST'])
def addPlayerOff():
    """
    新增运动员请假记录
    :return: {'add':i}, i为0时表示新增成功, 其余值表示失败
    """
    player_code = request.form.get("player_code")
    start_dt = request.form.get("start_dt")
    end_dt = request.form.get("end_dt")
    timegroup = request.form.get("timegroup")
    comment = request.form.get("comment")
    h = PlayerHandler()
    i = 0
    if h.validateApplyOff(datetime.now(), start_dt, timegroup):
        i = h.addPlayerOff(player_code,
                           start_dt,
                           end_dt,
                           timegroup,
                           comment=comment)
    else:
        i = -3
    return packageResponse({'add': i})


@weixin_bp.route('/listPlanTimeline', methods=['GET'])
def listPlanTimeLine():
    """
    查询请假时间规则配置信息
    :return: {"data":"[{'timegroup':'xxx','descr':'xxx','timeline':'00:00:00','before':3,'eff_status':'A'}]"}
    """
    h = PlayerHandler()
    l = h.getPlanTimeLineData()
    return packageResponse({'data': l})


@weixin_bp.route('/addPlanTimelineData', methods=['POST'])
def addPlanTimelineData():
    """
    新增请假规则配置
    :return: {'add':i}, i为0时表示新增成功, 其余值表示失败
    """
    json_str = request.form.get("planTimelineData")
    planTimelineData = json.loads(json_str)
    h = PlayerHandler()
    r = h.addPlanTimelineData(planTimelineData)
    return packageResponse({'add': r})
