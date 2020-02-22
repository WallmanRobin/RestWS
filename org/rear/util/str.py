"""
json常用的操作函数
"""

def trimPhoneNumber(s):
    """
    处理电话号码字符串中的特殊字符
    :param s: str, 待处理的电话号码字符串
    :return: 处理后的电话号码字符串
    """
    return s.replace('-', '').replace('——', '').replace('_', '').replace(
        '(', '').replace(')', '').replace('（', '').replace('）', '')