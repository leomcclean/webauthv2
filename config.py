#!/usr/bin/python3
import os
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
	SECRET_KEY = os.getenv('SECRET_KEY')
	if(os.getenv('ENVIRONMENT') == 0):
		SQLALCHEMY_DATABASE_URI = os.getenv('DB_URL')
	else:
		SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	WTF_CSRF_ENABLED = True
