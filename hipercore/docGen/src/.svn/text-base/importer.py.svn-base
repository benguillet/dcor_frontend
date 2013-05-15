# HiPerCic Project / St. Olaf College / Computer Science Dept.
##################################################################################################
# docGen/importer.py
# Created 7/19/2011
##################################################################################################
__author__ = "Chris Cornelius"
__version__ = "0.1.0"
__status__ = "Development"

import imp

import out




def importModule(modStr, Path=None, moduleStack=""):
    """  A method to load a given module by recursively following the complete path down to import the module.
         @input modStr - The full name of the module to import, ie. "hipercic.hipercore.beanstalk.jack"
         @input Path - The searchpath for the top-level of the module we'll be importing.  Defaults to None, and that's generally okay.
         @input moduleStack - The set of module names to apply to the head of the final module that is imported.
                For example, importing module "hipercore.admin" with moduleStack of "johnny" will result in the module object named "johnny.hipercore.admin" Defaults to "".
    """
    try:
        modName, remainder = modStr.split('.', 1) # disconnnect the first element from the python module path were were passed.
    except ValueError as e:  # we couldn't split off the first module - must be the last one in the list
        modName = modStr
        remainder = ""    

    # terminal case - the desired module is given by modName
    if remainder == "":
        # import the module given by modName, and return the reference to it
        f,p,d = imp.find_module(modName, Path)
        finalModule = imp.load_module(moduleStack+modName,f,p,d)
        
        return finalModule
        
    # intermediate case - we must import modName in order to get to the module we really want
    else:
        # find the intermediate module
        if Path == None:
            f,p,d = imp.find_module(modName)
        else:
            f,p,d = imp.find_module(modName, Path)

        M = imp.load_module(modName,f,p,d) # load the intermediate module
        
        # add the name of the module we loaded onto the module stack
        moduleStack = moduleStack + modName + "."
        
        return importModule(remainder, M.__path__, moduleStack) # recur, using the module we just imported as the source for the path
        
    



