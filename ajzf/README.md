
## 项目搭建：

### 1. 环境virtualenv
	virtualenv --no-site-packages ajenv
	
### 2. 激活环境
	windows:
		cd ajenv/Script
		activate / deativate
	linux,mac:
		source ajenv/Script/bin/activate
		
### 3. 并安装flask
    1）pip3 install flask

    2)创建需要安装环境的txt文件
	    requeirement.txt中加入flask

		pip install -r requirement.txt
    
### 4. 一个最小的web

    from flask import Flask

    app = Flask(__name__)

    @app.route('/')
    def hello():
    	return 'hello world'

    if __name__ == '__main__':
    	app.run()

### 5. MVC思路拆分项目

### 6. pycharm配置

    setting中python解释器指定
    debug模式的配置文件配置，启动方式修改
    python xxx.py runserver -p -h -d
    
## 用户模块：
	
### 1. 注册(演示)
    用户名，密码，重复密码
    POST  /use/register/
    # 1. 验证数据完整性
    # 2. 验证手机号码的正确性
    # 3. 验证密码
    # 4. 保存用户数据
### 2. 登录(演示)
    用户名，密码，校验密码
    POST /user/login/
        mobile
        password

    # 1.验证数据完整
    # 2.验证手机正确性
    # 3.验证用户
    # 4.校验密码
    # 5.验证用户成功

### 3. 装饰器
	验证登录与否

### 4. 上传头像(演示)
	图片上传，图片展示，修改用户名

### 5. 注销
	删除session中的值

### 6. 实名认证
    验证身份证合法性
    保存用户实名信息
    实名后不可再次提交数据
    
## 房屋模块：

### 1. 我的房源

	实名认证展示
	发布房源

### 2. 发布房源

    2.1）房屋信息保存，房屋设备信息保存
    2.2）区域信息，房屋设备信息
    2.3) 发布房屋图片上传
		设置默认房屋的第一张图片为房源首页显示图片
	2.4) 将房源信息做持久化存储
		
### 3. 房屋详情

    利用接口获取房屋信息
    通过js将数据动态加载到页面

### 4. 网站首页

    利用接口获取房屋信息
    js渲染数据到页面
    接入搜索接口
    
### 5. 搜索页面
    
    根据条件筛选房屋信息
    
## 订单模块

### 1. 预约房屋
    
    利用接口获取房屋信息
    通过js将数据动态加载到页面
    根据住宿天数计算金额
    将订单信息做持久化存储

### 2. 我的订单
    
    利用接口获取订单信息
    实现退单，支付，评论功能

### 3.客户订单

    利用接口获取客户订单信息
    实现接单，拒单功能