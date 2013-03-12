# HiPerCic Project / St. Olaf College / Computer Science Dept.
###################################################################################
# hipercic/hipercore/bugreporter/urls.py
# Created 7/26
###################################################################################
from django.conf.urls.defaults import *
from hipercic.hipercore import admin


urlpatterns = patterns('hipercic.hipercore.bugs.views',
                       
                       ('^submit','submit'),


                       # default is viewBugs
                       ('^$','viewBugs'),
                       ('^bug','bugDetails'),
                       ('^deletedbugs$','deletedBugs'),

)
