from django.contrib import admin
from authentication.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserModelAdmin(BaseUserAdmin):
    list_display = ('id', 'email', 'name', 'tc' ,'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        ('User Credentials', {'fields':('email','password')}),
        ('Personal Info', {'fields':('name','tc')}),
        ('Permissions', {'fields':('is_admin',)}),
    )

    # when add user through admin pannel

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'tc', 'password1','password2'), 
        }),
    )

    search_fields = ('email',)
    ordering = ('email','id')
    filter_horizontal = ()

admin.site.register(User, UserModelAdmin)