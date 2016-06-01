import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext.moment import Moment
from flask_debugtoolbar import DebugToolbarExtension

basedir = os.getcwd()
app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:52186vato@localhost:5432/Ocean'

db = SQLAlchemy(app)
moment = Moment(app)
toolbar = DebugToolbarExtension(app)

import models
from Vasco.models import *
import views
from views import *
