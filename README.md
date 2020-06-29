# PIT App

Django app with web forms to assist with the collection of data for Point-in-Time (PIT) counts for the Annual Homeless Assessment Report (AHAR) sent to the U.S. Congress. You can view these annual reports at:
https://www.hudexchange.info/homelessness-assistance/ahar

Examples PDFs of the forms:
 - Intervew: https://files.hudexchange.info/resources/documents/Model-Interview-Based-Unsheltered-Night-of-Count-PIT-Survey.pdf
 - Observation: https://files.hudexchange.info/resources/documents/Model-Observation-Based-Unsheltered-Night-of-Count-PIT-Survey.pdf 

## Running Locally
The app can be run locally using `docker` and `docker-compose`.
There are instructions on how to install `docker`
[here](https://docs.docker.com/engine/install/ubuntu/) and
`docker-compose`
[here](https://docs.docker.com/compose/install/).
Once `docker-compose` is installed you
can run the app using the following commands:
 
 `docker-compose up --build`

This will rebuild the docker images to the latest versions, bring
up a postgres database locally, run Django migration scripts on that
database, and then finally start the Django app. The app should
now be available locally at http://127.0.0.1:8000.

## Database connection
This app uses the envdot library to retrieve the configuration needed
to point to a database to run the Django app on. By default the
database is configured to use a database brought up when run through
`docker-compose`. You must set the following environment variables
when running through any other environment to point to the proper
database:

 - `DATABASE_ENGINE`
 - `DATABASE_NAME`
 - `DATABASE_USER`
 - `DATABASE_PASSWORD`
 - `DATABASE_HOST`
 - `DATABASE_PORT` 
 
 You can set these all in a single command like so, replacing `XXX`
 with the correct value for your database:
 
`DATABASE_ENGINE=XXX DATABASE_NAME=XXX DATABASE_USER=XXX DATABASE_PASSWORD=XXX DATABASE_HOST=XXX DATABASE_PORT=XXX python3 manage.py runserver`


