# Vasco de data
A flask app designed for the exploration (fast retrieval and cleaning) of public data.
Working with this code to make your own cleaning and sythesizing data tool should be doable with a basic knowledge of python flask.

A special thanks to *Blazing DB* for the inspiration to start this
http://blazingdb.com/

As of now, the data base is populated via a public data API drawing from the UN and World Bank data sources that extracts, standardizes, and stores public data. these procs are stored in Vasco/ETL. I am hard at work making these scripts managable and useable so any user can retool this site to accept their data with basic python knowledge.

Check out the demo on heroku here - https://vasco-de-data.herokuapp.com/index

email me if you are interested in hacking on this or need more info at vince.buscarello@gmail.com. 
Below are some initial tips if you are interested in getting started 

* As of 7/24, as the ETL tools are built to work by running them in the command line. 
They will use the database name set in the connection string to alert the user which database is being worked on. So if you build your own development or deployment databases, be sure and note the database name. This is helpful for connecting new datasources, working with test data, and deletions when experiments go wrong or the database begins to run out of space.