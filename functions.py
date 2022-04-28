from flask import *
from datetime import datetime
import pytz
from passlib.hash import sha256_crypt
import mysql.connector
import os
from dotenv import load_dotenv
import pandas as pd
from pywebpush import webpush

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

tz = pytz.timezone(os.environ.get('TIMEZONE'))

PERIODS = {
    'm': '08:00',
    '1': '08:20',
    '2': '09:15',
    '3': '10:10',
    '4': '11:05',
    '5': '13:15',
    '6': '14:10',
    '7': '15:05',
    '8': '15:55',
    '9': '16:45',
}

def refresh_db():
    return mysql.connector.connect(user=os.environ.get('MYSQL_USER'), password=os.environ.get('MYSQL_PASSWORD'),
                                   host=os.environ.get('MYSQL_HOST'),
                                   database=os.environ.get('MYSQL_DATABASE'))

def genHash(password):
    return sha256_crypt.hash(password)


def verifyPassword(password, hash):
    return sha256_crypt.verify(password, hash)

def isLogin():
    return ('is_logged_in' in session and
            'loginTime' in session and
            session['is_logged_in'] == True and
            (datetime.now(tz) - session['loginTime']).total_seconds() < int(os.environ.get('LOGIN_TIMEOUT')))
