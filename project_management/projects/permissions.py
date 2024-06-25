from rest_framework.permissions import BasePermission
from .models import Project , ProjectMembership

# Obj is the instance of the project table (any)

class IsProjectOwnerOrMember(BasePermission):
    def has_object_permission(self, request, view, obj):

        if obj.owner == request.user:
            return True

        try:
            # checking if the user is the member of the project
            membership = ProjectMembership.objects.get(project=obj, user=request.user)
            if request.method in ['GET','HEAD','OPTIONS']:
                return True
            if request.method == 'POST' and membership.can_create:
                return True
            if request.method == 'PUT' and membership.can_update:
                return True
            if request.method == 'DELETE' and membership.can_delete:
                return True
            
        except ProjectMembership.DoesNotExist:
            return False

class CanManageUsers(BasePermission):
    def has_permission(self, request, view):
        # Allow access if the user has can_manage_users permission for the project
        project_id = view.kwargs.get('pk')
        project = Project.objects.get(id=project_id)
        
        # Check if the user is the project owner or has can_manage_users permission
        if project.owner == request.user:
            return True
        
        try:
            membership = ProjectMembership.objects.get(project=project, user=request.user)
            return membership.can_manage_users
        except ProjectMembership.DoesNotExist:
            return False