from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user

from blog import db
from blog.models import User, Permission
from . import auth
from .forms import LoginForm, RegistrationForm, ChangepwdForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('邮箱或密码错误~~')
    return render_template('auth/login.html', form=form, Permission=Permission)


@auth.route('/logout/<exchange>')
@login_required
def logout(exchange):
    logout_user()
    flash('登出成功~~')
    res = redirect(url_for('main.index'))
    if exchange == '1':
        res = redirect(url_for('.login'))
    res.delete_cookie('show_followed')
    return res


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data)
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        flash('注册成功~~')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form,
                           Permission=Permission)


@auth.route('/changepwd', methods=['GET', 'POST'])
@login_required
def changepwd():
    form = ChangepwdForm()
    if not current_user:
        flash('请您先登录~~')
        return redirect(url_for('auth.login'))
    if form.validate_on_submit():
        user = current_user
        if user is not None and user.verify_password(form.oldpwd.data):
            user.password = form.newpwd1.data
            db.session.add(user)
            db.session.commit()
            flash('修改密码成功~~')
            return redirect(url_for('auth.login'))
        flash('原密码输入错误~~')
    return render_template('auth/changepwd.html', form=form,
                           Permission=Permission)


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()



