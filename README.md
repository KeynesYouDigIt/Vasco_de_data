# Vasco de data
A flask app designed for the exploration (fast retrieval and cleaning) of public data.
Working with this code to make your own cleaning and sythesizing data tool should be doable with a basic knowledge of python flask.

======

======

A special thanks to *Blazing DB* for the inspiration to start this
http://blazingdb.com/As of now, the data base is populated via a public data API drawing from the UN and World Bank data sources that extracts, standardizes, and stores public data. these procs are stored in Vasco/ETL. I am hard at work making these scripts managable and useable so any user can retool this site to accept their data with basic python knowledge.

##Check out the demo on heroku here - https://vasco-de-data.herokuapp.com/index
======

Email me if you are interested in hacking on this or need more info at vince.buscarello@gmail.com. 
Below are some initial tips if you are interested in getting started 

* If you have a beginers understanding of Flask or even Django, you shouldn't have too many issues. If you are new to python web development, start with  more basic flask app.

*** To start, clone this repo, create a virtual enviroment. Activate it and run the usual `pip install -r requirments.txt`

*** Create a postgres database and note the name, username and password and add an enviromental variable DATABASE_URL equal to postgresql://user:password@localhost:5432/DBNAME. You cant use the SETX command in windows and export for bash.


* Postgres is the RDBMS.

* As of 7/24, as the ETL tools are built to work by running them in the command line. 
They will use the database name set in the connection string to alert the user which database is being worked on. So if you build your own development or deployment databases, be sure and note the database name. This is helpful for connecting new datasources, working with test data, and deletions when experiments go wrong or the database begins to run out of space.



*** the connection is created using the enviromental variable set above. This allows your computer to store the connection to your local or the production database and set it wherever it is running.

*** To start populating the data, run the procs stored in Vasco de Data\\Vasco\\ETL from a command line, starting with create_and_test_db.py

*** see a full schema diagram at
Vasco de Data\\archive\\diagrams\\db schema