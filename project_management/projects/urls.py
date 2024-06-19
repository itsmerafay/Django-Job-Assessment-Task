from django.urls import path
from . import views

urlpatterns = [
    path('projects/', views.ProjectListCreateAPIView.as_view(), name='project-list-create'),
    path('projects/<int:pk>/', views.ProjectRetrieveUpdateDestroyAPIView.as_view(), name='project-retrieve-update-destroy'),
    path('projects/<int:pk>/permissions/', views.ProjectPermissionUpdateAPIView.as_view(), name='project-permissions'),

]
