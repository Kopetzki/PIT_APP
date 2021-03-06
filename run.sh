#!/bin/bash
#
# By default the db.sqlite3 database file is created in the
# site-packages folder of your Python distribution. To have it be
# created in a different folder use the DATABASE_NAME environment
# variable. For example the following commands:
#
# DATABASE_NAME="./db.sqlite3" ./run.sh
#
# will create the the sqlite file in whatever directory you call run.sh
# from, or use a prexisting file if already exists there.

pip3 install django-pit-survey -U
pit_init
pit_run
