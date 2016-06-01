from flask import render_template, url_for, request, redirect, flash, abort
from datetime import datetime
from models import *
from Vasco import *
#from avail_eng import *

def make_wo():
	wo = 'wooooooo'
	return wo

#avail = get_avail()


@app.route('/')
@app.route('/index')
def ind():
    return render_template('index.html', 
        htwo='Welcome to Vasco de Data', 
        usr=avail, 
        shrub='avail')


@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500