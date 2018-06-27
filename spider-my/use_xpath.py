import re
import urllib.request
from lxml import etree
import pymysql as pymysql


def get_html(url):
    """
    获取网页源码
    :param url:
    :return:
    """
    headers = {
        'User - Agent': 'Mozilla / 5.0(Windows NT 6.1;Win64;x64) AppleWebKit / '
                        '537.36(KHTML, likeGecko) Chrome / 63.0.3239.132Safari / 537.36',
        'referer': url
    }
    req = urllib.request.Request(url, headers=headers)
    rep = urllib.request.urlopen(req)
    html = rep.read()
    page_html = decode_html(html)
    return page_html


def decode_html(html):
    """
    解码
    :param html:
    :return:
    """
    for i in ['GBK', 'utf-8']:
        try:
            page_html = html.decode(i)
            break
        except Exception as e:
            pass
    return page_html


def pattern_regex(html, pattern, flags=re.S):
    """
    封装的正则匹配函数
    :param html:
    :param pattern:
    :param flags:
    :return:
    """
    html_regex = re.compile(pattern, flags)
    return html_regex.findall(html)


def get_links(html):
    html = etree.HTML(html)
    links = html.xpath('/html/body/div[1]/div[4]/div[1]/div[1]/ul/li/a/@href')
    return links


def save(sql, params_list):
    """
    mysqlhandler连接数据库
    :param sql:
    :param params_list:
    :return:
    """
    conn = pymysql.connect(host='localhost', port=3306, user='root',
                           password='root', database='spider', charset='utf8')
    cursor = conn.cursor()
    cursor.executemany(sql, params_list)
    conn.commit()
    cursor.close()


def start_crawl(url):
    """
    爬虫主函数，获取数据，保存数据
    :param url:
    :return:
    """
    page_html = get_html(url)
    link_list = get_links(page_html)
    params_list = []
    for link_url in link_list:
        try:
            detail_html = get_html(link_url)
        except:
            pass
        detail_html = etree.HTML(detail_html)
        # 标题
        title = detail_html.xpath('//*[@id="article-container"]/div[2]/div[1]/div[1]/h1/text()')
        # 内容
        content = detail_html.xpath('//*[@id="mp-editor"]/p/text()')
        # print(content)
        # 将标题和内容放入列表中
        params_list.append([title[0], ''.join(content)])
        print(params_list)
    sql = 'insert into result_souhu values (%s, %s)'
    save(sql, params_list)


if __name__ == '__main__':
    url = 'https://sports.sohu.com/nba_a.shtml'
    start_crawl(url)
