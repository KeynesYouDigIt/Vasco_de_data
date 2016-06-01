from Vasco import *
db.create_all()
camelot = Entity(level='Province', name='Camelot',iso_code='CAM')
db.session.add(camelot)
lit = Literal_data(ent_id=1, year=2012, value=2, display_name = 'swallow count', meta_id=1)
db.session.add(lit)
swallow = Meta_indicator_data(p_name = 'swallow count',family = 'animal life',num_type = 'interger',provider = 'camelot bird comission',p_description = 'swallows. duh.')
db.session.add(swallow)
db.session.commit()