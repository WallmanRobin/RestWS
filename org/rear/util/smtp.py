# coding=utf-8

"""
邮件常用的操作函数
"""

import logging
import smtplib
import sys
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import path

from org.rear.util import cfg


def packageAttachment(dir, codeset='utf-8'):
    """
    将指定文件列表中的文件装入附件
    :param dir: list, 文件列表
    :param codeset: str, 附件字符集
    :return: list, 已封装好的附件列表
    """
    al = []
    for f in dir:
        if path.isfile(f):
            n = path.basename(f)
            att = MIMEText(open(f, 'rb').read(), 'base64', codeset)
            att["Content-Type"] = 'application/octet-stream'
            # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
            att["Content-Disposition"] = 'attachment; filename=' + n
            al.append(att)
    return al

def sendMail(fr, to, subject, content,attachments, codeset='utf-8', mime='plain', fr_str='', to_str=''):
    """
    发送邮件
    :param fr: str, smtp服务器地址
    :param to: str, smtp服务器端口
    :param subject: str, 邮件标题
    :param content: str, 邮件内容
    :param attachments: list, 邮件附件列表
    :param codeset: str, 邮件字符集
    :param mime: str, 邮件内容类型，例如html或者plain
    :param fr_str: str, 发送者邮箱
    :param to_str: str, 接收者邮箱
    :return: 无返回值
    """
    scfg = cfg.smtpConf()
    mail_host = scfg['host']  #设置服务器
    mail_port = scfg['port']  #设置服务器
    mail_user = scfg['user']    #用户名
    mail_pass = scfg['password']   #口令 
    
    sender = fr
    receivers = to  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    
    message = MIMEMultipart()
    if fr_str=='':
        message['From'] = fr
    else:
        message['From'] = Header(fr_str, codeset)
    if to_str=='':
        message['To'] = to
    else:
        message['To'] = Header(to_str, codeset)
    message['Subject'] = Header(subject, codeset)
    message.attach(MIMEText(content, mime, codeset))
    for e in attachments:
        message.attach(e)

    try:
        print('sending mail:', fr, to, ' subject:', subject, ' attach length:', len(attachments))
        smtpObj = smtplib.SMTP() 
        smtpObj.connect(mail_host, int(mail_port))    # 25 为 SMTP 端口号
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print ("邮件发送成功")
    except smtplib.SMTPException as err:
        logger = logging.getLogger('rear')
        logger.error(sys.modules[__name__] + '.' + __name__ + ': ' + err)

def sendPlainMail(fr, to, subject, content, codeset='utf-8', fr_str='', to_str=''):
    """
    发送纯文字邮件
    :param fr: str, smtp服务器地址
    :param to: str, smtp服务器端口
    :param subject: str, 邮件标题
    :param content: str, 邮件内容
    :param codeset: str, 邮件字符集
    :param fr_str: str, 发送者邮箱
    :param to_str: str, 接收者邮箱
    :return: 无返回值
    """
    sendMail(fr, to, subject, content, [], codeset, 'plain', fr_str, to_str)

def sendHtmlMail(fr, to, subject, content, codeset='utf-8', fr_str='', to_str=''):
    """
    发送html邮件
    :param fr: str, smtp服务器地址
    :param to: str, smtp服务器端口
    :param subject: str, 邮件标题
    :param content: str, 邮件内容
    :param codeset: str, 邮件字符集
    :param fr_str: str, 发送者邮箱
    :param to_str: str, 接收者邮箱
    :return: 无返回值
    """
    sendMail(fr, to, subject, content, [], codeset, 'html', fr_str, to_str)

def sendPlainAttachmentMail(fr, to, subject, content, dir, codeset='utf-8', fr_str='', to_str=''):
    """
    发送带附件的纯文字邮件
    :param fr: str, smtp服务器地址
    :param to: str, smtp服务器端口
    :param subject: str, 邮件标题
    :param content: str, 邮件内容
    :param attachments: list, 邮件附件列表
    :param codeset: str, 邮件字符集
    :param fr_str: str, 发送者邮箱
    :param to_str: str, 接收者邮箱
    :return: 无返回值
    """
    al = packageAttachment(dir)
    sendMail(fr, to, subject, content,al, codeset, 'plain', fr_str, to_str)

def sendHtmlAttachmentMail(fr, to, subject, content, dir, codeset='utf-8', fr_str='', to_str=''):
    """
    发送带附件的html邮件
    :param fr: str, smtp服务器地址
    :param to: str, smtp服务器端口
    :param subject: str, 邮件标题
    :param content: str, 邮件内容
    :param attachments: list, 邮件附件列表
    :param codeset: str, 邮件字符集
    :param fr_str: str, 发送者邮箱
    :param to_str: str, 接收者邮箱
    :return: 无返回值
    """
    al = packageAttachment(dir)
    sendMail(fr, to, subject, content,al, codeset, 'html', fr_str, to_str)