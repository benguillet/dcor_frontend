# HiPerCic Project / St. Olaf College / Computer Science Dept.
##########################################################################################################################
# hipercic/settings.py
# Created 8/3/11
# Django settings module for the HiPerCiC Django front end.
# This module loads the apps/AppConfig module and incorporates all the information
#    which that module provides about the apps installed in this HiPerCiC instance.
##########################################################################################################################
import os, sys


## Set up the global HIPERCIC_VERSION constants ##
os.environ['HIPERCIC_VERSION'] = "0.8"
os.environ['HIPERCIC_VERSION_TEXT'] = "Hipercic Development Version 0.8.  Summer 2011 Development Release."
os.environ['HIPERCIC_RELEASE'] = "Hipercic Development Release 0.8"


##########################################################################################################################
## Import the appConfig module in order to access data for the apps added to this system. ################################
try:
	# change the system PATH to include the "apps" directory
	hipercic_path = os.path.dirname(__file__) # Get the path of the current file	
	lib_path = os.path.abspath(hipercic_path+'/apps/')  # build a relative path to the "apps" subfolder
	existing_path = sys.path   # save the old path value
	
	# add the new path, and import the appConfig module
	sys.path.append(lib_path)  
	import appConfig

	# copy all the data we need from appConfig into local vars
	hipercic_installed_apps = appConfig.getAppPackages()  # Get a list of currently installed apps (from appConfig.py)
	hipercic_app_database_routers = appConfig.getDatabaseRouters()  # Get a list of database routers for our apps.  Note: returns a list, not a tuple, so we can concatenate
	hipercic_app_database_configurations = appConfig.getAppDatabases()  # Get all the database configuration information for the apps.

	# revert the path to its previous state, calling remove() to make sure
	sys.path = existing_path   
	sys.path.remove(lib_path)	

except Exception as ex:
	# In the case of an error while importing the appConfig module
	# TODO: use the logging functions here!
	print("Error while loading appConfig module: " + str(ex))
	print("Aborting Django startup!")
	sys.exit(-99)
## End importing appConfig. ##


##########################################################################################################################
## Set up basic debugging and localization flags. ########################################################################

DEBUG = True                    # Return useful error pages for Django errors
TEMPLATE_DEBUG = DEBUG          # Return useful 404 pages for template errors
TIME_ZONE = 'America/Chicago'   # Time zone for the installation.  Choices: http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
LANGUAGE_CODE = 'en-us'         # Language code for this installation. All choices can be found here: http://www.i18nguy.com/unicode/language-identifiers.html
SITE_ID = 1
USE_I18N = True                 # If you set this to False, Django will make some optimizations so as not to load the internationalization machinery.
USE_L10N = True                 # If you set this to False, Django will not format dates, numbers and calendars according to the current locale

## End debugging/localization ##


##########################################################################################################################
## Set up Admin users (not much used in HiPerCiC) and other Admin stuff. #################################################
ADMINS = ( ('guillet', 'guillet@stolaf.edu'),
	)
MANAGERS = ADMINS
LOGIN_URL='/'
#LOGIN_REDIRECT_URL='/'
ADMIN_MEDIA_PREFIX = '/hipercore/admin/media/'  # URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
SECRET_KEY = 'jbchgl%o^)*z%-%f$fsp737%zct+#de78ab_7m$a@)o9p9=!ko'  # Make this unique, and don't share it with anybody.  Especially Wormtail.

AUTHENTICATION_BACKENDS = ( 'hipercic.hipercore.authenticore.backends.ModelBackend',	) 
ADMIN_FOR = ( 'hipercic.hipercore.admin', )
#BACKEND = ('hipercic.hipercore.authenticore.backends', )

## End admin code ##


##########################################################################################################################
## Set up Databases for Django's access.  Includes databases and dbconfigs from appConfig, too. ##########################

globalDatabases = {
    'default': {
	'ENGINE': 'django.db.backends.sqlite3', # 'postgresql_psycopg2' for postgreSQL (servers), or 'sqlite3' for local development
        'NAME': 'hipercore/hipercic.db',          # Or path to database file if using sqlite3.
    },
}

# Build our DATABASES dictionary out of the globals and the app databases from appConfig
DATABASES = dict( globalDatabases.items() + hipercic_app_database_configurations.items() )  

# Set up database routers, which associate the models of our apps with the app databases
DATABASE_ROUTERS = tuple( hipercic_app_database_routers )

## End database settings


##########################################################################################################################
## Set up Media, Templates, Static files, and URL configs.  ##############################################################
MEDIA_ROOT = ''  # Absolute filesystem path to the directory that will hold user-uploaded files.
MEDIA_URL = '' # URL that handles the media served from MEDIA_ROOT. Make sure to use a trailing slash if there is a path component (optional in other cases).

TEMPLATE_LOADERS = ( # List of callables that know how to import templates from various sources.
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)
TEMPLATE_CONTEXT_PROCESSORS = (  # Callables which process templates into pages - defaults are all that are needed for HiPerCiC
   'hipercic.hipercore.authenticore.context_processors.auth',
   'django.core.context_processors.static',
)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'hipercic.hipercore.authenticore.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)
TEMPLATE_DIRS = (  # places templates can be found -- not needed for Apps, because INSTALLED_APPS are searched for templates
    "hipercore/templates/",  # enables hipercore's templates -- the basis for hipercic
)

ROOT_URLCONF = 'hipercic.hipercore.urls'   # The module where the base url config for this site is found.

# Configuration for the static resources manager
STATICFILES_DIRS = ( "hipercore/static", )  # Where to look for global (non-app) static files.  INSERT_ABSOLUTE_PATH
STATIC_URL = '/static/'  # The URL that the server will provide for the static media 
#STATIC_ROOT = '???' -- this is where static files will be collected for release

## End Media, Template, Static, URLs ##


##########################################################################################################################
## Set up INSTALLED_APPS, including the apps from appConfig. #############################################################

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',  # manage staticfiles for Django 1.3 +

    # Enable the hipercic admin site found in hipercore/
    'hipercic.hipercore.authenticore',
    'hipercic.hipercore.admin',
    #'hipercic.hipercore.documentation',

    # Enable the bug-reporting package
    'hipercic.hipercore.bugs',

) + hipercic_installed_apps  # append the list of installed HiPerCiC apps that we generated at the top of the document


##########################################################################################################################
## END SETTINGS.PY #######################################################################################################
##########################################################################################################################
##########################################################################################################################
