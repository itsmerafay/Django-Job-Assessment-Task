from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate 
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .renderers import UserRenderer
from .serializers import UserRegistrationSerializer, UserLoginSerializer

# Manually generating the token
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }


class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request, format=None):
        if request.user.is_authenticated:
            return Response({
                'error': 'Authenticated users cannot access the registration endpoint.'
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserRegistrationSerializer(data=request.data)
        # work already done in serializers.py
        # raise_exception here is raised from serialization to simplifies error logic in views
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({
            'msg': 'Registration Successful',
            'access': token 
            }, status = status.HTTP_201_CREATED)

        return Response({
            serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)
    


class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):

        serializer = UserLoginSerializer(data=request.data)

        # if there is any exception then throw it
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            token = get_tokens_for_user(user)
            if user is not None:
                return Response({
                    'msg': 'LoggedIn Successfully ',
                    'token': token
                }, status=status.HTTP_200_OK)
            else:

                return Response({
                    'errors':{'non_field_errors':['Email or password is not valid']}
                }, status = status.HTTP_404_NOT_FOUND)
            