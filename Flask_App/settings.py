import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = os.urandom(24)

DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///{0}'.format(os.path.join(ROOT_DIR, 'sqlite_data.db')))

STORMPATH_API_KEY_ID = os.environ.get('STORMPATH_API_KEY_ID')
STORMPATH_API_KEY_SECRET = os.environ.get('STORMPATH_API_KEY_SECRET')

FRIENDLY_SERVER_ERROR = 'This is embarrassing but we are having some server' \
                        ' issues. We are working to resolve it now. Check back soon.'