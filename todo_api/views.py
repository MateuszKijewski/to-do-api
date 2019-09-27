from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated

from todo_api import serializers
from todo_api import models


class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    pass


