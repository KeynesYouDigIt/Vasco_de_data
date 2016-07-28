"""
The models below are created in a Postgres database.

To work with them outside of the production database,
create a valid pg database connection string
and set it via os.environ['DATABASE_URL']='your string here'
The connection string will be something like-
postgresql://user:password@localhost:5432/DBNAME
Then run db.create_all() To start populating the data, run the procs stored in 
Vasco de Data\\Vasco\\ETL

see a full schema diagrame at
Vasco de Data\\archive\\diagrams\\db schema
"""
from Vasco import db

class Entity(db.Model):
    '''An entity is  a country, state, 
    or any other body about which there may be data.
    Data points about entities are refered to as indicators.'''

    __tablename__ = 'ent'
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    iso_code = db.Column(db.Text, nullable=True)
    get_literal = db.relationship('Literal_data', backref='ent', lazy='dynamic')


    @staticmethod
    def get_by_name(name):
        return Entity.query.filter_by(name=name).first()


    def __repr__(self):
        return "<this is '{}': it is a '{}' || db id is '{}'>".format(self.name, self.level, self.id)

class Meta_indicator_data(db.Model):
    '''There is significant data about the indicators that should be
    storable for each new indicator. This table stores the name, description, and other categorization
    data for each indicator.'''

    __tablename__ = 'meta'
    id = db.Column(db.Integer, primary_key=True)
    p_name = db.Column(db.Text, nullable=False, unique=True)
    family = db.Column(db.Text, nullable=False)
    num_type = db.Column(db.Text, nullable=False)
    provider = db.Column(db.Text, nullable=False)
    p_description = db.Column(db.Text, nullable=False)
    give_to_literal = db.relationship('Literal_data', backref='meta', lazy='dynamic')

    @staticmethod
    def get_by_name(name):
        return Meta_indicator_data.query.filter_by(p_name=name).first()


class Literal_data(db.Model):
    '''This table stores only the literal data, the year, and foreign keys
    used to retrieve the corresponding entity and meta data.'''
    __tablename__ = 'literal'
    id = db.Column(db.Integer, primary_key=True)
    ent_id = db.Column(db.Integer, db.ForeignKey('ent.id'))
    year = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Float, nullable=True)
    display_name = db.Column(db.Text, nullable=False)
    meta_id = db.Column(db.Integer, db.ForeignKey('meta.id'))


"""
I plan on releasing functionality that stores data sets and makes them
easy to retrieve and share. This is not part of the current release,
but below is the start of the code if anyone wants to start working
on it!

class Saved_data_sets(object):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    comments = db.Column(db.Text, nullable=False)
    tags = db.Column(db.Text, nullable=False)
    """
