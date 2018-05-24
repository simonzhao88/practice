"""
author: Simonzhao
time: 18-05-24
Features: 通过四川省交通管理网制作简单车辆违规查询功能
"""
import time

import requests

s = requests.Session()


def v_code(yzm_url):
    """
    获取验证码
    :param yzm_url: 验证码url
    :return:
    """
    res1 = s.get(yzm_url).content
    with open('yzm.jpg', 'wb') as f:
        f.write(res1)


def accept_data():
    """
    交互获取查询数据
    :return: 数据
    """
    hpzl_dict = {
            "大型汽车": "01", "小型汽车": "02", "使馆汽车": "03", "领馆汽车": "04", "境外汽车": "05",
            "普通摩托车": "07", "大型新能源汽车": "51", "小型新能源汽车": "27"
        }
    yzm = input('请输入验证码：')
    hpzl = hpzl_dict[input('请输入车辆类型：')]
    chepai = input('请输入车牌号：')
    haoma = chepai[1:]
    fdjh = input('请输入发动机号：')
    data = {
        'hpzl': hpzl,
        'hphm1b': haoma,
        'hphm': chepai,
        'fdjh': fdjh,
        'captcha': yzm,
        'qm': 'wf',
        'page': '1'
    }
    return data


def inquire(url, header, data):
    """
    查询
    :param url: 查询url
    :param header: 请求头
    :param data: 行驶证数据
    :return: 查询结果
    """
    res = s.post(url, header, data)
    print(res.text)


def main():
    """
    主函数
    :return:
    """
    yzm_url = 'https://sc.122.gov.cn/captcha?nocache=' + str(int(time.time()))
    url = 'https://sc.122.gov.cn/m/publicquery/vio'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/63.0.3239.132 Safari/537.36',
        'Referer': 'https://sc.122.gov.cn/views/inquiry.html?q=j',
        'Host': 'sc.122.gov.cn'
    }
    v_code(yzm_url)
    data = accept_data()
    inquire(url, header, data)


if __name__ == '__main__':
    main()
