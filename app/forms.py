#!/usr/bin/python3
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User
import sys

def lengthCheck(form, field):
	if len(field.data) > 32 or len(field.data) < 10:
		raise ValidationError('Password must be a minimum of 10 and maximum of 20 characters.')

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	recaptcha = RecaptchaField()
	loginEmail = SubmitField('Log in with Email')
	loginSMS = SubmitField('Log in with SMS')
	
class OTPForm(FlaskForm):
	code = StringField('Code', validators=[DataRequired()])
	submit = SubmitField('Standard Password Login')
	partial = SubmitField('Partial Password Login')
	forgot = SubmitField('Forgot Password')
	
class PasswordForm(FlaskForm):
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired(), lengthCheck])
	password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
	recaptcha = RecaptchaField()
	submit = SubmitField('Register')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Please use a different username.')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Please use a different email address.')

class ChangeForm(FlaskForm):
	oldpassword = PasswordField('Current Password', validators=[DataRequired(), lengthCheck])
	newpassword = PasswordField('New Password', validators=[DataRequired(), lengthCheck])
	newpassword2 = PasswordField('Repeat New Password', validators=[DataRequired(), EqualTo('newpassword')])
	submit = SubmitField('Change Password')

