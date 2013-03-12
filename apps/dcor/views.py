# HiPerCic Project / St. Olaf College / Computer Science Dept.
###################################################################################
# apps/dcor/views.py
# Holds the methods which render templates into pages.  Called from urls.py
###################################################################################
import subprocess

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import Template, Context
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.core import serializers
from django.views.decorators.csrf import *
from django import forms

from datetime import datetime
from hipercic.apps.dcor import models # Don't forget to dcor!!!
from hipercic.hipercore.admin.hipercicViewHelpers import NavigationBar
from hipercic.hipercore.authenticore.decorators import login_required

class SubmitForm(forms.Form):
	ASSET_CHOICES = (
			('rem', 'REM'),
			('iwm', 'IWM'),
			('vmo', 'VMO'),
    )
	
	start_date = forms.DateField()
	end_date   = forms.DateField()
	asset1     = forms.ChoiceField(ASSET_CHOICES)
	per_asset1 = forms.IntegerField(min_value = 0, max_value = 100)
	asset2     = forms.ChoiceField(ASSET_CHOICES)
	per_asset2 = forms.IntegerField(min_value = 0, max_value = 100)
	amount     = forms.FloatField(min_value = 0.0)	

# include csrf protection and standard Hipercic title block
#@login_required    # uncomment to require a login -- for use on a full server only!
def home(request):
	navbar = NavigationBar()
	context = navbar.generateNavBar(request, current_app='dcor')
	context['title'] = 'Home'
	context.update(csrf(request))  # add cross-site request forgery protection - useful for POST and javascript
	context.update({'csrfTokenValue':csrf(request)['csrf_token']})  # add the token a second way

	# insert additional content rendering here
	
	return render_to_response("base_home.html", context)

def job_submit(request):
	navbar = NavigationBar()
	context = navbar.generateNavBar(request, current_app='dcor')
	context['title'] = 'Submit'
	context.update(csrf(request))  # add cross-site request forgery protection - useful for POST and javascript
	context.update({'csrfTokenValue':csrf(request)['csrf_token']})  # add the token a second way
	
	form = SubmitForm(request.POST or None)
	context['form'] = form
	if request.method == 'POST':
		if form.is_valid():
			# write file in ~/hipercic/apps/dcor/jobs/
			params_file = open('apps/dcor/jobs/job_' + datetime.today().strftime("%Y%m%d_%H%M%S") + '_params.txt', 'w')
			for key, val in form.cleaned_data.iteritems():
				params_file.write(str(val) + ' \n')
			params_file.close
			cmd = 'scp /home/guillet/hipercic/' + params_file.name + ' guillet@helios.public.stolaf.edu:'
			context['cmd'] = cmd
			return_code = subprocess.call(cmd.split())
			return render(request, 'base_pending.html', context)
	
	return render(request, "base_submit.html", context)

def job_pending(request):
	navbar = NavigationBar()
	context = navbar.generateNavBar(request, current_app='dcor')
	context['title'] = 'Pending'
	context.update(csrf(request))  # add cross-site request forgery protection - useful for POST and javascript
	context.update({'csrfTokenValue':csrf(request)['csrf_token']})  # add the token a second way

	# insert additional content rendering here
	
	return render_to_response("base_pending.html", context)
