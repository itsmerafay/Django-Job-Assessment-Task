from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Project, ProjectMembership
from .serializers import ProjectSerializer, ProjectMembershipSerializer
from .permissions import IsProjectOwnerOrMember, CanManageUsers
from django.shortcuts import get_object_or_404

class ProjectListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    # List all projects the authenticated user is a member of.

    def get(self, request):
        # memberships__user=request.user helps in querying projects that are associated with memberships where request.user
        projects = Project.objects.filter(is_deleted=False, memberships__user=request.user) 
        serializer = ProjectSerializer(projects, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
            )
    
    def post(self, request):

        request.data['owner'] = request.user.id

        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            project = serializer.save(owner=request.user)
            
            # Automatically adding the creator as the user of the project

            ProjectMembership.objects.create(
                user=request.user,
                project=project,
                can_create=True,
                can_update=True,
                can_delete=True,
                can_manage_users=True
            )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
class ProjectDetailView(APIView):

    permission_classes = [IsAuthenticated, IsProjectOwnerOrMember]

    # Specifc project with details

    def get_object(self,pk):
        return get_object_or_404(Project, pk=pk , is_deleted=False)

    # by default accept pk for Project because of above get_object
    def get(self, request, pk):
        project = self.get_object(pk)
        # this check object permissions iterate over all the permissions class defined above.
        self.check_object_permissions(request, project)
        serializer = ProjectSerializer(project)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
    
    def put(self, request, pk):
        project = self.get_object(pk)
        self.check_object_permissions(request, project)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)  # Return the updated data
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    def delete(self, request, pk):
        project = self.get_object(pk)
        self.check_object_permissions(request, project)
        project.is_deleted = True
        project.save()
        return Response(
            'Successfully deleted !!',
            status=status.HTTP_200_OK
        )
    

class AddProjectMemberView(APIView):
    permission_classes = [IsAuthenticated, CanManageUsers]
    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk, is_deleted=False)
        serializer = ProjectMembershipSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(project=project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        project = get_object_or_404(Project, pk=pk, is_deleted=False)
        self.check_object_permissions(request, project)
        
        user_id = request.data.get('user_id')  
        
        try:
            membership = ProjectMembership.objects.get(project=project, user_id=user_id)
            membership.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProjectMembership.DoesNotExist:
            return Response({"error": "Membership not found"}, status=status.HTTP_404_NOT_FOUND)