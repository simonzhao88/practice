"""
author: simon
date: 2018-06-27
功能：利用豆瓣电影api获取电影数据并存入数据库
"""
import threading
import pymysql
import requests

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}


def get_movies_tag(url):
    """
    获取标签数据
    :param url:
    :return:
    """
    res = requests.get(url, headers=header)
    # print(res.json())
    tag_list = res.json()['tags']
    return tag_list


def get_movies_data(url, params_list, tag):
    """
    获取电影数据
    :param url:
    :param params_list:
    :param tag:
    :return:
    """
    res = requests.get(url, headers=header)
    # print(res.json())
    movies_datas = res.json()['subjects']
    for movies_data in movies_datas:
        rate = movies_data['rate']
        cover_x = movies_data['cover_x']
        title = movies_data['title']
        url = movies_data['url']
        playable = movies_data['playable']
        cover = movies_data['cover']
        movie_id = movies_data['id']
        cover_y = movies_data['cover_y']
        is_new = movies_data['is_new']
        params_list.append([rate, cover_x, title, url, playable,
                            cover, movie_id, cover_y, is_new, tag])
    return params_list


def conn_mysql(sql, params_list):
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


def save_data(params_list):
    """
    保存数据到数据库
    :param params_list:
    :return:
    """
    sql = 'insert into douban_movies (rate, cover_x, title, url, playable, cover, id, cover_y, is_new, tag) ' \
          'values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    conn_mysql(sql, params_list)


class GetMovies(threading.Thread):
    def __init__(self, func):
        super(GetMovies, self).__init__()
        self.func = func

    def run(self):
        return self.func


if __name__ == '__main__':
    tag_url = 'https://movie.douban.com/j/search_tags?type=movie&source='
    tags = get_movies_tag(tag_url)
    params_list = []
    tag_lock = threading.Lock()
    page = input('输入要爬取的页数：')
    # for tag in tags:
    #     movies_url = 'https://movie.douban.com/j/search_subjects?type=movie' \
    #                  '&tag=' + tag + '&sort=recommend&page_limit=20&page_start=0'
    #     params = get_movies_data(movies_url, params_list, tag)
    # print(params)
    while True:
        if tag_lock.acquire() and tags:

            tag = tags.pop()
            movies_url = 'https://movie.douban.com/j/search_subjects?type=movie' \
                         '&tag=' + tag + '&sort=recommend&page_limit=' + page*20 + '&page_start=0'
            get_movies = GetMovies(get_movies_data(movies_url, params_list, tag))

            get_movies.start()
            get_movies.join()
            tag_lock.release()
        else:
            break

    save_data(params_list)
    print('爬取完成~~')
