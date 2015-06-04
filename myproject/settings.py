# Django settings for myproject project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('########################', '##############################'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'pizza_impulse_database',                      # Or path to database file if using sqlite3.
        'USER': '############',                      # Not used with sqlite3.
        'PASSWORD': '############',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'


# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '/var/www/django-apps/pizza_impulse/static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    '/var/www/django-apps/pizza_impulse/myproject/static',
    '/var/www/django-apps/pizza_impulse/myproject/static/pizza_impulse',
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
SECRET_KEY = '#######################################'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'myproject.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'myproject.wsgi.application'

TEMPLATE_DIRS = (
    '/var/www/django-apps/pizza_impulse/myproject/templates',
    '/var/www/django-apps/pizza_impulse/myproject/templates/pizza_impulse',
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'topping_preferences',
    'pizza_merchants',
    'addresses',
    'pizza_orders',
    'pizza_types',
    'time_preferences',
    'spec_pizza_sales',
    'drivers',
    'views',
    'authorizenet',
    'south',
    'twilio',
    'email_identifiers',
    'pygeocoder',
    'google_distance_matrix',
    'spec_pizza_candidate_records',
    'driver_pizza_orders',
    #'pygeocoder-1.2.5',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

ALLOWED_HOSTS = ['#######################','########################']

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
)

AUTHNET_DEBUG = True

AUTHNET_LOGIN_ID = "##################"

AUTHNET_TRANSACTION_KEY = "###################"

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = '############'
EMAIL_HOST_PASSWORD = '############'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

TWILIO_ACCOUNT_SID = "###############################"

TWILIO_AUTH_TOKEN = "###############################"

TWILIO_FROM_NUMBER = "##########"

TWILIO_DEFAULT_CALLERID = "Pizza Impulse"

#Custom settings variables begin here:

# EMAIL_RECIPIENT_CONTACT_FORM should be set to the party at Pizza Impulse
# who will be checking user messages sent in through the contact form.
EMAIL_RECIPIENT_CONTACT_FORM = "###############################"

# OUTER_EMAIL_SIGNATURE goes on the bottom of all out-going emails to users,
# and should be set to a string of HTML tags with inline styles. Don't worry
# about the hash tag in the 'color' style being interpreted as a comment on this page,
# it will still be interpreted properly.
OUTER_EMAIL_SIGNATURE = "<br><br><span style='font-family:Georgia,serif;font-style:italic;color:#111111;'>- Pizza Impulse</span>"

COMPANY_OFFICIAL_NAME = "Pizza Impulse, Inc."

PHYSICAL_ADDRESS_1 = "123 Legal Address"

PHYSICAL_ADDRESS_2 = "########################"

# SPECULATION_PIZZA_MARKET_RADIUS_MAX is the maximum number of miles from a
# primary delivery address that a merchant will search for speculation pizza
# prospects.

SPECULATION_PIZZA_MARKET_RADIUS_MAX = 10

#SPECULATION_PIZZA_VETTING_TIME is the maximum number of minutes the driver
#should be expected to wait after delivering primary pizza order.

SPECULATION_PIZZA_VETTING_TIME = 25
