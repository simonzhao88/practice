

from flask_wtf import Form
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import Required


class NameForm(Form):
    name = StringField('name', validators=[Required()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('Submit')
