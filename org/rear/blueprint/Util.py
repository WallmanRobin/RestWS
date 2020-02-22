# coding=utf-8

from flask import Blueprint, send_file, abort, request

from org.rear.util import img
from org.rear.util.app import packageResponse, packageDate, packageTimeStamp

util_bp = Blueprint('Util', __name__)

@util_bp.route('/cartoonPortraits', methods=['GET'])
def listCartoonPortraits():
    """
    向客户端返回所有卡通头像的绝对路径
    :return: json, {'data': []}
    """
    l = img.loadCartoonPortraits()
    return packageResponse({'data': l})
