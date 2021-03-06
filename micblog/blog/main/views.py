from flask import render_template, session, redirect, url_for, abort, flash, request, current_app, make_response
from flask_login import current_user, login_required

from blog.utils.check_permission import admin_required, permission_required
from . import main
from .forms import EditProfileForm, EditProfileAdminForm, PostForm, CommentForm
from .. import db
from ..models import User, Role, Permission, Post, Comment


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and \
            form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.index'))
    show_followed = False
    if current_user.is_authenticated:
        show_followed = request.cookies.get('show_followed', '')
    if show_followed == '1':
        query = current_user.followed_posts
    elif show_followed == '2':
        query = current_user.self_posts
    else:
        query = Post.query
    page = request.args.get('page', 1, type=int)
    pagination = query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['BLOG_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('index.html',
                           form=form, posts=posts,
                           Permission=Permission,
                           pagination=pagination)


@main.route('/user/<username>')
def user(username):
    u = User.query.filter_by(username=username).first()
    if u is None:
        abort(404)
    return render_template('user.html', user=u, Permission=Permission, )


@main.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        db.session.commit()
        flash('您的资料已经更新成功~')
        return redirect(url_for('.user',
                                username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form,
                           username=current_user.username,
                           Permission=Permission)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash('资料已更新~')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html',
                           form=form, user=user,
                           Permission=Permission)


@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          author_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        flash('评论成功~')
        return redirect(url_for('.post', id=post.id))
    page = request.args.get('page', 1, type=int)
    pagination = post.comments.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['BLOG_COMMENTS_PER_PAGE'], error_out=False
    )
    comments = pagination.items
    return render_template('post.html', posts=[post],
                           form=form, comments=comments,
                           pagination=pagination,
                           Permission=Permission)


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
            not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()
        flash('The post has been updated.')
        return redirect(url_for('.post', id=post.id))
    form.title.data = post.title
    form.body.data = post.body
    return render_template('edit_post.html', form=form,
                           Permission=Permission)


@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('没有此用户~')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash("你已经关注了此用户~")
        return redirect(url_for(".user", username=username))
    current_user.follow(user)
    flash("你已成功关注{}".format(username))
    return redirect(url_for('.user', username=username))


@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('没有此用户~')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash("你还未关注此用户~")
        return redirect(url_for(".user", username=username))
    current_user.unfollow(user)
    flash("你已成功取消关注{}".format(username))
    return redirect(url_for('.user', username=username))


@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('没有此用户~')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page=current_app.config['BLOG_FOLLOW_PER_PAGE'],
        error_out=False
    )
    follows = [{'user': item.follower, 'timestamp': item.timestamp} for
               item in pagination.items]
    return render_template('followers.html', user=user, title='关注者',
                           endpoint='.followers', pagination=pagination,
                           follows=follows, Permission=Permission)


@main.route('/followed/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('没有此用户~')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=current_app.config['BLOG_FOLLOW_PER_PAGE'],
        error_out=False
    )
    followeds = [{'user': item.followed, 'timestamp': item.timestamp} for
                 item in pagination.items]
    return render_template('followed.html', user=user, title='被关注者',
                           endpoint='.followers', pagination=pagination,
                           followeds=followeds, Permission=Permission)


@main.route('/all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '', max_age=7 * 24 * 60 * 60)
    return resp


@main.route('/followed')
@login_required
def show_followed():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '1', max_age=7 * 24 * 60 * 60)
    return resp


@main.route('/mine')
@login_required
def show_mine():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '2', max_age=7 * 24 * 60 * 60)
    return resp


@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['BLOG_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('moderate.html', comments=comments,
                           pagination=pagination, page=page,
                           Permission=Permission)


@main.route('/moderate/enable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_enable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('.moderate',
                            page=request.args.get('page', 1, type=int)))


@main.route('/moderate/disable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_disable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('.moderate',
                            page=request.args.get('page', 1, type=int)))
