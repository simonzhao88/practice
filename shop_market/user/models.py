from django.db import models


class UserModel(models.Model):
    """用户表"""
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=256)
    email = models.CharField(max_length=64, unique=True)
    sex = models.BooleanField(default=False)   # 性别  默认为女
    icon = models.ImageField(upload_to='uploads/icons')  # 头像
    is_delete = models.BooleanField(default=False)  # 是否删除 默认为未删除

    class Meta:
        db_table = 'xf_users'


class UserTicketModel(models.Model):
    """用户口令表"""
    user = models.ForeignKey(UserModel)   # 关联用户
    ticket = models.CharField(max_length=256)   # 口令
    out_time = models.DateTimeField()   # 过期时间

    class Meta:
        db_table = 'xf_users_ticket'
