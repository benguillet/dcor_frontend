from django.db import transaction
from django.conf import settings
from hipercic.hipercore import admin
from hipercic.hipercore.authenticore.forms import UserCreationForm, UserChangeForm, AdminPasswordChangeForm
from hipercic.hipercore.authenticore.models import User, Group, App
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.html import escape
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext, ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect
############
from django import forms
from hipercic.hipercore.docGen.src.importer import importModule
csrf_protect_m = method_decorator(csrf_protect)

class GroupAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    ordering = ('name',)
    filter_horizontal = ('permissions',)

class AppAdmin(admin.ModelAdmin):
    pass

class UserAdmin(admin.ModelAdmin):
    """ Modify the fields in the edit user from (aka change_view, render_change_form)
    
    """
    add_form_template = 'admin/auth/user/add_form.html'
    change_user_password_template = None
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'apps', 'default_app')}),
        (_('Application Specific Permissions'), {'fields':()}),
        (_('Groups'), {'fields': ('groups',)}),
    )
    admin_fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'apps', 'default_app', 'is_app_manager','apps_managed', 'is_admin', 'user_permissions')}),
        (_('Application Specific Permissions'), {'fields':()}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Groups'), {'fields': ('groups',)}),
    )
    app_manager_fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'apps', 'default_app', 'is_app_manager','apps_managed', 'user_permissions')}),
        (_('Application Specific Permissions'), {'fields':()}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Groups'), {'fields': ('groups',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')}
        ),
    )
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ('username', 'email', 'is_admin', 'is_app_manager')
    list_filter = ('is_app_manager', 'is_admin', 'is_active', 'default_app')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    filter_horizonatal = ('user_permissions', 'apps_managed', 'apps')

    def __call__(self, request, url):
        # this should not be here, but must be due to the way __call__ routes
        # in ModelAdmin.
        if url is None:
            return self.changelist_view(request)
        if url.endswith('password'):
            return self.user_change_password(request, url.split('/')[0])
        return super(UserAdmin, self).__call__(request, url)

    def get_fieldsets(self, request, obj=None):
        """this function gets the fieldsets, as the name indicates. It also sets 
            the list of fieldsets based on the loged in user's status.  To change the
            fields that are displayed for each level of user, modify the if statement below 
            that sets the fieldsets variable.
        """
        if request.user.is_admin:
            self.fieldsets = self.admin_fieldsets #allows the admin to see all possible fields
            
        elif request.user.is_app_manager:
            self.fieldsets = self.app_manager_fieldsets #allows the app manager to see only some fields
        else:
            self.fieldsets = self.fieldsets #allows any user who may have reached the page to modify only default values
        if not obj: 
            return self.add_fieldsets
        
        return super(UserAdmin, self).get_fieldsets(request, obj)

    def change_view(self, request, object_id, extra_context=None):
        """ this allows the extra context needed to display app permissions 
            Template=change_form.html
        """
        def helper(currentUid, ModifiedUid, appList):
                
                appPerms=[]
                for app in appList:
                    obj = importModule('apps.'+app+'.permissions')
                    mperms=obj.getPermissionsForUser(ModifiedUid)
                    cperms=obj.getGrantablePermissions(currentUid)
                    if mperms != None and cperms != None:
                        for perm in mperms:
		                    for cperm in cperms:
			                    if perm['id'] == cperm['id']:
			    	                cperm['value'] = perm['value']
                        appPerms.append(cperms)
                return appPerms

        if request.method == 'POST':
            #from django.template.defaultfilters import slugify #doing this will not exactly work
            #users there manycase where two strings return the same slugified string!
            appList=[]
            if request.user.is_admin: # get all installed apps
                from hipercic.apps.appConfig import ACTIVE_APPS #import all ACTIVE_APPS apps
                appList = ACTIVE_APPS
            else:
                #get only the apps the user has permissions to
                apps = request.user.apps_managed.all()
                for app in apps:
                    appList.append(app.name)
            for app in appList:
                perm_dict = helper(request.user.id, object_id, [app]) #for each app get a perm dict
                for ls in perm_dict:
                  for perm in ls: #for every perm update all values
                    #find the key from the request with the correct id...
                    #print "old: ", perm['value']                    
                    perm['value'] = request.POST.__getitem__(perm['id'])
                    #print "new: ", perm['value']               
                    #update the value of the dictionary with the value from the request
                    obj = importModule('apps.'+app+'.permissions')
                    test = obj.updatePermissions(object_id, ls)    
            return super(UserAdmin, self).change_view(request, object_id, extra_context)
        #if request.path contains user... we know permissions for the user object must be loaded.
        
        else: #method is get generate user permissions

            
            appPerms=[]
            #Modify extra context to pass information to the template
            if request.user.is_admin: # get all installed apps
                from hipercic.apps.appConfig import ACTIVE_APPS #import all ACTIVE_APPS apps
                appPerms = helper(request.user.id, object_id, ACTIVE_APPS)
            else:
                #get only the apps the user has permissions to
                apps = request.user.apps_managed.all()
                appList=[]
                for app in apps:
                    appList.append(app.name)
                appPerms = helper(request.user.id, object_id, appList)
               
                #import permissions from only a few apps
                #pass a dictionary of dictionaries of permissions to the templates
        #pass a dictionary of dictionary permissions to the template
            if extra_context == None:
                return super(UserAdmin, self).change_view(request, object_id, {'appPerms':appPerms})
            else:
                extra_context.update({'appPerms':appPerms})
                return super(UserAdmin, self).change_view(request, object_id, extra_context)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """This is where modifications can be made to the content of the
            manytomany fields.  See the official django 1.2 contrib/admin documentation
            about ModelAdmin for details about overriding other types of fields
        """ 
        limited_list=['user_permissions','apps','apps_managed'] 
                    #This is a nested list of the field name and the associated Model name. 
        from hipercic.hipercore.authenticore.models import Permission
        from hipercic.hipercore.authenticore.models import App
        if db_field.name in limited_list: #this is for a list and not a list of dictionaries... FIX
            if request.user.is_admin: #if the user is an admin, display all fields
                if db_field.name == 'user_permissions':
                    kwargs["queryset"] = Permission.objects.filter()
                else:
                    kwargs["queryset"] = App.objects.filter()
            elif request.user.is_app_manager: #if the user is an app_manager display only the fields for the apps they manage
                ls = []
                for app in request.user.apps_managed.all():
                    ls.append(app.id)
                if db_field.name == 'user_permissions':
                    kwargs["queryset"] =  Permission.objects.filter(app__in=ls)
                else: 

                    kwargs["queryset"] = App.objects.filter(id__in=ls)
            else: #No fields should be displayed due to lack of permissions
                if db_field.name == 'user_permissions':                
                    kwargs["queryset"] = Permission.objects.filter(app=0)
                else:
                    kwargs["queryset"] = App.objects.filter(app=0)
        return super(UserAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
        
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """This is where modifications can be made to the content of the
            manytomany fields.  See the official django 1.2 contrib/admin documentation
            about ModelAdmin for details about overriding other types of fields
        """ 
        limited_list=['default_app'] 
                    #This is a nested list of the field name and the associated Model name. 

        from hipercic.hipercore.authenticore.models import App
        if db_field.name in limited_list: #this is for a list and not a list of dictionaries... FIX
            if request.user.is_admin: #if the user is an admin, display all fields
                kwargs["queryset"] = App.objects.filter()
            elif request.user.is_app_manager: #if the user is an app_manager display only the fields for the apps they manage
                ls = []
                for app in request.user.apps_managed.all():
                    ls.append(app.id)
                kwargs["queryset"] = App.objects.filter(id__in=ls)
            else: #No fields should be displayed due to lack of permissions
                kwargs["queryset"] = App.objects.filter(app=0)
        return super(UserAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
            

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during user creation
        """
        defaults = {}
        if obj is None:
            defaults.update({
                'form': self.add_form,
                'fields': admin.util.flatten_fieldsets(self.add_fieldsets),
            })
        defaults.update(kwargs)
        return super(UserAdmin, self).get_form(request, obj, **defaults)

    def get_urls(self):
        from django.conf.urls.defaults import patterns
        return patterns('',
            (r'^(\d+)/password/$', self.admin_site.admin_view(self.user_change_password))
        ) + super(UserAdmin, self).get_urls()

    @csrf_protect_m
    @transaction.commit_on_success
    def add_view(self, request, form_url='', extra_context=None):
	print request.user.is_admin
	print request.user.is_app_manager
        # It's an error for a user to have add permission but NOT change
        # permission for users. If we allowed such users to add users, they
        # could create superusers, which would mean they would essentially have
        # the permission to change users. To avoid the problem entirely, we
        # disallow users from adding users if they don't have change
        # permission.
        if not request.user.is_app_manager or not request.user.is_admin: #this needs to check for if user is app_manager or admin
            #if self.has_add_permission(request) and settings.DEBUG:
                # Raise Http404 in debug mode so that the user gets a helpful
                # error message.
                #raise Http404('Your user does not have the "Change user" permission. In order to add users, Django requires that your user account have both the "Add user" and "Change user" permissions set.')
            raise PermissionDenied
        if extra_context is None:
            extra_context = {}
        defaults = {
            'auto_populated_fields': (),
            'username_help_text': self.model._meta.get_field('username').help_text,
        }
        extra_context.update(defaults)
        return super(UserAdmin, self).add_view(request, form_url, extra_context)

    def user_change_password(self, request, id):
        if not self.has_change_permission(request):
            raise PermissionDenied
        user = get_object_or_404(self.model, pk=id)
        if request.method == 'POST':
            form = self.change_password_form(user, request.POST)
            if form.is_valid():
                new_user = form.save()
                msg = ugettext('Password changed successfully.')
                messages.success(request, msg)
                return HttpResponseRedirect('..')
        else:
            form = self.change_password_form(user)

        fieldsets = [(None, {'fields': form.base_fields.keys()})]
        adminForm = admin.helpers.AdminForm(form, fieldsets, {})

        return render_to_response(self.change_user_password_template or 'admin/auth/user/change_password.html', {
            'title': _('Change password: %s') % escape(user.username),
            'adminForm': adminForm,
            'form': form,
            'is_popup': '_popup' in request.REQUEST,
            'add': True,
            'change': False,
            'has_delete_permission': False,
            'has_change_permission': True,
            'has_absolute_url': False,
            'opts': self.model._meta,
            'original': user,
            'save_as': False,
            'show_save': True,
            'root_path': self.admin_site.root_path,
        }, context_instance=RequestContext(request))

    def response_add(self, request, obj, post_url_continue='../%s/'):
        """
        Determines the HttpResponse for the add_view stage. It mostly defers to
        its superclass implementation but is customized because the User model
        has a slightly different workflow.
        """
        if '_addanother' not in request.POST:
            # The 'Save' button should act like the 'Save and continue
            # editing' button
            request.POST['_continue'] = 1
        return super(UserAdmin, self).response_add(request, obj, post_url_continue)
        
    
admin.site.register(Group, GroupAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(App, AppAdmin)
