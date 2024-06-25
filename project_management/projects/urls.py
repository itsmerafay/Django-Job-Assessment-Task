from django.urls import path, include
from .views import ProjectListCreateView, ProjectDetailView, AddProjectMemberView

urlpatterns = [
    path('projects/', ProjectListCreateView.as_view(), name='projects-list-create'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('projects/<int:pk>/add_member/', AddProjectMemberView.as_view(), name='project-add-member')
]

