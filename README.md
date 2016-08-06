#Vasco de data
A flask app designed for the exploration (fast retrieval and cleaning) of public data.
Working with this code to make your own cleaning and sythesizing data tool should be doable with a basic knowledge of python flask.


As of now, the data base is populated via a public data API drawing from the UN and World Bank data sources that extracts, standardizes, and stores public data. these procs are stored in Vasco/ETL. I am hard at work making these scripts managable and useable so any user can retool this site to accept their data with basic python knowledge.

###Check out the demo on heroku [here](https://vasco-de-data.herokuapp.com/index)

 --------

*A special thanks to [Blazing DB](http://blazingdb.com/) for the inspiration to start this*

 --------

 --------

 --------

##Working on Vasco

Email me if you are interested in hacking on this or need more info at vince.buscarello@gmail.com. 
Below are some initial tips if you are interested in getting started 

####If you have a beginner's understanding of Flask or even Django, you shouldn't have too many issues.
* If you don't [go here](http://www.pgbovine.net/flask-python-tutorial.htm)

####Postgres is the RDBMS.
* To start, clone this repo, create a virtual enviroment. Activate it and run the usual `pip install -r requirments.txt`

* Create a postgres database and note the name, username and password and add an enviromental variable DATABASE_URL equal to postgresql://user:password@localhost:5432/DBNAME. to do this test the set command in windows and export for bash, and add these commands to the begining of the activate script in your virtual enviroment, which should not push to github with the source code.
For example, the last line of the "C:\\...path...\\venv_Vasco\\Scripts\\activate.bat" script in my virtual enviroment reads
`set "DATABASE_URL=postgresql://user:password@localhost:5432/DBNAME"`


*[Good short tutorial on this here](http://andrewtorkbaker.com/using-environment-variables-with-django-settings)*


####As of 7/24, as the ETL tools are built to work by running them in the command line. 
* They will use the database name set in the connection string to alert the user which database is being worked on. the connection is created using the enviromental variable set above. This allows your computer to store the connection to your local or the production database and set it wherever it is running.

* To start populating the data, run the procs stored in Vasco de Data\\Vasco\\ETL from a command line, starting with create_and_test_db.py

* see a full schema diagram at Vasco de Data\\archive\\diagrams\\db schema