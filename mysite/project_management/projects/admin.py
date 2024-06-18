from django.contrib import admin

# Register your models here.
from .models import Project, ProjectPermission

admin.site.register(Project)
admin.site.register(ProjectPermission)