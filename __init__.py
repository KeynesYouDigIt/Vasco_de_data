#Embedded file name: C:\Users\Vince\Google Drive\PeacefulMandE\HelloWorldFlask\hello\__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask.ext.moment import Moment
from flask_debugtoolbar import DebugToolbarExtension
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'hello.db')
db = SQLAlchemy(app)
moment = Moment(app)
toolbar = DebugToolbarExtension(app)

import models
from models import *
import views
from views import *
