import re

from lxml import etree

import requests

from bs4 import BeautifulSoup


def start_crawl(url):
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 6.1;Win64;x64) AppleWebKit / '
                      '537.36(KHTML, likeGecko) Chrome / 63.0.3239.132Safari / 537.36'
    }
    res = requests.get(url, headers=headers)
    # parse_by_etree(res.text)
    parse_by_bs4(res.text)


def parse_by_etree(html):
    html = etree.HTML(html)
    title = html.xpath('//*[@id="js-explore-tab"]/div[1]/div/div/h2/a/text()')
    a_href = html.xpath('//*[@id="js-explore-tab"]/div[1]/div/div/h2/a/@href')
    print(title, a_href)


def parse_by_bs4(html):
    soup = BeautifulSoup(html, 'lxml')
    result = soup.find_all('a', 'question_link')
    for i in result:
        href_link = 'https://www.zhihu.com' + i.attrs.get('href')
        title = i.text
        print(href_link, title)


if __name__ == '__main__':
    url = 'https://www.zhihu.com/explore'
    start_crawl(url)
