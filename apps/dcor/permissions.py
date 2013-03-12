# HiPerCic Project / St. Olaf College / Computer Science Dept.
###################################################################################
# apps/dcor/permissions.py
# Created INSERT_DATE
# This file manages permissions on the dcor application.  It contains three
# important methods for hipercore's permissions management, but the rest of the
# content is app-specific and therefore up to you.
###################################################################################

# TODO: should we change this to userIds instead?

## generate a list of dictionaries of input fields to help Hipercore render the admin site
# inputs: currentUser - the object for the current user (the user who is granting permissions)
# returns: a list of dictionaries (see below definition) 
def getGrantablePermissions(currentUser):
    
    
    
    pass


"""
Sample permissions:

*permissionsList containing a dictionary for each permission.
*Additional data can be added to these dictionaries and will be returned unmodified, but will not be displayed in hipercore.  Use additional fields
*when necessary to make your management of permissions easier.

**EACH PERMISSION MUST HAVE: id, title, type, value, description (can be None) and (depending on the type) possibleValues


permissionsList = [
                    { 'id':'ad84', 'title': 'Is allowed to view Dataset #1', 'description': 'dataset info #1', 'type': 'checkbox', 'value': 'False',  'possibleValues': ['value1','value2']},
                    { 'id':'38d', 'title': 'Is allowed to view Dataset #2', 'description': 'dataset info #2', 'type': 'checkbox', 'value': 'False',  },
                    { 'id':'asdf', 'title': 'Is allowed to make datasets from Computation #7', 'description': 'computation info #7', 'type': 'checkbox', 'value': 'False',  },
                    ]

type = ['dropdownlist' or 'checkbox' or 'list']
id: a unique string (per instance of permissionsList) containing only letters and numbers... no white space or other characters.
title: this is what the user will see as the name of the value they are changeing
value: self explanatory
possibleValues: only for types where there is a select one from a list.
description: must exist but can be "" or None.
"""

## return a dictionary describing all the permissions already given to a certian user
# inputs: currentUser - the object for the current user
# returns: a dictionary (see definition)
def getPermissionsForUser(User):

    pass





## process a permissions modification -- make the proper entries into the database
# inputs: modifiedUser - the object for the user whose permissions need to be set
#         permissionsDict - the dictionary of permissions to grant the user
# returns: true if permissions were successfully changed, throws errors otherwise.
def updatePermissions(modifiedUser, permissionsDict):
    
    pass
