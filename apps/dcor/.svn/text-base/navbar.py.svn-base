# HiPerCic Project / St. Olaf College / Computer Science Dept.
###################################################################################
# apps/dcor/navbar.py
# Created INSERT_DATE
# Holds configuration options for the in-app navbar at the top of the page
###################################################################################

# This list holds the links visible in the navigation bar of this app.
# Fill in a list of dictionaries formatted as follows:
# {'text':'TEXT TO DISPLAY', 'url':'LINK TO FOLLOW'}
appNavList = [{'text':'put links here!', 'url':'.'},
	      {'text':'google!', 'url':'www.google.com'} ]



# Notes on rendering a navigation bar:
# In each view function, start with a new NavigationBar object:
#        navbar = NavigationBar()
# Then make sure to assign the navbars content in the context you are going to render, either by initializing the context with it:
#        context = navbar.generateNavBar(request, current_app='dcor')
# Or by including it later:
#	 context.update(navbar.generateNavBar(request, current_app='dcor')
# You can also customize what is displayed in the nav bar by using the items[] argument:
#	 navbar.generateNavBar(request, current_app='dcor', items = appNavList2)
# Finally, you'll render the context to your template and return the HTML generated:
#        return render_to_response('TEMPLATE_NAME', context)
