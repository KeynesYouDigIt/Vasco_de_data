from datetime import datetime
from sqlalchemy import desc
from Vasco import db
#from flask_login import UserMixin
#from werkzeug.security import check_password_hash, generate_password_hash

class Entity(db.Model):
    '''An entity is  a country, state, or any other body *about which* there may be data.'''
    __tablename__ = 'ent'
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    iso_code = db.Column(db.Text, nullable=True)
    get_literal = db.relationship('Literal_data', backref='ent', lazy='dynamic')


    @staticmethod
    def get_by_name(name):
        return User.query.filter_by(name=name).first()


    def __repr__(self):
        return "<this is '{}': it is a '{}' || db id is '{}'>".format(self.name, self.level, self.id)

class Meta_indicator_data(db.Model):
    '''this tabe holds in depth data on indictor descriptions and sources'''
    __tablename__ = 'meta'
    id = db.Column(db.Integer, primary_key=True)
    p_name = db.Column(db.Text, nullable=False)
    family = db.Column(db.Text, nullable=False)
    num_type = db.Column(db.Text, nullable=False)
    provider = db.Column(db.Text, nullable=False)
    p_description = db.Column(db.Text, nullable=False)
    give_to_literal = db.relationship('Literal_data', backref='meta', lazy='dynamic')

    @staticmethod
    def get_by_name(name):
        return User.query.filter_by(p_name=name).first()


class Literal_data(db.Model):
    '''this stores only the literal data, the year, and where to get the corresponding entity and meta data.'''
    __tablename__ = 'literal'
    id = db.Column(db.Integer, primary_key=True)
    ent_id = db.Column(db.Integer, db.ForeignKey('ent.id'))
    year = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Float, nullable=True)
    display_name = db.Column(db.Text, nullable=False)
    meta_id = db.Column(db.Integer, db.ForeignKey('meta.id'))



class Saved_data_sets(object):
    """docstring for Data_sets"""
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    comments = db.Column(db.Text, nullable=False)
    tags = db.Column(db.Text, nullable=False)
        

#Running sql on the above
#hey=db.engine.execute('select * from User')
#    #consider making new var to actualy use data
#data = hey.fetchall() http://docs.sqlalchemy.org/en/latest/core/connections.html
