# fullstack-catalog

Catalog app for the project 3 of the Udacity Full Stack Nanodegree. It consists of a wiki for web development ressources, that can be modified if correctly logged in using Oauth.

##Dependencies

To run, you need to have the following python module installed :
* flask
* oauth2client
* sqlalchemy
* requests

You can install all of them using pip (pip install [package-name]).

You will also need to have postgresql installed.

##How to run

You have to initialize the db first, with the command python db_setup.py. You then have to populate it using python populate_db.py.

To get the app on localhost, run the command python project.py from the root folder, and the app should run on localhost:5001.

##How the app works

Simply browse the catalog or sign in to create, edit or delete your entries.
