# Django settings for sharider project.
import os
DEBUG = True
TEMPLATE_DEBUG = True

INSTALL_DIR = os.path.dirname(__file__) + "/"

SEGMENT_DIR = INSTALL_DIR + 'segments/'


#
# Maybe this should all go in a DB
#
MARKER_TYPE_ERROR = 0
MARKER_TYPE_RIDER = 1
MARKER_TYPE_BIKESHOP = 2
MARKER_TYPE_GHOST_BIKE = 3
MARKER_TYPE_BIKE_RACK = 4
MARKER_TYPE_CAUTION = 5
MARKER_TYPE_HOME = 6
MARKER_TYPE_MEETUP_SPOT=7

# Bike Rack, Scary Spot, Ghost Bike
MARKER_TYPES = ( (MARKER_TYPE_ERROR,"Error"),
                 (MARKER_TYPE_RIDER, "Rider"), 
                 (MARKER_TYPE_BIKESHOP, "Bike Shop"),
                 (MARKER_TYPE_GHOST_BIKE, "Ghost Bike"),
                 (MARKER_TYPE_BIKE_RACK, "Bike Rack"),
                 (MARKER_TYPE_CAUTION, "Danger Spot"),
                 (MARKER_TYPE_HOME, "Home"),
                 (MARKER_TYPE_MEETUP_SPOT, "Meetup Spot"),
                 )

EDITIABLE_MARKER_TYPES =  (
                 (MARKER_TYPE_BIKE_RACK, "Bike Rack"),
                 (MARKER_TYPE_BIKESHOP, "Bike Shop"),
                 (MARKER_TYPE_MEETUP_SPOT, "Meetup Spot"),
                 (MARKER_TYPE_CAUTION, "Danger Spot"),
                 (MARKER_TYPE_GHOST_BIKE, "Ghost Bike"),
                 )

MARKER_INFO = {
    #
    # icon - image file to use in map display
    # option_name - Text for on screen UI (show/hide) etc
    # option_tag - Name to use for code stuff
    # show - Should the page default to showing these as on
    # enabled - Should these show up in the UI at all for this page
    #
    MARKER_TYPE_ERROR : dict(icon='marker_error.png',option_tag = 'errors' ,option_name ='Errors', show = True , enabled = False),
    MARKER_TYPE_RIDER : dict(icon='marker_rider.png', option_tag = 'riders', option_name ='Riders', show = True, enabled = True),
    MARKER_TYPE_BIKESHOP : dict(icon='marker_bikestore.png',  option_tag ='bikeshops', option_name ='Bike Shops', show = True, enabled =True),
    MARKER_TYPE_GHOST_BIKE : dict(icon='marker_ghostbike.png', option_tag = 'ghostbikes' ,option_name ='Ghost Bikes', show = True, enabled = True),
    MARKER_TYPE_MEETUP_SPOT : dict(icon='marker_meetup.png', option_tag = 'meetups' ,option_name ='Meetup Spots', show = True, enabled = True),

    MARKER_TYPE_BIKE_RACK : dict(icon='marker_bikerack.png', option_tag = 'bikeracks', option_name ='Bike Racks', show = True, enabled = True),
    MARKER_TYPE_CAUTION: dict(icon='marker_caution.png', option_tag= 'cautionspots', option_name ='Caution Spots', show = True, enabled = True),
    MARKER_TYPE_HOME: dict(icon='marker_unknown.png', option_tag= 'home', option_name ='Home', show = True, enabled = False)
}



ADMINS = (
    ('Brice Tebbs', 'brice@bricetebbs.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default' : {
            'ENGINE' : 'django.db.backends.mysql',        # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME' : 'sharider',           # Or path to database file if using sqlite3.
            'USER' :  'django',          # Not used with sqlite3.
            'PASSWORD' : 'django',      # Not used with sqlite3.
            'HOST'  : '',                 # Set to empty string for localhost. Not used with sqlite3.
            'PORT'  : '',     # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''
STATIC_ROOT = ''
STATIC_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Additional locations of static files
STATICFILES_DIRS = (
    INSTALL_DIR + 'static_files',
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'njw2y^+3@zp4cjya8%3l@yncfck506!h*y-syassh=t&a_1*jc'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
# csrf ?
    'django.middleware.transaction.TransactionMiddleware',
)

LOGIN_URL= '/signup/login/'
LOGOUT_URL= '/signup/logout/'
LOGIN_REDIRECT_URL = '/sharider/rider/'

ROOT_URLCONF = 'sharider.urls'

AUTH_PROFILE_MODULE = 'srmain.RiderProfile'

AUTHENTICATION_BACKENDS  = ('signup.views.SignupBackEnd',)


TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    INSTALL_DIR +'templates',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
     'sharider.context_processors.settings',
)
    

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    
    'sharider.srmain',
    'sharider.signup',

)

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'user@example.com'
EMAIL_HOST_PASSWORD ='password'
EMAIL_SUBJECT_PREFIX = '[SpokeTransit.com]'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
SERVER_EMAIL = DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

MY_LOG_FILENAME = INSTALL_DIR + 'logs/sharider.log'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },

        'rotating_file':
        {
            'level' : 'DEBUG',
            'formatter': 'verbose',
            'class' : 'logging.handlers.TimedRotatingFileHandler',
            'filename' :  MY_LOG_FILENAME,
            'when' : 'midnight',
            'interval' : 1,
            'backupCount' : 7,
        },
    },
    'loggers': {
        'django': {
            'handlers':['null'],
            'propagate': True,
            'level':'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'sharider': {
            'handlers': ['rotating_file'],
            'level': 'DEBUG',
        },
         'signup': {
            'handlers': ['rotating_file'],
            'level': 'DEBUG',
        }
    }
}


from settings_local import *