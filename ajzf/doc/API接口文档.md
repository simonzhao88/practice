# 爱家住房接口文档 v1.01

## 1.用户模块接口
* 注册

request请求

    POST /auth/register/

params参数

    phone str 手机号
    password str 密码
    password2 str 确认密码

response响应

成功响应：

    {'code': 200, 'msg': '请求成功~'}
    
失败响应1：
    
    {'code': 1001, 'msg': '请填写完所有参数~'}
    
失败响应2：

    {'code': 1002, 'msg': '请输入正确的手机号~'}
失败响应3：

    {'code': 1003, 'msg': '两次输入密码不一致~'}
失败响应4：

    {'code': 1004, 'msg': '该用户已注册，请直接登录~'}
    
* 登录

request请求

    POST /auth/login/

params参数

    phone str 手机号
    password str 密码

response响应

成功响应：

    {'code': 200, 'msg': '登录成功~'}
    
失败响应1：
    
    {'code': 1005, 'msg': '请填写完所有参数~'}
    
失败响应2：

    {'code': 1007, 'msg': '用户名或密码错误~'}
失败响应3：

    {'code': 1006, 'msg': '用户不存在，请先注册~'}
    
* 注销

request请求

    DELETE /auth/logout/
response响应

    {
        'code': 200,
        'msg': '请求成功'
    }

* 个人中心

    * 获取用户信息
    
        request请求
        
            GET /api/mine/
        response响应
        
            {
                'code': 200,
                'msg': '请求成功~',
                'data': {
                    'phone': u.phone,
                    'name': u.name,
                    'avatar': u.avatar
                }
            }
    * 修改用户信息
    
        request请求
        
            patch /api/profile/
            
        params参数
            
            avatar file 用户头像
            name str 用户名
        response响应
        
        成功响应：
         
        上传头像图片：
            
            { "code": "200", "url": "/static/upload\landlord01.jpg" }
        修改用户名：
        
            { 'code': 200, 'msg': '修改用户名成功~' }
        
        失败响应1：
            
            {'code': 1008, 'msg': '上传图片格式错误~'}
        失败响应2：
        
            {'code': 0, 'msg': '数据库错误，稍后重试~'}
        失败响应3：
        
            {'code': 1009, 'msg': '用户名已存在，请重新设置~'}
            
    * 获取实名认证信息
    
        request请求
        
            GET /api/authentication/
            
        response响应
        
            {
            'id_name': self.id_name,
            'id_card': self.id_card
        }
        
    * 修改实名认证信息
    
        request请求
        
            PATCH /api/profile/
            
        params参数
        
            real_name str 用户真实姓名
            id_card str 用户身份证号
            
        response响应
        
        成功响应：
        
            {'code': 200, 'msg': '请求成功~'}
        
        失败响应1：
        
            {'code': 1010, 'msg': '实名认证信息不完整~'}
        失败响应2：
        
            {'code': 1012, 'msg': '用户已实名，如需修改请联系客服~'}
        失败响应3：
        
            {'code': 0, 'msg': '数据库错误，稍后重试~'}
            

##房屋模块接口

* 我的房源信息

request 请求

    GET /api/house/
response 响应

成功响应1：
    
    {
    "code": "200",
    "data": [{
            "address": "xxx100号",
            "area": "锦江区",
            "create_time": "2018-05-21 08:59:08",
            "id": 7,
            "image": "/static/upload/house\\mvc.png",
            "order_count": 0,
            "price": 251,
            "room": 10,
            "title": "情侣公寓"
        },
        {
            "address": "天府大道",
            "area": "锦江区",
            "create_time": "2018-05-20 15:24:19",
            "id": 2,
            "image": "\\static\%upload\\house\\orm.png",
            "order_count": 0,
            "price": 166,
            "room": 10,
            "title": "单身公寓"
        }
    ]
    }
成功响应2：

    {'code': 1013, 'msg': '用户没有实名认证~'}

响应参数：

    id int ID
    address str 地址
    area str 区域名称
    create_time str 创建时间
    image file 房间图片
    order_count int 住过几次
    room int 可出租房间个数
    title str 房屋标题
    
