import jwt

from datetime import datetime
from time import time

from app import db, login
from flask import current_app
from flask_login import UserMixin
from app.helpers import format_dbdatetime
from werkzeug.security import check_password_hash, generate_password_hash
from slugify import slugify
from sqlalchemy import event, extract
from sqlalchemy.ext.hybrid import hybrid_property


# flask_login requires this method to know how to load users by id
@login.user_loader
def load_user(id):
    # flask_login puts the user retrieved below in the database session, so you
    # never need to db.session.add() the current_user - it's already there
    # (confusing? yes.)
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # first argument below references class name 'Post', not the table name
    # 'post'. sigh.
    posts = db.relationship('Post', backref='user', lazy='dynamic',
                            cascade='delete', order_by="desc(Post.timestamp)")

    def __repr__(self):
        return '<User {} / {}>'.format(self.username, self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        # we decode at the end to get a string - otherwise it would be a byte
        # sequence
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return

        return User.query.get(id)

    def previous_years_posts(self):
        posts = Post.query.filter_by(user_id=self.id).filter(
            Post.timestamp_day == datetime.today().day,
            Post.timestamp_month == datetime.today().month,
            Post.timestamp_year != datetime.today().year
        ).order_by(Post.timestamp.desc()).all()

        return posts if len(posts) > 0 else False


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=True)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {} / user: {}>'.format(
            self.id, self.user.username)

    @hybrid_property
    def formatted_time(self):
        return format_dbdatetime(self.timestamp)

    @hybrid_property
    def timestamp_day(self):
        """
        gets the day from the python instance of timestamp
        """
        return self.timestamp.day

    @timestamp_day.expression
    def timestamp_day(cls):
        """
        how to translate 'timestamp_day' into a sql expression
        """
        return extract('day', cls.timestamp)

    @hybrid_property
    def timestamp_month(self):
        return self.timestamp.month

    @timestamp_month.expression
    def timestamp_month(cls):
        return extract('month', cls.timestamp)

    @hybrid_property
    def timestamp_year(self):
        return self.timestamp.year

    @timestamp_year.expression
    def timestamp_year(cls):
        return extract('year', cls.timestamp)
