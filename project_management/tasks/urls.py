from django.urls import path
from .views import TaskListCreateAPIView, TaskRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('<int:pk>/tasks/', TaskListCreateAPIView.as_view(), name='task-list-create'),  # List and create tasks for a project
    path('<int:pk>/tasks/<int:task_id>/', TaskRetrieveUpdateDestroyAPIView.as_view(), name='task-retrieve-update-destroy'),  # Retrieve, update, and delete a specific task
]
