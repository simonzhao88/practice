"""
功能：继承序列化类，自定义序列化格式
author：simon
"""

from rest_framework import serializers

from stu.models import Student, Grade


class StudentSerializer(serializers.ModelSerializer):

    s_name = serializers.CharField(max_length=20, error_messages={
        'blank': '姓名字段不能为空'
    })

    class Meta:
        model = Student
        fields = ['id', 's_name', 's_img', 'g']

    def to_representation(self, instance):
        """
        利用外键获取想要的班级信息
        循环获取
        :param instance:
        :return:
        """
        data = super().to_representation(instance)
        data['g_name'] = instance.g.g_name

        return data


class GradeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Grade
        fields = ['id', 'g_name', 'g_create_time']

    def to_representation(self, instance):
        """
        利用外键获取想要的班级信息
        循环获取
        :param instance:
        :return:
        """
        data = super().to_representation(instance)
        data['g_create_time'] = instance.g_create_time.strftime("%Y-%m-%d %H:%M:%S")

        return data

    def do_update(self, instance, data):
        """
        将数据保存到数据库，实现持久化存储
        :param instance:
        :param data:
        :return:
        """
        instance.g_name = data['g_name']
        instance.save()
        # data = self.to_representation(instance)
        return data
