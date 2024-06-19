from rest_framework import serializers
from .models import ProjectPermission, Project
from authentication.models import User

from rest_framework import serializers
from .models import ProjectPermission

class ProjectPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectPermission
        fields = ['id', 'user', 'project', 'can_create', 'can_read', 'can_update', 'can_delete', 'can_add_users', 'created_at', 'updated_at']

# projects/serializers.py

from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner', 'users', 'is_deleted']
        read_only_fields = ['owner', 'is_deleted']

    def create(self, validated_data):
        users_data = validated_data.pop('users', [])
        owner = self.context['request'].user
        project = Project.objects.create(owner=owner, **validated_data)
        project.users.set(users_data)
        return project
