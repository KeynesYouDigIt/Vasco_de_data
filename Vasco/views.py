from flask import render_template, url_for, request, redirect, flash, abort
from datetime import datetime
from models import *
from Vasco import *
from avail_eng import *

avail = get_avail()


@app.route('/')
@app.route('/index')
'''this is the only current connection between the front end an the data itself. 
Within the next couple weeks, I plan on replacing it with a robust system that calls the public data APIs and stores the data in a Postgres database for easy retrival.'''
def ind():
    return render_template('index.html', 
        htwo='Welcome to Vasco de Data', 
        usr=avail, 
        shrub='shruberyyyy')


@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500