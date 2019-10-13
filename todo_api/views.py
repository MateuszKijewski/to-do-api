import json
import random

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
from todo_api import scrapers


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
        serializer.save(
            user=self.request.user
        )


class TodoListViewset(viewsets.ModelViewSet):
    """Handle managing todo-lists"""
    serializer_class = serializers.TaskListSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.TodoListPermission, IsAuthenticated,)

    def get_queryset(self):
        """Gets the queryset for authenticated user"""
        user = self.request.user
        task_list = self.kwargs['']
        return models.TodoTaskList.objects.filter(user=user)
    
    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user=self.request.user)

    def retrieve(self, request, pk=None):
        pass

class ObjectDelete(APIView):
    """Handle tasks deleting"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.DeletePermission, IsAuthenticated,)
    queryset = None

    def post(self, request, format=None):
        """Deletes objects that user posted"""
        serializer = serializers.DeleteSerializer(data=request.data)
        if serializer.is_valid():
            ids = serializer.validated_data.get('ids')            
            for value in ids:
                value = int(value)
                try:
                    task = self.queryset.objects.get(pk=value)
                except self.queryset.DoesNotExist:
                    return Response({'message': 'Some of the given objects doesnt exist'})
            for value in ids:
                task = self.queryset.objects.get(pk=value)
                task.delete()
            return Response({'message': 'Objects were succesfully deleted'})
        
        return Response(
            {
                'errors': serializer.errors,
                'request': request.data
            }
        )


class TaskDelete(ObjectDelete):
    queryset = models.TodoTask

class TaskListDelete(ObjectDelete):
    queryset = models.TodoTaskList

class InspirationalQuote(APIView):
    """Outputs a random inspirational quote"""

    def get(self, request, format=None):
        quote_group = models.QuoteGroup.objects.get(name="inspirational quotes")

        quotes = json.loads(quote_group.quotes)
        authors = json.loads(quote_group.authors)
        quote_number = random.randint(0, (len(quotes)-1))

        return Response({
            'quote': quotes[quote_number],
            'author': authors[quote_number]
        })

    
