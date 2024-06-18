from rest_framework.permissions import BasePermission
from .models import Project , ProjectPermission
from tasks.models import Task

# This line of code checks if the user making the request is either:
# The owner of the project (obj.owner == request.user), or
# A user who has been granted read permission for the project 


class IsProjectOwnerOrHasPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the object is a project instance
        if isinstance(obj, Project):
            return obj.owner == request.user or ProjectPermission.objects.filter(user=request.user, project=obj, can_read=True).exists()
        
        if isinstance(obj, Task):
            # get the associated project
            project = obj.project
            
            # Allow access if the user is the owner of the project or has read permission for the project
            return project.owner == request.user or ProjectPermission.objects.filter(user=request, project=project, can_read=True).exists()

        if isinstance(obj, ProjectPermission):
            # Allow access if the user is the owner of the project related to this permission instance
            return obj.project.owner == request.user 

        # default to deny access
        return False