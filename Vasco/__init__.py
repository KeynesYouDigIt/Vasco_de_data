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

#blueprints for moduarization of the app and its functions coming soon!

db = SQLAlchemy(app)
moment = Moment(app)
toolbar = DebugToolbarExtension(app)

from Vasco.models import *
from Vasco.views import *
from Vasco.order_takers import *