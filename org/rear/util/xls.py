# coding=utf-8

"""
Excel文件的常用操作函数
"""

import json
import xlwt
from os import path

from org.rear.util import cfg


def set_style(name, height, bold=False):
    """
    设置样式
    :param name: str, 字体名称
    :param height: int, 字体高度
    :param bold: boolean, 是否粗体
    :return: xlwt.XFStyle, 返回指定的样式
    """
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    return style

def writeSignInXls(signInData, planDate, user):
    """
    根据签到数据生成并写入xls文件
    :param signInData: json, 签到情况数据
    :param planDate: str, 签到日期
    :param user: str, 签到用户
    :return: tuple, 成功则返回(文件名, 文件路径)元组,失败返回('','')空字符串元组
    """
    workBook = xlwt.Workbook()
    sheet1 = workBook.add_sheet('签到情况', cell_overwrite_ok=True)

    # 写第一行
    row0 = ['时间', '运动员代码', '姓名', '英文名', '球衣号码', '课时', '第一节', '第二节']
    for i in range(0, len(row0)):
        sheet1.write(0, i, row0[i], set_style('Times New Roman', 220, True))

    # 写签到数据
    r = 1
    for p in signInData:
        if p['course1'] == 'Y' or p['course2'] == 'Y':
            sheet1.write(r, 0, p['d'], set_style('Times New Roman', 220))
            sheet1.write(r, 1, p['player_code'], set_style('Times New Roman', 220))
            sheet1.write(r, 2, p['name'], set_style('Times New Roman', 220))
            sheet1.write(r, 3, p['al_name'], set_style('Times New Roman', 220))
            sheet1.write(r, 4, p['number'], set_style('Times New Roman', 220))
            sheet1.write(r, 5, (p['course1'] == 'Y') + (p['course2'] == 'Y'), set_style('Times New Roman', 220))
            sheet1.write(r, 6, p['course1'], set_style('Times New Roman', 220))
            sheet1.write(r, 7, p['course2'], set_style('Times New Roman', 220))
            r = r + 1
    xlsDir = cfg.xlsConf()['cache']
    fn = user + '_' + planDate + '.xls'
    fd = xlsDir + fn
    workBook.save(fd)
    if path.isfile(fd):
        return fn, fd
    else:
        return '', ''

def getCachedXlsFileDir(fn):
    """
    得到缓存的xls文件路径
    :param fn: str, xls文件名
    :return: str, 缓存的xls文件路径
    """
    xlsDir = cfg.xlsConf()['cache']
    fd = xlsDir + fn
    return fd
