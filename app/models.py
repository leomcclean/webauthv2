from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import random, sys

def createPartials(password):
	_list = []
	for x in range(4):
		newRdm = random.randint(0, len(password) - 1)
		while newRdm in _list:
			newRdm = random.randint(0, len(password) - 1)
		_list.append(newRdm)
	_list.sort()
	return _list
	
def shortPassHash(password, short_pass):
	newStr = ''
	for i in range(4):
		newStr += password[int(short_pass[i])]
	short_pass_hash = generate_password_hash(newStr)
	return short_pass_hash
		
def toString(array):
	string = ''
	for i in array:
		string += str(i+1) + ', '
	string = string[:-1]
	string = string[:-1]
	return string

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	user_hash = db.Column(db.String(128))
	
	email = db.Column(db.String(120), index=True, unique=True)
	phone = db.Column(db.String(64), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	
	short_pass1 = db.Column(db.String(64))
	short_hash1 = db.Column(db.String(128))
	short_pass2 = db.Column(db.String(64))
	short_hash2 = db.Column(db.String(128))
	short_pass3 = db.Column(db.String(64))
	short_hash3 = db.Column(db.String(128))
	
	def hashName(self):
		self.user_hash = generate_password_hash(self.username)
	
	def setPassword(self, password):
		self.password_hash = generate_password_hash(password)
		
		short_pass = createPartials(password)
		short_hash = shortPassHash(password, short_pass)
		short_pass = toString(short_pass)
		self.short_hash1 = short_hash
		self.short_pass1 = short_pass
		
		short_pass = createPartials(password)
		temp = toString(short_pass)
		while temp == self.short_pass1:
			short_pass = createPartials(password)
			temp = toString(short_pass)
		short_hash = shortPassHash(password, short_pass)
		short_pass = temp
		self.short_hash2 = short_hash
		self.short_pass2 = short_pass
		
		short_pass = createPartials(password)
		temp = toString(short_pass)
		while temp == self.short_pass1 or temp == self.short_pass2:
			short_pass = createPartials(password)
			temp = toString(short_pass)
		short_hash = shortPassHash(password, short_pass)
		short_pass = temp
		self.short_hash3 = short_hash
		self.short_pass3 = short_pass

	def returnShortPass(self):
		newRdm = random.randint(1, 3)
		if newRdm == 1:
			return self.short_pass1
		elif newRdm == 2:
			return self.short_pass2
		elif newRdm == 3:
			return self.short_pass3
			
	def returnPassHash(self):
		return self.password_hash

	def checkPPassword(self, password, short_pass):
		if short_pass == self.short_pass1:
			return check_password_hash(self.short_hash1, password)
		elif short_pass == self.short_pass2:
			return check_password_hash(self.short_hash2, password)
		elif short_pass == self.short_pass3:
			return check_password_hash(self.short_hash3, password)
		else:
			return False

	def checkPassword(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return self.username
		
	@login.user_loader
	def load_user(id):
		return User.query.get(int(id))

