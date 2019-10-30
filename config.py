import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	SECRET_KEY = 'ZTLA6DgGSQV0dsRc6n7Z'
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://webauthv2:Rocket1234@webauthv2db.cxvqbz3pght8.eu-west-1.rds.amazonaws.com/webauthv2db'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	WTF_CSRF_ENABLED = True
