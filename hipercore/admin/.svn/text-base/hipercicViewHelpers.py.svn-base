from django.utils.text import capfirst
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy, ugettext as _
from hipercic.apps.appConfig import ACTIVE_APPS
from hipercic.hipercore.admin.adminConfig import Admin_apps, Admin_appNavBar
#from hipercic.hipercore.admin.sites import index
from django.http import Http404
import logging


def getGroupsOnApp(app):
	""" Returns a list of group ids which have access to the given app.
        NOTE: the use the spelling and capitalizations located in ACTIVE_APPS in appConfig.py
	"""
	pass

def getUsersInGroup(gid):
	""" Returns a list of all the user IDs in a group.
	"""
	pass


def getCurrentUserId(request):
	""" Decodes the user from the given request object and returns the user's id.
	"""
	return request.user.id


def getCurrentUserName(request):
	""" Decodes the user from the given request object and returns the user's name.
	"""
	return request.user.username



def getUserName(userId):
	""" Gets the name of the Hipercic user indicated by userId.  If the user does not exist, returns None.
	"""
	from hipercic.hipercore.authenticore.models import User  # import the User model to elp us

	if userId == -1: # a very special case :)
		return "User -1"
	try:
 		u_obj = User.objects.get(id__exact=userId)
		return u_obj.username

	except Exception: # fail silently
		return None
	

def getUserLevel(userId, app):
    """Gets the hipercore permission level of a user.
        Returns:
            None -- no user was found with that Id
            1 = Normal -- if the user has access to the given app
            2 = Manager -- if the user is a manager for the given app
            3 = Admin -- this is self explanatory, give this person permission to everything
        NOTE: the use the spelling and capitalizations located in ACTIVE_APPS in appConfig.py
    """
    from hipercic.hipercore.authenticore.models import User
    try:
        u_obj = User.objects.get(id__exact=userId)
        if u_obj.is_admin: #user is admin, allow access to everything
            return 3
        elif u_obj.is_app_manager: #user is an app manager for some app
            for managedapp in u_obj.apps_managed:
                if app == managedapp.name:
                    return 2
            #assert: user is not a manager for this app
            #check for base level access to the app
            for apps in u_obj.apps:
                if app == apps.name:
                    return 1
            #assert: user has no permissions to this appp      
            return None
        else:
            #assert: the user is not an admin or manager
            for apps in u_obj.apps:
                if app == apps.name:
                    return 1
            return None
    except Exception:
        return None
	
	
def getUserIdByName(userName):
	""" Returns the user id associated with a given user name.  If the user does not exist, returns None.
	"""

	from hipercic.hipercore.authenticore.models import User  # import the User model to help us

	try:
 		u_obj = User.objects.get(username__exact=userName)
		return u_obj.id

	except Exception: # fail silently
		return None
	
	
	
def userHasPermissionOnApp(userId, appName):
	""" Returns true if the given user has permission to app appName, returns false otherwise.
	"""
	
	from hipercic.hipercore.authenticore.models import User, App
	
	try:
		u_obj = User.objects.get(id__exact=userId) # get the User object specified
		app = App.objects.get(name__exact=appName) # get the App object specified
		# TODO: fix this!!! doesn't find app!

		if app in u_obj.apps.all():
			return True
		else:
			return False
		

	except Exception as e: # fail safe
		print "Error getting app/user relation: " + str(e) # TODO: remove this line once this method works!
		return False




