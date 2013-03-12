# HiPerCic Project / St. Olaf College / Computer Science Dept.
###################################################################################
# hipercic/hipercore/bugs/models.py
# Created 7/26
# Holds python models for the bug reporting subsite
###################################################################################
import os
from django.db import models, transaction
from hipercic.hipercore.authenticore.models import User

class BugReport(models.Model):
	""" A model describing a bug report entry.
	"""
	
	active = models.BooleanField(default=True)  # set to false to "delete" this object
	
	## general data initialized when object is created ##
	dateSubmitted = models.DateTimeField(auto_now_add=True) # When was this object created?
	user = models.ForeignKey('authenticore.User')  # The user who submitted this bug report
	
	## bug-report-specific data ##
	webBrowserData = models.CharField(max_length=300)   # get from browser using javascript Navigator object (userAgent is most useful string)
	hipercicVersion = models.CharField(max_length=6)    # what is the version of hipercic under which this bug report was generated?
	sourceUrl = models.CharField(max_length=300)        # the URL from which the bug submit button was clicked
	summary = models.CharField(max_length=110)          # a brief summary of the bug
	reportText = models.TextField()                     # the bulk text describing the problem specifically
	
	## a field to describe the general type of bug ##
	BUG_TYPE_CHOICES = ( ('S','Suggestion'), ('B','Broken Link'), ('X','Security error'), ('A', 'App-specific bug'), ('O', 'Other bug'), )
	bugType = models.CharField(max_length=1, choices=BUG_TYPE_CHOICES)
	
	## data about the status of the bug report ##
	BUG_STATUS_CHOICES = ( ('O','Open'), ('RF','Resolved - Fixed'), ('RD','Resolved - Duplicate'), ('RI','Resolved - Invalid'), ('RW','Resolved - Will Not Fix'), ('C','Closed'),)
	status = models.CharField(max_length=2, choices=BUG_STATUS_CHOICES, default='O')  # what is the status of this bug?
	resolvedText = models.TextField(default="")    # The text describing the bug resoltion
	dateModified = models.DateTimeField(auto_now=True)  # keep track of the last time the model was saved... when was it modified?


	def __unicode__(self):
		return "BugReport object " + str(self.id) + ", submitted " + str(self.dateSubmitted) + " by " + str(self.user.id) + "\n   " + str(self.sourceUrl) + "\n   Bug Summary: " + str(self.summary)

	def __str__(self):
		return self.__unicode__()

