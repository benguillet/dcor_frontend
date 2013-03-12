# HiPerCic Project / St. Olaf College / Computer Science Dept.
##################################################################################################
# docGen/out.py
# Created 7/19/2011
##################################################################################################
__author__ = "Chris Cornelius"
__version__ = "0.1.0"
__status__ = "Development"


import sys, datetime

# global var to determine debug mode
DBPRINT_DEBUG_MODE = False

# the short name of this application
SHORT_NAME = 'docGen'

# helper function to print a message as a "log" entry
# allows printing to a separate log file really easily... just put that stream name in
def log(string, err=False, nl=True, stream=sys.stdout, errstream=sys.stderr):
    if err:
        errstream.write(SHORT_NAME+": Error: " + string + "\n")
    elif err:
        errstream.write(SHORT_NAME+": " + string)
        if nl:
            errstream.write("\n")
    else:
        stream.write(SHORT_NAME+": " + string)
        if nl:
            stream.write("\n")




# helper function to aid printing of debug and error information
def debugPrint(string,err=False, nl=True, force_print=False):
    
    if DBPRINT_DEBUG_MODE | force_print:
        sys.stdout.write("docGen: " + string)
        if nl: sys.stdout.write("\n")
        sys.stdout.flush()
        
    if err:
        sys.stderr.write("docGen: Error: " + string)
        if nl: sys.stderr.write("\n")
        sys.stderr.flush()

# helper function to set DBPRINT_DEBUG_MODE
def setDebugMode(debug):
	DBPRINT_DEBUG_MODE = debug




# helper function to sanitize names by removing - and . characters
def cleanName(name):
    c = name.replace(".","_")
    c = c.replace("-","_")
    return c

# helper function to drop .html extension
def dropHtmlExt(name):
    return name.replace(".html","")



URLCONFIG_HEADER = "# URLconfig and simple views functions generated by docGen script.\n"
URLCONFIG_INCLUDES = "from django.conf.urls.defaults import *\nfrom django.shortcuts import render_to_response\nfrom django.template import Template, Context\nfrom django.http import HttpResponse\n"


def generateUrlPatterns(filenames, templatePath, defaultContext="{}"):
    """ Creates a string representing the Django urls.py file holding links to all the files indicated.
        @input filenames - a list of strings representing the files to include in the urlconfig.
        @input templatePath - the path that should be applied to the template locator to help find our files.
        @input defaultContext - the context that should, by default, be passed to each of the templates in the view functions.
        @return - the whole file, in string form.
    """
    import datetime
    
    output = "" # the string where we'll store our output
    
    # write the header information and the included files
    output += URLCONFIG_HEADER
    output += "# Created " + datetime.datetime.today().ctime() + "\n"
    output += "\n"
    output += URLCONFIG_INCLUDES
    output += "\n"
    
    # write a list of all files in this urlconfig, as tuples of (displayName, href)
    output += "# A list of items to display in the index, as tuples of (displayName, href).\n"
    output += "index_list = [\n"
    for F in filenames:
        output+= "\t('" + dropHtmlExt(F) + "', '" + F + "'), \n"
    output += "\t]\n"
    
    
    # write view functions for all the files
    for F in filenames:
        cname = cleanName(F)
        output += "def " + cname + "(request):\n"
        output += "\treturn render_to_response(\"" + templatePath + F + "\", " + defaultContext + ")\n\n"
        
    # write the index page's view function
    output += "def index(request):\n"
	
    # get today's date and time as a string
    d = datetime.datetime.today()
    datestring = d.strftime("%a, %b %d %Y, %H:%I%p")
    output += "\treturn render_to_response(\""+templatePath+"index.html\",{'index_list':index_list, 'title':'Pydoc API', 'updatedDate':\"" + datestring + "\"})\n\n"
    
    
    # write the urlpatterns object
    c = 0

    output += "urlpatterns = patterns('',\n" # open the urlpatterns function

    for F in filenames:
        if c > 200: # we've printed close to our maximum for one urlpatterns call
            output += "\t)\n"
            output += "urlpatterns += patterns('',\n"
            c = 0

        # write the urlconfig entry
        output += "\t(r'^" + F + "$', " + cleanName(F) + "), \n"
        c += 1

    output += "\t(r'^$',index)\n" # write an index router
    output += "\t)\n" # close the urlpatterns tuple
    
    return output