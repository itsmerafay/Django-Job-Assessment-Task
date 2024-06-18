from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Project, Task
from .serializers import ProjectSerializer
from tasks.serializers import TaskSerializer

class ProjectListCreateAPIView(APIView):
    def get(self, request):
        projects = Project.objects.filter(is_deleted=False)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ProjectSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectRetrieveUpdateDestroyAPIView(APIView):
    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk, is_deleted=False)
        except Project.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)
    
    def put(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        project = self.get_object(pk)
        project.is_deleted = True  # Soft delete logic
        project.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TaskListCreateAPIView(APIView):
    def get(self, request, pk):
        tasks = Task.objects.filter(project_id=pk, is_deleted=False)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    
    def post(self, request, pk):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(project_id=pk)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskRetrieveUpdateDestroyAPIView(APIView):
    def get_object(self, pk, task_id):
        try:
            return Task.objects.get(pk=task_id, project_id=pk, is_deleted=False)
        except Task.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, task_id):
        task = self.get_object(pk, task_id)
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    
    def put(self, request, pk, task_id):
        task = self.get_object(pk, task_id)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, task_id):
        task = self.get_object(pk, task_id)
        task.is_deleted = True  # Soft delete logic
        task.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
