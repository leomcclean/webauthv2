from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, OTPForm, RegistrationForm, PasswordForm, ChangeForm
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
import random, sys, smtplib, ssl

def generateOTP(user_hash):
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
		
	user = User.query.filter_by(user_hash=user_hash).first()
	message = """\
Subject: New Login Attempt

Your one time password is """ + otp + '.'
		
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
		server.login('authwebv2@gmail.com', 'Rocket1234')
		server.sendmail('authwebv2@gmail.com', user.email, message)
	
	return otp

@app.route('/')
@app.route('/index')

@login_required
def index():
	return render_template('index.html', title='webAuthV2')
	
@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None:
			flash('Invalid username')
			return redirect(url_for('login'))
		user_hash = user.user_hash
		otp = generateOTP(user_hash)
		print(otp, file=sys.stdout)
		otp_hash = generate_password_hash(otp)
		return redirect(url_for('otp', user_hash=user_hash, otp_hash=otp_hash))
	return render_template('login.html', title='Sign In', form=form)

@app.route('/otp', methods=['GET', 'POST'])
def otp():
	user_hash = str(request.args.get('user_hash'))
	otp_hash = str(request.args.get('otp_hash'))
	form = OTPForm()
	if form.validate_on_submit():
		if not check_password_hash(otp_hash, form.code.data):
			flash('Incorrect one time password')
			return redirect(url_for('login'))
		count = 0
		if form.partial.data:
			user = User.query.filter_by(user_hash=user_hash).first()
			short_pass = user.returnShortPass()
			return redirect(url_for('login2', user_hash=user_hash, short_pass=short_pass, count=count))
		elif form.submit.data:
			return redirect(url_for('login3', user_hash=user_hash, count=count))
	return render_template('otp.html', title='One Time Password', form=form)

@app.route('/login2', methods=['GET', 'POST'])
def login2():
	user_hash = str(request.args.get('user_hash'))
	user = User.query.filter_by(user_hash=user_hash).first()
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
	return render_template('login2.html', title='Sign In', form=form)
	
@app.route('/login3', methods=['GET', 'POST'])
def login3():
	user_hash = str(request.args.get('user_hash'))
	user = User.query.filter_by(user_hash=user_hash).first()
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
	return render_template('login3.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.hashName()
		user.setPassword(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('You have now registered')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)
	
@app.route('/changep', methods=['GET', 'POST'])
def changep():
	form = ChangeForm()
	username = current_user.username
	user = User.query.filter_by(username=username).first()
	if form.validate_on_submit():
		if not user.checkPassword(form.oldpassword.data):
			flash('Incorrect password')
			return redirect(url_for('changep'))
		user.setPassword(form.newpassword.data)
		db.session.commit()
		flash('Password changed successfully')
		return redirect(url_for('index'))
	return render_template('changep.html', title='Change Password', form=form)
	
@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('login'))
