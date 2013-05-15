# HiPerCic Project / St. Olaf College / Computer Science Dept.
###################################################################################
# hipercic/urls.py
# Created 6/11
# Base URLs document for hipercic project
###################################################################################
from django.conf.urls.defaults import *
from hipercic.hipercore import admin

#admin.autodiscover()
from hipercic.hipercore.authenticore.views import login, logout
from hipercic.hipercore.admin.views.hipercic_home import placeHolder
from hipercic.apps.appConfig import *

# Uncomment the next two lines to enable the admin:
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^hipercic/', include('hipercic.foo.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

   #(r'^accounts/logout/$', logout),
    
    # site header (cjc 6/9)
    (r'^$', admin.site.login), 
    
    # this page should be removed or developed further...
    (r'^placeHolder/$', placeHolder),
    
    # documentation subsite
    #(r'^docs/', include('hipercic.hipercore.documentation.urls')),


    # for the bugreporter subsite
    #(r'^bugs/', include('hipercic.hipercore.bugs.urls')),
	
    # for the local API
    #(r'^api/', include('hipercic.hipercore.apiUrls')),

    # for the epyapi
    #(r'^epy_api/', include('hipercic.hipercore.epyUrls')),

)

### append the urlpatterns for the installed apps
urlpatterns += getAppURLPatterns()
