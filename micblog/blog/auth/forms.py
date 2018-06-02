from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo, ValidationError

from blog.models import User


class LoginForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Remember_me')
    submit = SubmitField('登录')


class RegistrationForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    username = StringField('Username', validators=[Required(), Length(1, 64),
                                                   Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                          '用户名需由字母、数字下划线组成~~')])
    password = PasswordField('Password', validators=[Required(), EqualTo('password2',
                                                                         message='两次输入密码不一致~~')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已被注册~~')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已被使用~~')


class ChangepwdForm(Form):
    oldpwd = PasswordField('旧密码', validators=[Required()])
    newpwd1 = PasswordField('新密码', validators=[Required(), EqualTo('newpwd2',
                                                                   message='两次输入密码不一致~~')])
    newpwd2 = PasswordField('确认密码', validators=[Required()])
    submit = SubmitField('提交')
