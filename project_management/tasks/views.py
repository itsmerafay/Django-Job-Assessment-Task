# tasks/views.py

from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer
from projects.models import Project


# tasks/views.py
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Task
from .serializers import TaskSerializer
from projects.permissions import IsProjectOwner
from projects.models import Project

class TaskListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsProjectOwner]

    def get_project(self, project_id):
        try:
            return Project.objects.get(pk=project_id, is_deleted=False)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, project_id):
        project = self.get_project(project_id)
        self.check_object_permissions(request, project)
        tasks = Task.objects.filter(project_id=project_id, is_deleted=False)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    
    def post(self, request, project_id):
        project = self.get_project(project_id)
        self.check_object_permissions(request, project)
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(project_id=project_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskRetrieveUpdateDestroyAPIView(APIView):
    permission_classes = [IsAuthenticated, IsProjectOwner]

    def get_object(self, project_id, task_id):
        try:
            return Task.objects.get(pk=task_id, project_id=project_id, is_deleted=False)
        except Task.DoesNotExist:
            raise Http404

    def get_project(self, project_id):
        try:
            return Project.objects.get(pk=project_id, is_deleted=False)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, project_id, task_id):
        project = self.get_project(project_id)
        self.check_object_permissions(request, project)
        task = self.get_object(project_id, task_id)
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    
    def put(self, request, project_id, task_id):
        project = self.get_project(project_id)
        self.check_object_permissions(request, project)
        task = self.get_object(project_id, task_id)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, project_id, task_id):
        project = self.get_project(project_id)
        self.check_object_permissions(request, project)
        task = self.get_object(project_id, task_id)
        task.is_deleted = True  # Soft delete logic
        task.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
