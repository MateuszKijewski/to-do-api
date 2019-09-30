from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from todo_api import serializers
from todo_api import models
from todo_api import permissions


class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    queryset = models.UserProfile.objects.all()


class UserLoginApiView(ObtainAuthToken):
    """Handle creating user auth tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class TodoTaskViewset(viewsets.ModelViewSet):
    """Handle creating and checking Tasks"""
    serializer_class = serializers.TodoTaskSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.TodoListPermission, IsAuthenticated,)
    filterset_fields = ['task_status']
    
    def get_queryset(self):
        """Gets the queryset for an authenticated user"""
        user = self.request.user
        return models.TodoTask.objects.filter(user=user)
    
    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user=self.request.user, task_status=models.TodoTask.TO_DO)


class TaskDeleteApiView(APIView):
    """Handle tasks deleting"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.TaskDeletePermission, IsAuthenticated,)

    def post(self, request, format=None):
        """Deletes objects that user posted"""
        serializer = serializers.TaskDeleteSerializer(data=request.data)
        if serializer.is_valid():
            ids = serializer.validated_data.get('ids')            
            for value in ids:
                value = int(value)
                try:
                    task = models.TodoTask.objects.get(pk=value)
                except models.TodoTask.DoesNotExist:
                    return Response({'message': 'Some of the given objects doesnt exist'})
            for value in ids:
                task = models.TodoTask.objects.get(pk=value)
                task.delete()
            return Response({'message': 'Objects were succesfully deleted'})
        
        return Response(
            {
                'errors': serializer.errors,
                'request': request.data
            }
        )
                    