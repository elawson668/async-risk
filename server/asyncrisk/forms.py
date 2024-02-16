from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from asyncrisk.models import Users

# writing python classes that will be converted to html forms in template


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=7, max=20)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=10, max=80)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Create User')

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Use something else.')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already taken. Use something else.')


class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=10, max=80)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=7, max=20)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = Users.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is already taken. Choose something else.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = Users.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is already taken. Choose something else.')


class ChangePasswordForm(FlaskForm):
    current_pass = PasswordField('Current Password', validators=[Length(min=10, max=80)])
    new_pass = PasswordField('New Password', validators=[Length(min=10, max=80)])
    submit = SubmitField('Update')