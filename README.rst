Flask App
=========

Deploying Locally
-----------------
* To get started create a virtualenv and install everything in requirements.txt
* Add environment variables to your environment (necessary environment variables are defined in settings.py)
* Initialise the database by running init_db.py in the scripts folder.
* Run the app locally by running run_flask_app.py in the scripts folder.

Deploying to Heroku
-------------------
Install the heroku toolbelt and run the following commands from within your project folder:
 * 'heroku login' - Logs you into your heroku account
 * 'heroku create' - Create an app with APP_NAME
 * 'heroku git:remote -a APP_NAME' - Adds the correct git remote for dploying to heroku
 * 'heroku addons:create heroku-postgresql:hobby-dev' - Adds a PostgreSQL database to your app
 * 'heroku config:set STORMPATH_API_KEY_ID=xxx' / 'heroku config:set STORMPATH_API_KEY_SECRET=yyy' - Adds your environment variables
 * 'git push heroku master' - Push your app to heroku with git
 * 'heroku run init' - Runs the init_db.py script to configure your database

If you need to change your database schema you can drop all tables using
 * 'heroku pg:reset DATABASE_URL'