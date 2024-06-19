from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from .managers import ProjectQuerySet

class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="owned_projects", on_delete=models.CASCADE)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="projects", through='ProjectPermission')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    objects = ProjectQuerySet.as_manager()

    def __str__(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Check if owner is in the list of users
        if self.owner_id in self.users.values_list('id', flat=True):
            raise ValidationError("The project owner cannot have permissions for themselves.")


class ProjectPermission(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    can_create = models.BooleanField(default=False)
    can_read = models.BooleanField(default=False)
    can_update = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    can_add_users = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Allow saving if user is not the owner of the project
        if self.project.owner == self.user:
            raise ValidationError("The project owner cannot have permissions for themselves.")
        
        super().save(*args, **kwargs)