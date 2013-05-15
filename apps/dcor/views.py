# HiPerCic Project / St. Olaf College / Computer Science Dept.
###################################################################################
# apps/dcor/views.py
# Holds the methods which render templates into pages.  Called from urls.py
###################################################################################
import subprocess
import os

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import Template, Context
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.core import serializers
from django.views.decorators.csrf import *
from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from django.db import models

from datetime import datetime
from hipercic.apps.dcor import models # Don't forget to dcor!!!
from hipercic.hipercore.admin.hipercicViewHelpers import NavigationBar
from hipercic.hipercore.authenticore.decorators import login_required

ASSET_CHOICES = []
for a in models.Asset.objects.raw('SELECT * FROM dcor_asset'):
	temp_tuple = (str(a.name), str(a.name))
	ASSET_CHOICES.append(temp_tuple)
	
class TwoAssetsForm(forms.Form):
	start_date = forms.DateField()
	end_date   = forms.DateField()
	asset1     = forms.ChoiceField(ASSET_CHOICES)
	per_asset1 = forms.IntegerField(min_value = 0, max_value = 100)
	asset2     = forms.ChoiceField(ASSET_CHOICES)
	per_asset2 = forms.IntegerField(min_value = 0, max_value = 100)

class MultiAssetsForm(forms.Form):
	start_date       = forms.DateField()
	end_date         = forms.DateField()
	assets           = forms.MultipleChoiceField(required=True, widget=CheckboxSelectMultiple, choices=ASSET_CHOICES)
	portfolio_size  = forms.IntegerField()

# include csrf protection and standard Hipercic title block
#@login_required    # uncomment to require a login -- for use on a full server only!

def home(request):
	navbar = NavigationBar()
	context = navbar.generateNavBar(request, current_app='dcor')
	context['title'] = 'Home'
	context.update(csrf(request))  # add cross-site request forgery protection - useful for POST and javascript
	context.update({'csrfTokenValue':csrf(request)['csrf_token']})  # add the token a second way
	return render_to_response("base_home.html", context)
 

def job_submit(request):
	navbar = NavigationBar()
	context = navbar.generateNavBar(request, current_app='dcor')
	context['title'] = 'Submit'
	context.update(csrf(request))  # add cross-site request forgery protection - useful for POST and javascript
	context.update({'csrfTokenValue':csrf(request)['csrf_token']})  # add the token a second way
	return render(request, "base_job_submit.html", context)

def job_two_assets(request):
	navbar = NavigationBar()
	context = navbar.generateNavBar(request, current_app='dcor')
	context['title'] = 'Two Assets Job'
	context.update(csrf(request))  # add cross-site request forgery protection - useful for POST and javascript
	context.update({'csrfTokenValue':csrf(request)['csrf_token']})  # add the token a second way
		
	form = TwoAssetsForm(request.POST or None)
	context['form'] = form
	if request.method == 'POST':
		if form.is_valid():
			# write file in ~/hipercic/apps/dcor/jobs/
			with open('apps/dcor/jobs/job_' + datetime.today().strftime("%y%m%d_%h%m%s") + '_params.txt', 'w') as params_file:
				params_file.write(str(form.cleaned_data['start_date']) + '\n')
				params_file.write(str(form.cleaned_data['end_date']) + '\n')
				params_file.write(str(form.cleaned_data['asset1']) + ',')
				params_file.write(str(form.cleaned_data['asset2']) + '\n')
				params_file.write(str(form.cleaned_data['per_asset1']) + ',')
				params_file.write(str(form.cleaned_data['per_asset2']) + '\n')
				params_file.write(str(2)) # default value for portofolio_size

			request.session['job_filename'] = params_file.name
			scp = 'scp /home/guillet/hipercic/' + params_file.name + ' guillet@helios.public.stolaf.edu:dcor_backend/jobs/'
			#context['scp'] = scp
			return_code_scp = subprocess.call(scp, shell=True)
			#context['return_code_scp'] = return_code_scp
		
			head, tail = os.path.split(params_file.name)
			#print tail
			cpp = 'ssh guillet@helios.public.stolaf.edu "cd dcor_backend; ./dcor jobs/' + tail + '"'
			#context['cpp'] = cpp
			return_code_cpp = subprocess.call(cpp, shell=True)
			#context['return_code_cpp'] = return_code_cpp
			return render(request, 'base_job_result.html', context)

	return render(request, 'base_job_two_assets.html', context)

