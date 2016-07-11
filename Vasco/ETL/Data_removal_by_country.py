#removes item by country. Currenty, this is being done for the heroku demo since I am running out of space

from Vasco import *

#confirm country exists
ID_of_victim=db.engine.execute("select * from ent where iso_code='COM'").fetchall()[0][0]

#delete data
db.engine.execute("delete from literal where  ent_id=\'" + str(ID_of_victim) + "\' ")
#delete country
db.engine.execute("delete from ent where iso_code='COM'")

#ensure all data is removed
db.engine.execute("select * from ent where iso_code='COM'").fetchall()
db.engine.execute("select * from literal where  ent_id=\'" + str(ID_of_victim) + "\' ").fetchall()