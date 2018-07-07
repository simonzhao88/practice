import json

from scrapy import Request
# from scrapy.spiders import Rule, CrawlSpider  # 基于Spider的更强大的类
# from scrapy.linkextractors import LinkExtractor

from weibospider.items import WeibospiderItem, UserRelationItem
import scrapy


class WeiBoSpider(scrapy.Spider):
    name = 'weibo'

    # 用户url
    start_urls = 'https://m.weibo.cn/api/container/getIndex?uid={uid}&containerid=100505{uid}'
    # fans url
    fans_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_{uid}&since_id=1'

    # 关注
    follow_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_{uid}&page={page}'
    start_user_uuid = ['1350995007', '1195354434']

    def start_requests(self):
        for uid in self.start_user_uuid:
            yield Request(url=self.start_urls.format(uid=uid), callback=self.parse_user)

    def parse_user(self, response):
        """
        获取用户信息
        :param response:
        :return:
        """

        items = WeibospiderItem()
        response = json.loads(response.text)
        user_params = {
            'id': 'id',
            'screen_name': 'screen_name',
            'profile_image_url': 'profile_image_url',
            'profile_url': 'profile_url',
            'verified_reason': 'verified_reason',
            'description': 'description',
            'followers_count': 'followers_count',
            'follow_count': 'follow_count',
            'avatar_hd': 'avatar_hd'
        }
        for k, v in user_params.items():
            items[k] = response['data']['userInfo'][v]

        yield items

        yield Request(self.follow_url.format(uid=items.get('id'), page=1),
                      callback=self.parse_follower,
                      meta={'uid': items.get('id'), 'page': 1})

    def parse_follower(self, response):
        """
        获取用户和关注者信息
        :param response:
        :return:
        """

        # 解析用户关注
        res = json.loads(response.text)
        if res['ok']:
            card_group = res.get('data').get('cards')[-1].get('card_group')
            for card_info in card_group:
                user_info = card_info.get('user')
                uid = user_info.get('id')
                yield Request(self.start_urls.format(uid=uid), callback=self.parse_user)

            uid = response.meta.get('uid')
            # 解析用户的关注人信息之间的关系
            follower_list = []
            for follower in card_group:
                follower_list.append({'id': follower['user']['id'], 'name': follower['user']['screen_name']})
            user_relation = UserRelationItem()
            user_relation['id'] = uid
            user_relation['fans'] = []
            user_relation['follower'] = follower_list

            yield user_relation
            # 获取下一页关注信息
            page = int(response.meta.get('page')) + 1
            yield Request(self.follow_url.format(uid=uid, page=page),
                          callback=self.parse_follower,
                          meta={'uid': uid, 'page': page})