def job_multi_assets(request):
	navbar = NavigationBar()
	context = navbar.generateNavBar(request, current_app='dcor')
	context['title'] = 'Multi Assets Job'
	context.update(csrf(request))  # add cross-site request forgery protection - useful for POST and javascript
	context.update({'csrfTokenValue':csrf(request)['csrf_token']})  # add the token a second way
	
	form = MultiAssetsForm(request.POST or None)
	context['form'] = form
	if request.method == 'POST':
		if form.is_valid():
			# write file in ~/hipercic/apps/dcor/jobs/
			with open('apps/dcor/jobs/job_' + datetime.today().strftime("%Y%m%d_%H%M%S") + '_params.txt', 'w') as params_file:
				params_file.write(str(form.cleaned_data['start_date']) + '\n')
				params_file.write(str(form.cleaned_data['end_date']) + '\n')
				print u','.join(form.cleaned_data['assets']) 
				params_file.write(u','.join(form.cleaned_data['assets']) + '\n')
				# only for consistency of file format between two and multi assets mode	
				params_file.write('void\n')
				params_file.write(str(form.cleaned_data['portfolio_size']))
			
			request.session['job_filename'] = params_file.name
			scp = 'scp /home/guillet/hipercic/' + params_file.name + ' guillet@helios.public.stolaf.edu:dcor_backend/jobs/'

			scp = 'scp /home/guillet/hipercic/' + params_file.name + ' guillet@helios.public.stolaf.edu:dcor_backend/jobs/'
			#context['scp'] = scp
			return_code_scp = subprocess.call(scp, shell=True)
			#context['return_code_scp'] = return_code_scp
		
			head, tail = os.path.split(params_file.name)
			#print tail
			cpp = 'ssh guillet@helios.public.stolaf.edu "cd dcor_backend; ./dcor jobs/' + tail + '"'
			#context['cpp'] = cpp
			return_code_cpp = subprocess.call(cpp, shell=True)
			#context['return_code_cpp'] = return_code_cpp
			return render(request, 'base_job_result.html', context)	
	
	return render(request, 'base_job_multi_assets.html', context)

def job_result(request):
	navbar = NavigationBar()
	context = navbar.generateNavBar(request, current_app='dcor')
	context['title'] = 'Job result'
	context.update(csrf(request))  # add cross-site request forgery protection - useful for POST and javascript
	context.update({'csrfTokenValue':csrf(request)['csrf_token']})  # add the token a second way

	job_filename = request.session['job_filename']
	with open(job_filename, 'r') as job_parameters_file:
		for line_number, line in enumerate(job_parameters_file):
			if line_number == 0:
				context['param_start_date'] = line.rstrip()
			if line_number == 1:
				context['param_stop_date'] = line.rstrip()
			if line_number == 2:
				context['param_assets'] = line.rstrip()
			if line_number == 3:
				context['param_percentages'] = line.rstrip()

	two_assets_mode = False
	if context['param_percentages'] != 'void':
		two_assets_mode = True
		
	if (two_assets_mode):
		context['two_assets_mode'] = 'true' 
	else:
		context['two_assets_mode'] = 'false' 

	job_result_filename = job_filename[:-4] + '_results.txt'
	context['job_result_filename'] = job_result_filename	
	with open(job_result_filename, 'r') as job_result_file:
		for line_number, line in enumerate(job_result_file):
			if line_number == 0:
				context['return_value'] = line.rstrip()
			if line_number == 1:
				context['result_start_date'] = line.rstrip()
			if line_number == 2:
				context['result_stop_date'] = line.rstrip()
			if line_number == 3:
				context['result_combination'] = line.rstrip()
			if line_number == 4:
				context['result_percentages'] = line.rstrip()
			if line_number == 5:
				context['portfolio_distribution'] = '[' + line.rstrip() + ']'
	return render_to_response("base_job_result.html", context)

def about_us(request):
	navbar = NavigationBar()
	context = navbar.generateNavBar(request, current_app='dcor')
	context['title'] = 'About Us'
	return render_to_response("base_about_us.html", context)


def about_project(request):
	navbar = NavigationBar()
	context = navbar.generateNavBar(request, current_app='dcor')
	context['title'] = 'About Project'
	return render_to_response("base_about_project.html", context)

def glossary(request):
	navbar = NavigationBar()
	context = navbar.generateNavBar(request, current_app='dcor')
	context['title'] = 'Glossary'
	return render_to_response("base_glossary.html", context)

def etf_explanations(request):
	navbar = NavigationBar()
	context = navbar.generateNavBar(request, current_app='dcor')
	context['title'] = 'ETF Explanations'
	return render_to_response("base_etf_explanations.html", context)
