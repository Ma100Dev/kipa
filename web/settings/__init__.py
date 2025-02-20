import os

hakemisto=os.path.normpath(os.path.dirname(__file__)) + '/..'

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DEBUG = False
TEMPLATE_DEBUG = DEBUG
RECORDING = False

ADMINS = (
     ('First Name', 'noreply@kipa.example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': hakemisto + '/../db/kipa.db',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}
DEFAULT_AUTO_FIELD='django.db.models.AutoField' 

# Cache
TAUSTALASKENTA = False # Tulokset lasketaan taustalla (Vaatii toimiakseen tomivan cachekokoonpanon)
CACHE_TULOKSET = False # Etsitaanko tuloksia cachesta
CACHE_TULOKSET_TIME = 1800 # Tuloscachen voimassaoloaika viimeisesta nayttokerrasta. [s]
#CACHE_BACKEND = 'locmem:///' # Cache system for developement
#CACHE_BACKEND = 'locmem:///' # Cache system for developement
CACHE_BACKEND = 'db://tupa_tulos_cache'
if not CACHE_TULOKSET:
        CACHE_BACKEND = 'dummy:///' # No cache in use
        TAUSTALASKENTA = False

# Local time zone for this installation.
TIME_ZONE = 'Europe/Helsinki'

# Language code for this installation.
LANGUAGE_CODE = 'fi-FI'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = hakemisto + "/media/"

STATIC_DOC_ROOT = hakemisto + "/media/"

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = ''

FILE_UPLOAD_HANDLERS= (
    "django.core.files.uploadhandler.MemoryFileUploadHandler",
    "django.core.files.uploadhandler.TemporaryFileUploadHandler",
)

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [hakemisto + '/templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
]

ROOT_URLCONF = 'urls'

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'tupa',
    'django.contrib.admin',
    'django.template',
]

LOGIN_URL = ('/kipa/')
LOGIN_REDIRECT_URL = ('/kipa/')

TEST_RUNNER = ('tupa.tests.CustomTestRunner')

# Should we serve the media files through Python?
SERVE_MEDIA = DEBUG

try:
  from .local import *
except ImportError:
  pass

try:
  from .docker import *
except ImportError:
  pass
