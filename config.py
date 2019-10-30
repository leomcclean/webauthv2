import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	SECRET_KEY = 'ZTLA6DgGSQV0dsRc6n7Z'
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://ubuntu:@localhost:3306/db'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	WTF_CSRF_ENABLED = True
