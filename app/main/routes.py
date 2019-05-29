from app import db
from app.auth.email import send_password_reset_email
from app.main import bp
from app.main.forms import (
    PostForm,
    PostDeleteForm,
    ProfileForm)
from app.models import Post, User
from datetime import datetime
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required


@bp.route('/')
@bp.route('/index')
def index():
    if current_user.is_authenticated:
        posts = current_user.posts.order_by(Post.timestamp.desc()).limit(5)
        form = PostForm(post_url=url_for('main.new_post'))

        if form.validate_on_submit():
            postdatetime = datetime.strptime('{} {}'.format(
                form.date.data, form.time.data), '%Y-%m-%d %H:%M:%S')
            post = Post(title=form.title.data, timestamp=postdatetime,
                        content=form.content.data)
            db.session.add(post)
            db.session.commit()

            flash('New post added')

            return redirect(url_for('main.index'))

        elif request.method == 'GET':
            # TODO: assign timezone to each user?
            dt = datetime.now()
            form.date.data = dt.date()
            form.time.data = dt.time()

            return render_template('auth/index.html', posts=posts, form=form)
    else:
        return render_template('index.html', title='Home')


@bp.route('/profile')
@login_required
def profile():
    return redirect(url_for('main.profile_edit'))


@bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def profile_edit():
    form = ProfileForm(current_user.username, current_user.email)

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data

        if form.password.data:
            current_user.set_password(form.password.data)

        db.session.commit()

        flash('Updated your info. All set you bet.')

        return redirect(url_for('main.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    return render_template('auth/profile_edit.html', title='Edit profile',
                           form=form)


@bp.route('/posts', methods=['GET'])
@login_required
def posts():
    posts = current_user.posts.all()
    return render_template('post/all.html', posts=posts)


@bp.route('/posts/new', methods=['POST'])
@login_required
def new_post():
    form = PostForm(post_url=url_for('main.new_post'))

    if form.validate_on_submit():
        postdatetime = datetime.strptime('{} {}'.format(
            form.date.data, form.time.data), '%Y-%m-%d %H:%M:%S')
        post = Post(title=form.title.data, timestamp=postdatetime,
                    content=form.content.data, user=current_user)
        db.session.add(post)
        db.session.commit()

        flash('New post added')
    else:
        flash('Oops!')

    return redirect(url_for('main.index'))


@bp.route('/posts/<post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    form = PostForm(post_url=url_for('main.edit_post', post_id=post_id))

    if form.validate_on_submit():
        postdatetime = datetime.strptime('{} {}'.format(
            form.date.data, form.time.data), '%Y-%m-%d %H:%M:%S')
        post.title = form.title.data
        post.content = form.content.data
        post.timestamp = postdatetime

        db.session.add(post)
        db.session.commit()

        flash('Post updated!')

        # TODO: check for referring page to go right back into page 4 of posts?
        return redirect(url_for('main.index'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.date.data = post.timestamp.date()
        form.time.data = post.timestamp.time()
    else:
        flash('Uh oh, something went afoul with that edit. Try again?')

    return render_template('post/edit.html', title='Edit post', post=post,
                           form=form)


@bp.route('/posts/<post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    form = PostDeleteForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            db.session.delete(post)
            db.session.commit()

            flash('Your post has been deleted. Bu-bye post!')

            return redirect(url_for('main.index',))
        else:
            flash('Hm, something went sideways trying to delete that post.'
                  'We\'ll look in to it.')

    return render_template('post/delete.html', title='Delete post', post=post,
                           form=form)
