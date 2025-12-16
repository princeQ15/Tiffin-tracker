from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                         validators=[DataRequired(), 
                                   Length(min=4, max=20, message='Username must be between 4 and 20 characters')])
    email = EmailField('Email',
                      validators=[DataRequired(), 
                                Email(message='Please enter a valid email address')])
    password = PasswordField('Password', 
                           validators=[DataRequired(),
                                     Length(min=8, message='Password must be at least 8 characters')])
    confirm_password = PasswordField('Confirm Password',
                                   validators=[DataRequired(),
                                             EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered. Please use a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email',
                       validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                           validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                         validators=[DataRequired(), 
                                   Length(min=4, max=20)])
    email = EmailField('Email',
                      validators=[DataRequired(), 
                                Email()])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is already taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is already registered. Please use a different one.')

class RequestResetForm(FlaskForm):
    email = EmailField('Email',
                     validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', 
                           validators=[DataRequired(),
                                     Length(min=8, message='Password must be at least 8 characters')])
    confirm_password = PasswordField('Confirm Password',
                                   validators=[DataRequired(),
                                             EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Reset Password')
