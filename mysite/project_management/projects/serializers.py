from rest_framework import serializers
from .models import ProjectPermission, Project
from authentication.models import User

class ProjectPermissionSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    project = serializers.SlugRelatedField(slug_field='name', queryset=Project.objects.active())

    class Meta:
        model = ProjectPermission
        fields = ['id', 'user', 'project', 'can_create', 'can_read', 'can_update', 'can_delete', 'can_add_users', 'created_at', 'updated_at']


from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email', default=serializers.CurrentUserDefault())

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner', 'created_at', 'updated_at']

    def create(self, validated_data):
        owner = self.context['request'].user
        project = Project.objects.create(owner=owner, **validated_data)
        return project

