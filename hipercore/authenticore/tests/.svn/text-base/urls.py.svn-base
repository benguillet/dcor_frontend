from django.conf.urls.defaults import patterns
from hipercic.hipercore.authenticore.urls import urlpatterns
from django.http import HttpResponse
from django.template import Template, RequestContext

def remote_user_auth_view(request):
    "Dummy view for remote user tests"
    t = Template("Username is {{ user }}.")
    c = RequestContext(request, {})
    return HttpResponse(t.render(c))

# special urls for authenticore test cases
urlpatterns = urlpatterns + patterns('',
    (r'^logout/custom_query/$', 'hipercic.hipercore.authenticore\.views.logout', dict(redirect_field_name='follow')),
    (r'^logout/next_page/$', 'hipercic.hipercore.authenticore\.views.logout', dict(next_page='/somewhere/')),
    (r'^remote_user/$', remote_user_auth_view),
)

