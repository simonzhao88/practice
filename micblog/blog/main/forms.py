from flask_wtf import Form
from wtforms import StringField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.validators import Required, Length, Email, Regexp, ValidationError

from blog.models import Role, User


class NameForm(Form):
    name = StringField('name', validators=[Required()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('Submit')


class EditProfileForm(Form):
    name = StringField('Real Name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = StringField('About-Me')
    submit = SubmitField('Submit')


class EditProfileAdminForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已被注册~')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已被使用~')


class PostForm(Form):
    title = StringField('文章标题:', validators=[Required()])
    body = TextAreaField('在此撰写你的文章~~', validators=[Required()])
    submit = SubmitField('提交')
