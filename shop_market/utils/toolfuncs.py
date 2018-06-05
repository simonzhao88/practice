import random


def get_ticket():
    """
    生成随机ticket
    :return:
    """
    s = 'abcdefghijklmnopqrstuvwxyz1234567890_*='
    ticket = ''
    for i in range(28):
        ticket += random.choice(s)
    return 'TK_' + ticket
