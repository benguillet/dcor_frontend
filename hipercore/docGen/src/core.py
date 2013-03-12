# HiPerCic Project / St. Olaf College / Computer Science Dept.
###################################################################################
# docGen/core.py
# Created 7/19/2011
# Holds functions for the main operaction of docGen 
###################################################################################
__author__ = "Chris Cornelius"
__version__ = "0.1.0"
__status__ = "Development"

import os
import sys
import pydoc

import out
import importer
import doc




def setUpDjango(djangoProjectPath, djangoSettingsModule="settings"):
	""" Sets up the django environment for a given project to help with the importing of django-related modules.
	    @input djangoProjectPath - the full directory path to the django project we'll be using.
	    @input djangoSettingsModule - the name of the python module to use as the settings for this project.  (default = "settings")
	""" 
	
	# generate the full module name for the settings module
	settingsModuleName = os.path.basename(djangoProjectPath) + "." + djangoSettingsModule
	try:
		# do all the important settings stuff 
		sys.path.append(os.path.abspath(djangoProjectPath+'/..'))
		os.environ['DJANGO_SETTINGS_MODULE'] = settingsModuleName
		from django.core.management import setup_environ
		settingsModule = importer.importModule(settingsModuleName)
		out.log("Configured PATH, loaded Django settings.")
		
		setup_environ(settingsModule)
		out.log("Set up Django Environment for project " + os.path.basename(djangoProjectPath)+".")
	except Exception as e:
		out.log("Could not set up Django environment - " + str(e), err=True)
		out.log("Is the Django settings module really called " + settingsModuleName + " ?")
		out.log("Proceeding anyway.  Many of the module imports may fail.", err=True)





def processModule(targetModule, doc_destination, pyPath=None, excluded_modules=[]):
	""" Processes a module given by a target directory path and generates documentation 
	    @input targetModule - the full path to the module to be documented.
	    @input pyPath - if the python path must be updated to help import this module, make those changes.  Defaults to the directory above the requested module.
	    @input excluded_modules - a list of strings representing modules and packages that should not be documented.
	    @return - a list of strings representing the names of the html files created in the documentation process.
	"""

	# process default values for vars that cannot be set to "None"
	if pyPath == None:
		pyPath = targetModule + "/.."


	# Map out all the modules to document
	names = doc.indexPythonModule(targetModule)	
	out.log("Found " + str(len(names)) + " modules to document in module " + str(os.path.basename(targetModule)) )

	# change to the destination directory so pydoc can do its thing
	os.chdir(doc_destination)
	out.debugPrint("Changed working directory to " + os.getcwd())
		
	
	# Generate their documentation
	sys.path.append(os.path.abspath(pyPath))
	filenames = doc.documentModules(names, exclude=excluded_modules, destination=doc_destination )
			
	out.log("Wrote documentation for " + str(len(filenames)) + " modules into directory:\n\t" + str(doc_destination))
	
	return filenames



def writeDjangoUrlConfig(filenames, urlConfig_destination, urlConfig_name="apiUrls.py", templatePrefix='api/'):
	""" Creates a Django-style URL Configuration file for all the filenames specified.
	    @input filenames - the file names to write into the urlConfig file
	    @input urlConfig_destination - the destination for the apiUrls file
	    @input urlConfig_name - urlconfig file name (default: 'apiUrls.py')
	    @input templatePrefix - In the render_to_response call, should we look in a subdirectory of the templates dir?  (default: 'api/')
	    @return - none
	""" 
	
	
	os.chdir(urlConfig_destination)
	out.debugPrint("Changed working directory to " + os.getcwd())
    
	f = open(urlConfig_name,'w')    # open the file for non-append writing
	out.log("Opened file for writing:\n\t" + os.path.abspath(f.name))

	f.write(out.generateUrlPatterns(filenames, templatePrefix)) # write the urlpatterns to the file
	
	out.log("Wrote apiUrls.py file.")
	
	# finally, close the file
	f.close()
