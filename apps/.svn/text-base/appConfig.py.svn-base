# HiPerCic Project / St. Olaf College / Computer Science Dept.
###################################################################################
# hipercic/apps/appConfig.py
# Created 6/11 Chris Cornelius
# Holds code for configuring and managing the apps in the project
###################################################################################

### TOP LEVEL ###
### To install an app, add its name into this tuple ###
ACTIVE_APPS = ( 'dcor', )

### IMPORTS ###
from django.conf.urls.defaults import patterns, include



### CODE ### 

# generate the URL patterns for all apps... for the global urlconfig file
def getAppURLPatterns():
    patternList = patterns('',)
    
    for app in ACTIVE_APPS:
        # construct the path to the app's urls document and add to patternList
        patternList += patterns('', (r'^'+app+'/', include('hipercic.apps.'+app+'.urls')), ) 

    return patternList # return the list we made




# function to generate the DATABASE_ROUTERS... in list form (will be frozen into a tuple in settings.py
def getDatabaseRouters():
	dbRouters = [];
	
	for app in ACTIVE_APPS:
		# construct the name of the app's dbConfig databaseRouter
		dbRouters.append('hipercic.apps.' + app + '.dbConfig.DatabaseRouter')
		
	return dbRouters


# generate a dictionary with database information for each app... incorporate as "DATABASES" in settings.py
def getAppDatabases():
	databases = {} # TODO: find a way to let this fail elegantly if there are no imports

	for app in ACTIVE_APPS:
            try:
                # use the imp module to import the app we're looking for, followed by the dbConfig file
                import imp
                f,p,d = imp.find_module(app)  # find and load the app's module
                P = imp.load_module(app,f,p,d)
                f1,p1,d1 = imp.find_module("dbConfig",P.__path__)  # find and load the dbConfig module for the app
                DBCF = imp.load_module(app+".dbConfig",f1,p1,d1)
                
                dbName, dbConfigDict = DBCF.getDatabaseConfiguration()  # Get the appropriate information from the config file
                
                if dbName == '': # for the case when there's no database
                    continue     # just skip over this entry

                databases[dbName] = dbConfigDict # append to the dictionary we're building

            except Exception as ex:
                print("An error occured while importing module " + app + ".dbConfig.  Error: " + str(ex))
        
        # return our fully built database dictionary
        return databases




# generate a tuple of all the packages for our apps... for INSTALLED_APPS in settings.py
def getAppPackages():
	allPacks = ()
	
	for app in ACTIVE_APPS:
		# construct package name, append
		allPacks += ('hipercic.apps.'+app,)


	return allPacks
