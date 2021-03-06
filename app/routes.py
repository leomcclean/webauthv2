#!/usr/bin/python3
import os, pycountry
from geoip import geolite2
from dotenv import load_dotenv
from flask import render_template, flash, redirect, url_for, request, send_from_directory
from app import app, db
from app.forms import LoginForm, OTPForm, RegistrationForm, PasswordForm, ChangeForm
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
import random, sys, smtplib, ssl
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

def handleOTP(user_hash, email):
	account_sid = os.environ.get('ACCOUNT_SID')
	auth_token = os.environ.get('AUTH_TOKEN')
	client = Client(account_sid, auth_token)

	otp = ''
	for i in range(6):
		cType = random.randint(1,3)
		newRdm = 0
		if cType == 1:
			newRdm = random.randint(48,57)
		elif cType == 2:
			newRdm = random.randint(65,90)
		elif cType == 3:
			newRdm = random.randint(97,122)
		otp += chr(newRdm)

	if(email == False):
		client.messages.create(
			from_=os.environ.get('PHONE_NUMBER'),
			to=os.environ.get('USER_PHONE_NUMBER'),
			body='Your OTP is ' + otp)
	elif(email == True):
		user = User.query.filter_by(user_hash=user_hash).first()
		message = """\

		Subject: New Login Attempt

		Your one time password is """ + otp + '.'
	
		context = ssl.create_default_context()
		server = smtplib.SMTP_SSL(os.getenv('MAIL_SERVER'), os.getenv('MAIL_PORT'))
		server.login(os.getenv('MAIL_EMAIL'), os.getenv('MAIL_PASSWORD'))
		server.sendmail(os.getenv('MAIL_EMAIL'), user.email, message)
		server.quit()
		
	return otp

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
	ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
	match = geolite2.lookup(ip)
	if match is not None:
		country_object = pycountry.countries.lookup(str(match.country))
		country = country_object.name
	else:
		country = False
	user = User.query.filter_by(username=current_user.username).first()
	css = user.css
	if request.method == 'POST':
		css = int(request.form['css'])
		user.updateCSS(css)
		db.session.commit()
	return render_template('index.html', title='Home', ip=ip, country=country, css=css)
	
@app.route('/login', methods=['GET', 'POST'])
def login():
	Email = False
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	css = 1
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None:
			flash('Invalid username')
			return redirect(url_for('login'))
		if form.loginEmail.data:
			email = True
		elif form.loginSMS.data:
			email = False
		user_hash = user.user_hash
		otp = handleOTP(user_hash, email)
		otp_hash = generate_password_hash(otp)
		return redirect(url_for('otp', user_hash=user_hash, otp_hash=otp_hash))
	return render_template('login.html', title='Sign In', form=form, css=css)

@app.route('/otp', methods=['GET', 'POST'])
def otp():
	user_hash = str(request.args.get('user_hash'))
	otp_hash = str(request.args.get('otp_hash'))
	user = User.query.filter_by(user_hash=user_hash).first()
	css = user.css
	form = OTPForm()
	if form.validate_on_submit():
		if not check_password_hash(otp_hash, form.code.data):
			flash('Incorrect one time password')
			return redirect(url_for('login'))
		count = 0
		if form.partial.data:
			short_pass = user.returnShortPass()
			return redirect(url_for('login2', user_hash=user_hash, short_pass=short_pass, count=count))
		elif form.submit.data:
			return redirect(url_for('login3', user_hash=user_hash, count=count))
		elif form.forgot.data:
			login_user(user)
			return redirect(url_for('changep'))
	return render_template('otp.html', title='One Time Password', form=form, css=css)

@app.route('/login2', methods=['GET', 'POST'])
def login2():
	user_hash = str(request.args.get('user_hash'))
	user = User.query.filter_by(user_hash=user_hash).first()
	css = user.css
	short_pass = str(request.args.get('short_pass'))
	count = int(request.args.get('count'))
	form = PasswordForm()
	flash('Enter password characters ' + short_pass + " together with no spaces.")
	if form.validate_on_submit():
		if not user.checkPPassword(form.password.data, short_pass):
			count += 1
			if count == 3:
				flash('Out of attempts. New OTP required.')
				return redirect(url_for('login'))
			else:
				flash('Incorrect characters')
				flash('You have ' + str(3 - count) + ' attempts left before process reset')
				return redirect(url_for('login2', user_hash=user_hash, short_pass=short_pass, count=count))
		login_user(user)
		return redirect(url_for('index'))
	return render_template('login2.html', title='Sign In', form=form, css=css)
	
@app.route('/login3', methods=['GET', 'POST'])
def login3():
	user_hash = str(request.args.get('user_hash'))
	user = User.query.filter_by(user_hash=user_hash).first()
	css = user.css
	count = int(request.args.get('count'))
	form = PasswordForm()
	flash('Enter password.')
	if form.validate_on_submit():
		if not user.checkPassword(form.password.data):
			count += 1
			if count == 3:
				flash('Out of attempts. New OTP required.')
				return redirect(url_for('login'))
			else:
				flash('Incorrect password')
				flash('You have ' + str(3 - count) + ' attempts left before process reset')
				return redirect(url_for('login3', user_hash=user_hash, count=count))
		login_user(user)
		return redirect(url_for('index'))
	return render_template('login3.html', title='Sign In', form=form, css=css)

@app.route('/register', methods=['GET', 'POST'])
def register():
	css = 1
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.updateCSS(1)
		user.hashName()
		user.setPassword(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('You have now registered')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form, css=css)
	
@app.route('/changep', methods=['GET', 'POST'])
def changep():
	form = ChangeForm()
	username = current_user.username
	user = User.query.filter_by(username=username).first()
	css = user.css
	if form.validate_on_submit():
		if not user.checkPassword(form.oldpassword.data):
			flash('Incorrect password')
			return redirect(url_for('changep'))
		user.setPassword(form.newpassword.data)
		db.session.commit()
		flash('Password changed successfully')
		return redirect(url_for('index'))
	return render_template('changep.html', title='Change Password', form=form, css=css)
	
@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('login'))