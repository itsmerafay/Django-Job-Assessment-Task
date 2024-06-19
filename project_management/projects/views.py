# projects/views.py
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Project, ProjectPermission
from .serializers import ProjectSerializer, ProjectPermissionSerializer
from .permissions import IsProjectOwner
from django.http import Http404

from rest_framework import status
from django.http import Http404

# projects/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Project
from .serializers import ProjectSerializer

class ProjectPermissionUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_project(self, pk):
        try:
            return Project.objects.get(pk=pk, is_deleted=False)
        except Project.DoesNotExist:
            raise Http404

    def get_object(self, project, user_id):
        try:
            return ProjectPermission.objects.filter(project=project, user__id=user_id).first()
        except ProjectPermission.DoesNotExist:
            return None

    def put(self, request, pk):
        project = self.get_project(pk)
        owner = request.user

        # Check if the request user is the owner of the project
        if project.owner != owner:
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

        user_id = request.data.get('user_id')
        permission_data = {
            'can_create': request.data.get('can_create', False),
            'can_read': request.data.get('can_read', False),
            'can_update': request.data.get('can_update', False),
            'can_delete': request.data.get('can_delete', False),
            'can_add_users': request.data.get('can_add_users', False),
        }

        # Ensure user_id is provided and it's not the owner's id
        if not user_id or user_id == owner.id:
            return Response({"detail": "Invalid user id provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve or create ProjectPermission for the specified user
        project_permission = self.get_object(project, user_id)
        if not project_permission:
            # Create new permission record
            serializer = ProjectPermissionSerializer(data={
                'project': project.id,
                'user': user_id,
                **permission_data
            })
        else:
            # Update existing permission record
            serializer = ProjectPermissionSerializer(project_permission, data=permission_data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






class ProjectListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        projects = Project.objects.filter(owner=request.user, is_deleted=False)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectRetrieveUpdateDestroyAPIView(APIView):
    permission_classes = [IsAuthenticated, IsProjectOwner]

    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk, is_deleted=False)
        except Project.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        project = self.get_object(pk)
        self.check_object_permissions(request, project)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)
    
    def put(self, request, pk):
        project = self.get_object(pk)
        self.check_object_permissions(request, project)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        project = self.get_object(pk)
        self.check_object_permissions(request, project)
        project.is_deleted = True  # Soft delete logic
        project.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
