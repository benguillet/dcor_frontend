#!/usr/bin/python
# HiPerCic Project / St. Olaf College / Computer Science Dept.
##################################################################################################
# docGen/main.py
# Created 7/19/2011
# The main function for the docGen application -- parses arguments and generates documentation.
##################################################################################################
__author__ = "Chris Cornelius"
__version__ = "0.1.0"
__status__ = "Development"

import sys
import os

# local imports - from package src
from src import *

def usage():
	""" Prints the usage information for the program to standard error """
	import sys
		
	sys.stderr.write("\nUsage: docGen SOURCEPATH [options]\n")
	sys.stderr.write("Writes documentation for the module indicated by SOURCEPATH to html files.\n\n")
	sys.stderr.write("Options:   -d DEST     Specifies the destination directory to which the\n")
	sys.stderr.write("                           HTML files will be written.\n")
	sys.stderr.write("           -J PROJECT  Specifies PROJECT as the path to a Django project to\n")
	sys.stderr.write("                           use as context for this operation.\n")
	sys.stderr.write("           -U DEST     Specifies the destination directory to which the\n")
	sys.stderr.write("                           Django URL configuration file will be written.\n")
	sys.stderr.write("                           Defaults to the top-level project directory.\n")
	sys.stderr.write("           -P PATH     Adds PATH to the python environment variables for\n")
	sys.stderr.write("                           this search.  Useful when some modules aren't\n")
	sys.stderr.write("                           on the default path.\n")
	sys.stderr.write("           -E MODULE   A module to be excluded from the documentation process.\n")
	sys.stderr.write("                           A good tool for avoiding modules that must be\n")
	sys.stderr.write("                           imported only from a certain context.\n")
	sys.stderr.write("           --help      Display this help page and exit.\n")
	sys.stderr.write("\n")



def showhelp():
	""" Display help for the program """
	usage()



def main(argumentList):
	""" The main function for the program.  Checks args, calls functions, etc.
	"""
	initialPath = os.getcwd()

	### check for illegal argument combinations ###
	if len(argumentList) <= 1: 
		usage()
		sys.exit(-1)
		
	# set the default values for the variables involved
	excluded_modules = ["apiUrls"]
	pyPath = None
	destinationPath = os.path.abspath(os.getcwd()+"/templates/api/")

	# for operation in Django mode
	DJpath = None
	urlconfPath = None

	# the first argument MUST be the sourcepath or "--help"
	if argumentList[1] == "--help":  # print help and exit
		showhelp()
		exit(0)

	sourcePath = os.path.abspath(str(argumentList[1]))
	if not os.path.exists(sourcePath):
		sys.stderr.write("Error: Cannot find python module " + sourcePath + "\n")
		sys.exit(-10)
		
	# assert: sourcePath is either a directory or a file
		
	length = len(argumentList)
	i = 2
	while i < length:
		arg = argumentList[i]
		
		if arg == "-d":  # process the destination path...
			i += 1 # advance to next arg

			# Try to get that directory as destination
			try:
				destP = os.path.abspath(argumentList[i])
			except IndexError: continue # failure to index is silent

			if not os.path.isdir(destP):
				sys.stderr.write("Error: Cannot find doc destination directory " + destP + "\n")
				sys.exit(-10)
			# assert: destP holds the proper destination path	
			destinationPath = destP
				

		if arg == "-J":  # process Django set-up..
			i += 1 # advance to next arg
			
			# Try to get that directory as Django path
			try:
				djangoP = os.path.abspath(argumentList[i])
			except IndexError:
				# we couldn't load a module, so try to use the current directory
				djangoP = os.path.abspath(".")
				
			
			if not os.path.isdir(djangoP):
				sys.stderr.write("Error: Cannot find django package " + djangoP + "\n")
				sys.exit(-10)
			 # assert: destP holds the proper destination path	
			DJpath = djangoP
			
		if arg == "-E":  # exclude a module
			i += 1 # advance to next arg
			
			 # add the arg to the list of excluded modules
			try:
				excluded_modules.append(argumentList[i])
			except IndexError: continue # failure to index is silent
			

		if arg == "-U":  # the URLconfig destination
			i += 1 # advance to the next arg
			
			try:
				urlconfPath = os.path.abspath(argumentList[i])
			except IndexError: continue # failure to access this arg is silent
		
		if arg == "-P": # add to the path
			i+=1
			
			try:
				pyPath = os.path.abspath(argumentList[i])
			except IndexError: continue # fail silently

		if arg == "--help":  # print help and exit
			showhelp()
			exit(0)


		# end of arg-processing loop... next arg, please
		i += 1
	

	if not os.path.isdir(destinationPath):
		sys.stderr.write("Error: Cannot find doc destination directory:\n\t" + destinationPath + "\n")
		sys.exit(-10)

#	print "sourcePath = " + str(sourcePath)
#	print "destinationPath = " + str(destinationPath)
#	print "pythonPath = " + str(pyPath)
#	print "Excluded Modules = " + str(excluded_modules)
#	print "Django Project Path = " + str(DJpath)
#	print "Urlconfig destination = " + str(urlconfPath)

	# set up Django mode if we'll be using it
	if DJpath != None:
		core.setUpDjango(DJpath)

	# write out the documentation
	writtenFiles = core.processModule(sourcePath, destinationPath, pyPath, excluded_modules)
	
	# write out the url config file if we're using Django
	if DJpath != None:
		if urlconfPath == None:  # if a destination wasn't specified, choose this directory
			core.writeDjangoUrlConfig(writtenFiles,initialPath)
		else:
			core.writeDjangoUrlConfig(writtenFiles,urlconfPath)
		
	# change back to the original working directory
	os.chdir(initialPath)

# make sure we only run the program if this file has been run as an executable
if __name__ == "__main__":
	main(sys.argv)

else:
	pass

##################################################################################################

