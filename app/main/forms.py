from app.models import User
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    PasswordField,
    StringField,
    SubmitField,
    TextAreaField)
from wtforms_components import TimeField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError


class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password')
    password_confirm = PasswordField(
        'Confirm password', validators=[EqualTo('password')])
    submit = SubmitField('Update profile')

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        # store original_username to perform unique check in validate_username
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if (username.data != self.original_username):
            # this might not be great for performance
            # better to cache this data/query?
            user = User.query.filter_by(username=username.data).first()

            if user is not None:
                raise ValidationError(
                    'You can\'t have that username right now.')

    def validate_email(self, email):
        if (email.data != self.original_email):
            user = User.query.filter_by(email=email.data).first()

            if user is not None:
                raise ValidationError(
                    'Someone already registered that email address.')


class PostForm(FlaskForm):
    title = StringField('Title (optional)')
    content = TextAreaField('', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    time = TimeField('Time', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def __init__(self, post_url, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.post_url = post_url


class PostDeleteForm(FlaskForm):
    confirm = BooleanField('Check here to confirm deletion of this post. Be '
                           'sure!', validators=[DataRequired()])
    submit = SubmitField('Delete it')
