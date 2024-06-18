from django.urls import path
from . import views

urlpatterns = [
    path('projects/', views.ProjectListCreateAPIView.as_view(), name='project-list-create'),
    path('projects/<int:pk>/', views.ProjectRetrieveUpdateDestroyAPIView.as_view(), name='project-retrieve-update-destroy'),
    path('projects/<int:pk>/tasks/', views.TaskListCreateAPIView.as_view(), name='task-list-create'),
    path('projects/<int:pk>/tasks/<int:task_id>/', views.TaskRetrieveUpdateDestroyAPIView.as_view(), name='task-retrieve-update-destroy'),
]
