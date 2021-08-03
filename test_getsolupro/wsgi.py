"""import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_getsolupro.settings')

application = get_wsgi_application()
"""

import os, sys
from django.core.wsgi import get_wsgi_application
from test_getsolupro import settings

sys.path.append(f"{os.path.join(settings.BASE_DIR, 'fichiers_statiques')}")

#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_getsolupro.settings')

os.environ['DJANGO_SETTINGS_MODULE'] = 'test_getsolupro.settings'

application = get_wsgi_application()

