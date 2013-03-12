# HiPerCic Project / St. Olaf College / Computer Science Dept.
###################################################################################
# docGen/doc.py
# Created 7/19/2011
# Holds methods that help pydoc process modules
###################################################################################
__author__ = "Chris Cornelius"
__version__ = "0.1.0"
__status__ = "Development"

import os
import sys
import pydoc

import out
from importer import importModule

def documentModules(moduleNames, exclude=[], destination=".", Path=None):
    """ Generates pydoc documentation for each module name given and outputs the HTML files into the destination directory.
        @input moduleNames - a list of names for the modules to document.
        @input exclude - a list of module and package names that should NOT be documented
        @input destination - a string indicating the directory path where the documentation HTML should be written.  Defaults to "."
        @input Path - any specific PATH to use?
        @return - a list of the filenames of all html files which were written.
    """

    # update the path variable with any special info
    sys.path.append(Path)
    
    writtenFiles = [] # list for all files that have been written
    
    # change to the appropriate directory
    os.chdir(destination)
    
    # loop through all the module names we were given
    for modName in moduleNames:
        
        # filter out any excluded modules
        for x in exclude:
            if modName.find(x) != -1:
                out.log("Skipping module " + modName)
                modName = ""

        # filter out bogus module names
        if modName == "":
            continue
    

        # import the module and write out the documentation for it.
        try:
            M = importModule(modName, Path=Path)

	    out.log("",nl=False)

            pydoc.writedoc(M)

            writtenFiles.append(modName+".html")
        except ImportError as e: # print error msg and proceed to next object
            out.log("Could not import module " + modName + " - " + str(e), err=True)
            continue

    return writtenFiles
    
    






def indexPythonModule(path,force_walk=False):
    """ Walks through a python module importing the whole tree
        @input path - The path to the python module in question.
        @input force_walk - Forces the function to work on directories even if they are not python modules.  TODO 7/18 - IMPLEMENT THIS FEATURE.
        @return - A list of strings, each string being the long module name of modules within the module given by path.
        Example - processPythonModule('/home/python/') => ["python.mod1", "python.mod2", "python.mod3.a", "python.mod3.b"]
    """
    
    os.chdir(path)    
    out.debugPrint("Directory is " + os.getcwd())
    
    returnList = []
    
    allFiles = os.listdir(os.getcwd())
    
    dotdot, packageName = os.path.split(path) # get the containing folder and the name of this folder

    # check to see if this directory is a python package - if not, return []    
    if not "__init__.py" in allFiles and force_walk == False:
        return []

    else: # if we are going to search this module, add its name to the returnList
        returnList.append(packageName)
    
    for F in allFiles:

        # ignore invisble files
        if F[0] == '.':
            continue
        
        
        if os.path.isdir(os.path.abspath(F)):  
            # assert: F is a directory.  Recur on it, then add packageName to each returned 
            
            dirContents = indexPythonModule(os.path.abspath(F), force_walk)
            
            for x in dirContents:
                returnList.append(packageName + "." + x)
            
            os.chdir(path) # change back to the current directory

            continue

        else: # This is a regular file - if it's a .py file, append to the list            
            name, ext = os.path.splitext(F)

            if ext != ".py":  # check that our file is a .py file
                continue
            
            if name == "__init__": # do not process the init file
                continue

            returnList.append(packageName + "." + name)
            #print "Module " + returnList[-1]
            continue


    out.debugPrint(packageName + ": total " + str(len(returnList)) + " items.")
    return returnList





