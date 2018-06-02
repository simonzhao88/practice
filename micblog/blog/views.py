# from datetime import datetime
# from flask import render_template, flash, redirect, url_for, session, request, g
# from flask_login import current_user, login_user, login_required, logout_user
#
# from  import app, login_manager, db
#
# from .models import User
#
#
# @login_manager.user_loader
# def load_user(id):
#     return User.query.get(int(id))
#
#
# @app.route('/')
# @app.route('/index')
# # @login_required
# def index():
#     user = g.user
#     posts = [
#         {
#             'author': {'nickname': 'Jhon'}
#         },
#         {
#             'author': {'nickname': 'Susan'},
#             'body': 'The Avengers movie was so cool!'
#         }
#     ]
#     return render_template('index.html', title='Home',
#                            user=user, posts=posts, current_time=datetime.utcnow())
#
#
# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404
#
#
# @app.before_request
# def before_request():
#     g.user = current_user
#
#
# def after_login(resp):
#     if resp.email is None or resp.email == "":
#         flash('Invalid login. Please try again.')
#         return redirect(url_for('login'))
#     user = User.query.filter_by(email=resp.email).first()
#     if user is None:
#         nickname = resp.nickname
#         if nickname is None or nickname == "":
#             nickname = resp.email.split('@')[0]
#         user = User(nickname=nickname, email=resp.email)
#         db.session.add(user)
#         db.session.commit()
#     remember_me = False
#     if 'remember_me' in session:
#         remember_me = session['remember_me']
#         session.pop('remember_me', None)
#     login_user(user, remember=remember_me)
#     return redirect(request.args.get('next') or url_for('index'))
#
#
# @app.route('/logout')
# def logout():
#     logout_user()
#     return redirect(url_for('index'))

