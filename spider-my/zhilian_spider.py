import datetime
import re
import urllib.request
from urllib import parse
import matplotlib.pyplot as plt


def get_zhilian_html(url):
    hearder = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    req = urllib.request.Request(url, headers=hearder)
    res = urllib.request.urlopen(req)
    return res.read().decode('utf-8')


def get_data(html, result):

    job_num = re.findall(r'<em>(\d+)</em>', html)
    result[city] = int(''.join(job_num))
    return result


def draw(keys, values, job):
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    time = i = datetime.datetime.now()
    title = str(time.year) + "-" + str(time.month) + ' ' + job + "职位数柱形图"
    plt.title(title)
    plt.bar(keys, values, label="职位数")
    plt.legend()
    plt.savefig(title + '.png')
    plt.show()


def draw_cicle(keys, values, job):
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    time = i = datetime.datetime.now()
    explode = [0.01] + [0] * (len(keys) - 1)
    title = str(time.year) + "-" + str(time.month) + ' ' + job + "职位数饼状图"
    plt.title(title)
    plt.pie(x=values, labels=keys, explode=explode, labeldistance=1.1, startangle=90,
            pctdistance=0.6, autopct='%1.2f%%')
    plt.savefig(title + '.png')
    plt.show()


if __name__ == '__main__':
    citys = ['北京', '上海', '广州', '深圳', '成都']
    job = input('请输入搜索的岗位：')
    result = {}
    for city in citys:
        search = parse.urlencode({'jl': city, 'kw': job})
        url = 'https://sou.zhaopin.com/jobs/searchresult.ashx?' + search
        html = get_zhilian_html(url)
        get_data(html, result)
    keys = list(result.keys())
    values = list(result.values())
    draw(keys, values, job)
    draw_cicle(keys, values, job)