class NavigationBar:

    def generateAppNavBar(self, request, app):
        """This will generate the app nav bar, like the title says.  The app nav bar is the second navigation benesthe the 
            nav bar, under the title.  TODO: explain this better
            
        """
        #TODO check permissions for which pages can be linked to for a user
        app_list= []
        if app in [x['text'] for x in Admin_apps]: # checks if the current_app is within the Admin_apps
            app_list = Admin_appNavBar
        else:
            navbar = __import__('hipercic.apps.'+app+'.navbar', globals(), locals(), ['appNavList'], -1)
            app_list = navbar.appNavList
        
        context ={'app_nav_list': app_list }
        return context
    
    def generateWelcome(self, request):
        return {'user':request.user}
    
    def generateNavBar(self, request, current_app="authenticore", root_path='/', items=[]):
        """This is the code that should be used by any view to generate the navigation bar.  
           This should also handle the permissions simply by checking if the current_app is part of the permissions list...
	   Return an error if the current_app is not part of the list with permissions this requries a change in permissions but could make thing much simplier.  
	   Need a new way to fill out the items list without the register class... but how? 
	   returns a context of the nav bar which should be passed from the view to the template to be rendered... 
	   to render other information simply add it to the context...
        """ ##FINISH THIS needs proper permissions for redirects to pages the user has permissions to
        user = request.user
        currentAppIndex=0
        message=None
        app_list= []
        apps = [a for a in ACTIVE_APPS]
        context = self.generateWelcome(request)
        ## Admin_apps not a local var.
        
        
        try:
                currAppIndex = apps.index(current_app) 
                ## assert: current_app is installed with hipercic
        except:
                message="Current app is not installed"
                
        if user.has_module_perms(current_app):
                for app in apps: #apps is a list of strings
                   if user.has_module_perms(app):
                      app_list.append({'text':app, 'url': '/'+app}) #the url should link to app.home...
                for app in Admin_apps: #Note Admin_apps is a list of dictionaries...
                   if user.has_module_perms(app):
                      app_list.append(app)
            
                app_list.sort()
                
             #for the appnavbar -- dictionary of app specific links and urls to display
             #appnavbar called from this and inserted into the xcontext also
             #context returns lists of 
             #2 lists -- nav and appnav rendered in the display... format them differently when it comes to the template
             #title of the page should be part of the app view
             #root path... users default app? What is the purpose of the root path?

                context.update({
                     'title': _('Application Overview'),
                     'message': message,
                     'app_list': app_list,
                     'root_path': root_path,
                     'current_app_model': current_app,
                    })   
                if items == []: #app developer chose not to supply a list of items
                    context.update(self.generateAppNavBar(request, current_app)) 
                else: 
                    context.update({'app_nav_list': items})     
        else:
                message = "Just login, Chris! (Error from NavigationBar)"
                context ={'message': message,}
                #redirect
                #raise Http404 #TODO this needs to be changed to something else... The idea is to 
                            # check the perms for the current app here when the nav bar is generated
                            # rather than in every view... this should also be true for the links listed in the appNavBar
        
	# add some important hipercic versioning information to the context
	import os
	context.update({'HIPERCIC_VERSION': os.environ['HIPERCIC_VERSION'],
			'HIPERCIC_VERSION_TEXT': os.environ['HIPERCIC_VERSION_TEXT'] })

        return context


class HipercicLogger(logging.Logger):
	''' integrates logging into hipercic functionality'''

	def __init__(self,module, filename=None):
		'''takes two variables, module, which should be set to __name__ at all times, and filename, which is the file you wish to have everything you do logged to. if you don't wish to log anything beyond the global hipercic log, or wish to personnally handle logging, don't provide a filepath. to write to the logger call .debug, .info, .warning, .error, or .critical. (in an exception, you may also call .exception), depending on the importance of the message'''
		logging.Logger.__init__(self,module)
		self.setLevel(logging.DEBUG)
		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		if not filename == None:
			localHandler = logging.FileHandler("logs/"+filename)
			localHandler.setFormatter(formatter)
			self.addHandler(localHandler)
		fullHandler = logging.FileHandler("logs/HipercicFull.log")
		fullHandler.setLevel(logging.DEBUG)
		fullHandler.setFormatter(formatter)
		self.addHandler(fullHandler)
		errorHandler = logging.FileHandler("logs/HipercicError.log")
		errorHandler.setLevel(logging.ERROR)
		errorHandler.setFormatter(formatter)
		self.addHandler(errorHandler)
		errorstreamHandler = logging.StreamHandler()
		errorstreamHandler.setLevel(logging.ERROR)
		errorstreamHandler.setFormatter(formatter)
		self.addHandler(errorstreamHandler)
