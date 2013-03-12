# HiPerCic Project / St. Olaf College / Computer Science Dept.
###################################################################################
# hipercic/hipercore/bugs/views.py
# Created 7/26
# Holds Django views for the bug reporting subsite
###################################################################################
from django.shortcuts import render_to_response
from django.template import Template, Context
from django.http import HttpResponse
from django.views.decorators.csrf import *
from django.core.context_processors import csrf

from hipercic.hipercore.admin.hipercicViewHelpers import NavigationBar, getUserLevel
from hipercic.hipercore.authenticore.decorators import login_required

from hipercic.hipercore.bugs import models




@login_required
def viewBugs(request):
    """ Renders a page allowing users to see all the bugs.  If user is an admin, passes along extra details to allow administration of the bugs.
    """
    if request.method != 'GET':
        return HttpResponse("TODO: 404 here.", status=404)

    nbar = NavigationBar()
    context = nbar.generateNavBar(request)
    context.update({'title':"View bug reports"})
    context.update(csrf(request))  # add cross-site request forgery protection
    context.update({'csrfTokenValue':csrf(request)['csrf_token']})  # add the token a second way
    
    # extra content will be rendered if the user is an admin
    if getUserLevel(request.user.id, "") == 3 :
        context.update({'user_is_admin':True})
        context.update({'openBugs': models.BugReport.objects.filter(active__exact=True).filter(status__exact="O").order_by('dateModified')})
        context.update({'deletedBugs': models.BugReport.objects.filter(active__exact=False)})
        context.update({'numDeletedBugs': models.BugReport.objects.filter(active__exact=False).count()})

        
    # add the list of all bugs to the context
    context.update({'allBugs': models.BugReport.objects.filter(active__exact=True)})
    context.update({'bugStati':[('O', 'Open'), ('RF','Resolved - Fixed'), ('RD','Resolved - Duplicate'), ('RI','Resolved - Invalid'),('RW','Resolved - Will Not Fix'),('C','Closed')]})    


    return render_to_response("viewBugs.html", context)
    





@login_required
def deletedBugs(request):
    """ Renders a page showing the inactive bugs... but note that the template filters so it only displays for users with proper permissions.
    """
    if request.method != 'GET':
        return HttpResponse("TODO: 404 here.", status=404)

    nbar = NavigationBar()
    context = nbar.generateNavBar(request)
    context.update({'title':"View Inactive Bugs"})
    context.update(csrf(request))  # add cross-site request forgery protection
    context.update({'csrfTokenValue':csrf(request)['csrf_token']})  # add the token a second way
    
    # extra content will be rendered if the user is an admin
    if getUserLevel(request.user.id, "") == 3 :
        context.update({'user_is_admin':True})
        
    # add the list of all bugs to the context -- inactive bugs only!
    context.update({'allBugs': models.BugReport.objects.filter(active__exact=False)})
    
    return render_to_response("deletedBugs.html", context)






@login_required
def bugDetails(request):
    """ Displays the details for a bug, with the bug id indicated by the GET data.
    """

    if request.method == 'GET':  # we should render the page
        try:
            nbar = NavigationBar()
            context = nbar.generateNavBar(request)
            context.update({'title':"Bug Details"}) # the basic title
            context.update(csrf(request))  # add cross-site request forgery protection
            context.update({'csrfTokenValue':csrf(request)['csrf_token']})  # add the token a second way
            
            if getUserLevel(request.user.id, ""):
                context.update({'user_is_admin':True})
                
            # try to get the bug to render
                
            theBug = models.BugReport.objects.get(id__exact=int(request.GET['id']))
            context.update({'bug': theBug})
            
            if not theBug.status == "O":
                context.update({'resolveMessageDefault': theBug.resolvedText})
            
            context.update({'title':"Bug " + str(theBug.id) + " - " + theBug.summary}) # change the title
            return render_to_response("bug.html", context)

        except Exception as e:
            return HttpResponse("Error fetching bug report -- " + str(e) + "<br>TODO: replace this with a 404?", status=400)
        

    elif request.method == 'POST':
        try:
            theBug = models.BugReport.objects.get(id__exact=int(request.POST['id']))
            
            theBug.status=request.POST['newStatus']
            theBug.resolvedText=request.POST['resolutionMessage']

            print request.POST['active']
            
            # handle a request to disable the bug
            if request.POST['active'] == 'false':
                theBug.active = False
            else:
                theBug.active = True


            theBug.save()
            
            return HttpResponse("", status=200)
            
        except Exception as e:
            return HttpResponse("Error modifying bug report - " + str(e), status=400)
        
        
    
    return HttpResponse("")








@login_required
def submit(request):
    """ Renders the page and handles POST requests for creating a new BugReport
    """
    if request.method == 'GET':  # we should render the page
        nbar = NavigationBar()
        context = nbar.generateNavBar(request)
        context.update({'title':"Write a bug report"})
        context.update(csrf(request))  # add cross-site request forgery protection
        context.update({'csrfTokenValue':csrf(request)['csrf_token']})  # add the token a second way

        # decode the GET data we'll want as default values... which URL are we coming from?
        try:  href = request.GET['href']
        except Exception:  href = ""

        # add default data to context
        context.update({ 'href': href, 'bugTypeChoices': models.BugReport.BUG_TYPE_CHOICES} )
        
        return render_to_response("submit.html", context)

    elif request.method == 'POST':
        # try to decode the POST data to get our information
        try:
            # create the new object!
            newBug = models.BugReport( user = request.user,
                                       webBrowserData = request.POST['webBrowserData'],
                                       hipercicVersion = request.POST['hipercicVersion'],
                                       sourceUrl = request.POST['sourceUrl'],
                                       summary = request.POST['summary'],                                      
                                       reportText = request.POST['reportText'],
                                       bugType = request.POST['bugType'], )

            newBug.save()
            print "bugs/submit: saved new bug id " + str(newBug.id)
            
            return HttpResponse("",status=200)
            
        except Exception as e:
            print "bugs/submit: Error: " + str(e)
            return HttpResponse("Error creating bug object - " + str(e), status=400)
    
    return HttpResponse("Badly formed Http Request to " + str(request.path),status=403)
        



    
