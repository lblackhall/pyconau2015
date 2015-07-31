__author__ = 'lachlan'

from Flask_App.models.db_models import *

# import all modules here that might define models so that
# they will be registered properly on the metadata.  Otherwise
# you will have to import them first before calling init_db()
if __name__ == '__main__':
    db.create_all()