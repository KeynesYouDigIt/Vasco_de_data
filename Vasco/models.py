from datetime import datetime
from sqlalchemy import desc
from Vasco import db

"""
The models below were able to connect to and be created in my Postgres database, and stored the test data in /tests/
They will be used to store parsed results from various public data APIs

see a full schema at
Vasco de Data\\archive\\diagrams\\db schema
"""

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
    """In the early release days, i will allow storing of some shared data sets to give users and idea where to start
    this table also serves as a boiler plate from which I can build a robust login and save data sets system"""
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    comments = db.Column(db.Text, nullable=False)
    tags = db.Column(db.Text, nullable=False)
