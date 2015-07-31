__author__ = 'lachlan'

import os
import logging
from Flask_App import app

logger = logging.getLogger(__name__)

logger.info('Flask App Starting')

app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000), debug=os.environ.get('DEBUG', True))
