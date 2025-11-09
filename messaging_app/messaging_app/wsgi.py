import os
import sys

path = '/home/MaryKaranja/alx-backend-python/messaging_app'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'messaging_app.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

