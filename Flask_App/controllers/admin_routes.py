__author__ = 'lachlan'

from Flask_App import admin
from Flask_App import db_session
from flask.ext.admin.contrib.sqla import ModelView
from Flask_App.models.db_models import Todo, Users


# Add model views to Admin interface
admin.add_view(ModelView(Todo, db_session))
admin.add_view(ModelView(Users, db_session))

