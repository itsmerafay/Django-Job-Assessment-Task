from rest_framework.permissions import BasePermission
from .models import Project , ProjectPermission
from tasks.models import Task

# This line of code checks if the user making the request is either:
# The owner of the project (obj.owner == request.user), or
# A user who has been granted read permission for the project 
from rest_framework.permissions import BasePermission

class IsProjectOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Only the owner can access the project
        return obj.owner == request.user
