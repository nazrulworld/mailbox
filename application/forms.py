# _*_ coding=utf-8 _*_
from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField
from wtforms.validators import Required, Email
from .validators import EmailProviders


class LoginForm(Form):

    email = TextField('email', validators=[Required(message='E-mail address required'), Email(), EmailProviders()])
    password = PasswordField('password', validators=[Required(message='Password is required')])
    remember = BooleanField('remember', default=False)


