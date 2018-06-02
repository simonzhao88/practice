"""
功能：继承rest_framework的JSONRender，自定义返回数据的json内容
author：simon
"""
from rest_framework.renderers import JSONRenderer


class CustomJsonRenderer(JSONRenderer):
    """
    自定义rest_framework返回json格式数据
    返回结果的构造
    {
        'data':{results},
        'code': 200,
        'msg': '请求成功'
    }
    """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context:

            if isinstance(data, dict):
                code = data.pop('code', 0)
                msg = data.pop('msg', '请求成功')
            else:
                code = 0
                msg = '请求成功'

            res = {
                'code': code,
                'msg': msg,
                'data': data
            }
            return super().render(res, accepted_media_type, renderer_context)
        else:
            return super().render(data, accepted_media_type, renderer_context)