* 添加新房源
request 请求

    PSOT /api/house/
    
params参数

    title str 房屋名
    price int 单价
    address str 地址
    room_count int 房间数目
    acreage int 房屋面积
    unit str 房屋单元， 如几室几厅
    capacity int 房屋容纳的人数
    beds str 房屋床铺的配置
    deposit int 房屋押金
    min_days int 最少入住天数
    max_days int 最多入住天数，0表示不限制
    order_count int 预订完成的该房屋的订单数
    facilities int 房屋设施
    
response 响应

成功响应：
    
    {
        'code': 200,
        'msg': '请求成功~',
        'house_id': house_id
    }
失败响应1：

    {'code': 2001, 'msg': '请将全部信息填写完整后再提交~'}
失败响应2：
    
    {'code': 0, 'msg': '数据库错误，稍后重试~'}

* 添加房源图片

request 请求
    
    POST /api/house/image/
    
params参数

    house_image file 房源图片
    house_id int 房屋编号
response 响应

成功响应：

    {'code': 200, 'msg': '请求成功~'}
失败响应1：

    {'code': 1008, 'msg': '上传图片格式错误~'}
失败响应2：
    
    {'code': 0, 'msg': '数据库错误，稍后重试~'}
    
* 房屋详情
request 请求

    GET /api/house/detail/
    
param 参数
    
    house_id int 房屋编号
    
response 响应

成功响应：
    
    {
      "code": 200,
      "data": {
        "acreage": 666,
        "address": "武侯区火车南站站前广场",
        "beds": "大床房 250*222",
        "capacity": 1,
        "deposit": 135,
        "facilities": [
          {
            "css": "wirelessnetwork-ico",
            "id": 1,
            "name": "无线网络"
          },
          {
            "css": "heater-ico",
            "id": 4,
            "name": "暖气"
          },
          {
            "css": "smoke-ico",
            "id": 5,
            "name": "允许吸烟"
          },
          {
            "css": "elevator-ico",
            "id": 15,
            "name": "电梯"
          },
          {
            "css": "pet-ico",
            "id": 17,
            "name": "允许带宠物"
          },
          {
            "css": "meet-ico",
            "id": 18,
            "name": "允许聚会"
          },
          {
            "css": "accesssys-ico",
            "id": 19,
            "name": "门禁系统"
          },
          {
            "css": "tv-ico",
            "id": 22,
            "name": "电视"
          }
        ],
        "id": 5,
        "images": [
          "upload\\5\\home01.jpg",
          "upload\\5\\home02.jpg",
          "upload\\5\\home03.jpg"
        ],
        "max_days": 0,
        "min_days": 1,
        "order_count": 0,
        "price": 235,
        "room_count": 1,
        "title": "火车南站大床房",
        "unit": "一室",
        "user_avatar": "upload\\1529486595570001.jpg",
        "user_name": "admin"
      }
    }
失败响应：
    
    {'code': 2003, 'msg': '无此房屋信息，请查验后再查询~'}

响应参数：
    
facilities：配套设置的信息
    
    id int ID
    css str 样式
    name str 名称
    
data：房屋的信息

    acreage int 房屋面积
    address str 面积
    beds str 房屋床铺的配置
    deposit	int 房屋押金
    facilities str 配套设施
    id int ID
    image str 房屋图片
    min_days int 最少入住天数
    max_days int 最多入住天数，0表示不限制
    order_count int 预订完成的该房屋的订单数
    price str 价格
    user_avatar str 用户头像
    user_name str 用户名称
    
* 预约页面信息

同房屋详情接口
    
## 预约模块接口

* 预约创建

request 请求
    
    POST /api/order/
param 参数

    house_id int 房屋id
    start_date str 入住开始时间
    end_date str 结束时间
    price int 房屋单价
response 响应
    
失败响应1：

    {'code': 1000, 'msg': '请填写完所有参数~'}
失败响应2：

    {'code': 3001, 'msg': '订单入住时间错误~'}
失败响应3：
    
    {'code': 0, 'msg': '数据库错误，稍后重试~'}
成功响应：

    {'code': 200, 'msg': '请求成功~'}