from flask_wtf import Form
from wtforms import StringField, BooleanField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Required, Length, Email


class LoginForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('Sign In')
