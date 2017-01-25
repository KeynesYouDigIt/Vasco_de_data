#removes item by country. Currenty, this is being done for the heroku demo since I am running out of space
############# untested
from Vasco import app, db

print 'You are currently working on the database %s' % db.engine.url.database
print 'make sure that name is the name of the database you intend to work on!'
target_iso = raw_input('Please provide the ISO code for the country you would like to remove from this database')

def delete(country_iso_code):
	#confirm country exists
	ID_of_victim=db.engine.execute("select * from ent where iso_code=\'" + str(country_iso_code)+ "\' ").fetchall()[0][0]
	if ID_of_victim:
		db.engine.execute("delete from literal where  ent_id=\'" + str(ID_of_victim) + "\' ")
		db.engine.execute("delete from ent where iso_code=\'" + str(country_iso_code)+ "\' ")
		#ensure all data is removed
		search_for_deleted_country=db.engine.execute("select * from ent where iso_code=\'" + str(country_iso_code)+ "\' ").fetchall()
		search_for_deleted_country_data=db.engine.execute("select * from literal where  ent_id=\'" + str(ID_of_victim) + "\' ").fetchall()
		if search_for_deleted_country or search_for_deleted_country_data:
			print 'deletion did not include %s or %s ' % (search_for_deleted_country, search_for_deleted_country_data)
		else:
			print 'Deletion of %s successful!' % country_iso_code
	else:
		print 'country not found in the database. the entry is either misspelled or was already deleted.'

delete(target_iso)