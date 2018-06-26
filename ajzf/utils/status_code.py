OK = 200
DATABASE_ERROR = {'code': 0, 'msg': '数据库错误，稍后重试~'}
SUCCESS = {'code': 200, 'msg': '请求成功~'}
DATA_NOT_FULL = {'code': 1000, 'msg': '请填写完所有参数~'}
LOGIN_REQUIRED = {'code': 404, 'msg': '请登录~'}
# 用户模块
USER_REGISTER_NOT_NULL = {'code': 1001, 'msg': '请填写完所有参数~'}
USER_REGISTER_MOBILE_ERROR = {'code': 1002, 'msg': '请输入正确的手机号~'}
USER_REGISTER_PASSWORD_IS_NOT_VALID = {'code': 1003, 'msg': '两次输入密码不一致~'}
USER_REGISTER_EXITS_USER = {'code': 1004, 'msg': '该用户已注册，请直接登录~'}


USER_LOGIN_NOT_NULL = {'code': 1005, 'msg': '请填写完所有参数~'}
USER_LOGIN_MOBILE_ERROE = {'code': 1006, 'msg': '用户不存在，请先注册~'}
USER_LOGIN_PASSWORD_ERROE = {'code': 1007, 'msg': '用户名或密码错误~'}


USER_CHANGE_PROFILE_IMAGES_ERROR = {'code': 1008, 'msg': '上传图片格式错误~'}
USER_CHANGE_PROFILE_NAME_ERROR = {'code': 1009, 'msg': '用户名已存在，请重新设置~'}


USER_AUTH_DATA_IS_NOT_NULL = {'code': 1010, 'msg': '实名认证信息不完整~'}
USER_AUTH_ID_CARD_IS_NOT_VALID = {'code': 1011, 'msg': '身份证号错误~'}
USER_AUTH_NOT_AUTHENTICATION = {'code': 1013, 'msg': '用户没有实名认证~'}
USER_AUTH_IS_EXITS_ERROR = {'code': 1012, 'msg': '用户已实名，如需修改请联系客服~'}

# 房屋模块

HOUSE_ADD_DATA_IS_NOT_NULL = {'code': 2001, 'msg': '请将全部信息填写完整后再提交~'}
HOUSE_ADD_HOUSE_IMAGE_ERROR = {'code': 2002, 'msg': '上传图片格式错误~'}
HOUSE_QUERY_ERROR = {'code': 2003, 'msg': '无此房屋信息，请查验后再查询~'}

# 订单模块

CREATE_ORDER_END_DATA_ERROR = {'code': 3001, 'msg': '订单入住时间错误~'}
CREATE_ORDER_START_DATA_ERROR = {'code': 3002, 'msg': '订单退房时间错误~'}
