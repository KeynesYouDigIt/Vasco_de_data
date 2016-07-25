import os

from Vasco import *

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

#on switch
manager = Manager(app)

#migrations
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

@manager.command
def list_routes():
    '''Taken from http://flask.pocoo.org/snippets/117/'''
    import urllib
    from flask import render_template, url_for
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, url))
        output.append(line)
    
    for line in sorted(output):
        print line

if __name__ == '__main__':
    manager.run()
