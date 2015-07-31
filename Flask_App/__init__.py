from Flask_App import settings
from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = settings.SECRET_KEY

# Initialise logging
import logging

defaults = {
        'level': logging.DEBUG,
        'format': "%(relativeCreated)d %(levelname)s: %(message)s"
    }
handler = logging.basicConfig(**defaults)
app.logger.addHandler(handler)


# ---Initialise extensions here---

# SQLAlchemy for easy database access
from flask.ext.sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = settings.DATABASE_URL
db = SQLAlchemy(app)
db_session = db.session

# Admin for easy access to the data in the database
from flask.ext.admin import Admin
admin = Admin(app)

# Add authentication and user management
from flask.ext.stormpath import StormpathManager
app.config['STORMPATH_API_KEY_ID'] = settings.STORMPATH_API_KEY_ID
app.config['STORMPATH_API_KEY_SECRET'] = settings.STORMPATH_API_KEY_SECRET
app.config['STORMPATH_APPLICATION'] = 'mystories'
stormpath_manager = StormpathManager(app)


# Register the endpoints for the app
from Flask_App.controllers.admin_routes import *
from Flask_App.controllers.app_routes import *
