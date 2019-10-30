import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
	SECRET_KEY = os.environ.get('SECRET_KEY')
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://webauthv2:Rocket1234@webauthv2db.cxvqbz3pght8.eu-west-1.rds.amazonaws.com:3306/webauthv2db'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	WTF_CSRF_ENABLED = True
