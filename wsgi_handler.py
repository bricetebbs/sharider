import os, sys
import sys
sys.stdout = sys.stderr
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
sys.path.append('/home/nikto/sites/ride.northnitch.com/sharider/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'sharider.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
