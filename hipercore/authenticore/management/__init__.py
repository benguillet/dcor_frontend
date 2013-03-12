"""
Creates permissions for all installed apps that need permissions.
"""

from django.db.models import get_models, signals
from hipercic.hipercore.authenticore import models as auth_app

def _get_permission_codename(action, opts):
    return u'%s_%s' % (action, opts.object_name.lower())

def _get_all_permissions(opts):
    "Returns (codename, name) for all permissions in the given opts."
    perms = []
    for action in ('add', 'change', 'delete'): # Modifying_permissions
        perms.append((_get_permission_codename(action, opts), u'Can %s %s' % (action, opts.verbose_name_raw)))
    return perms + list(opts.permissions)

def create_permissions(app, created_models, verbosity, **kwargs):
    from hipercic.hipercore.authenticore.models import Permission, App
    #from hipercic.apps.appConfig import ACTIVE_APPS
    from hipercic.hipercore.permissions import all_perms
    apps = App.objects.all()
    perms= all_perms()
    for app in apps:
        for perm in perms:
            p, created = Permission.objects.get_or_create(name=perm['title'], app=app)
    	    if created:
		print p.name + "|" + p.app.name    

def create_superuser(app, created_models, verbosity, **kwargs):
    from hipercic.hipercore.authenticore.models import User
    from django.core.management import call_command
    if User in created_models and kwargs.get('interactive', True):
        msg = "\nYou just installed Django's authenticore system, which means you don't have " \
                "any admin defined.\nWould you like to create one now? (YES/no): "
        confirm = raw_input(msg)
        while 1:
	    if confirm == '':
		confirm = 'yes'
            if confirm not in ('yes', 'no'):
                confirm = raw_input('Please enter either "yes" or "no": ')
                continue
            if confirm == 'yes':
                call_command("createsuperuser", interactive=True)
            break

def load_active_apps(**kwargs):
    from hipercic.apps.appConfig import ACTIVE_APPS
    from hipercic.hipercore.authenticore.models import App
    for app in ACTIVE_APPS:
        a, created = App.objects.get_or_create(name=app, is_active=True) #put each app into the database...
        if created:
            print "Added app '%s'" % a
            
signals.post_syncdb.connect(load_active_apps, 
    dispatch_uid = "hipercic.hipercore.authenticore.management.load_active_apps")
signals.post_syncdb.connect(create_permissions,
    dispatch_uid = "hipercic.hipercore.authenticore.management.create_permissions")
signals.post_syncdb.connect(create_superuser,
    sender=auth_app, dispatch_uid = "hipercic.hipercore.authenticore.management.create_superuser")
