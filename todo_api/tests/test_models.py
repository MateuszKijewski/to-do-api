from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from todo_api import serializers

TODO_LIST_URL = reverse('todo_api:todo-list')

class TodoListTests(TestCase):

    def setUp(self):
        self.client = APIClient()
    
    def test_login_required(self):
        """Test that the login is required to retrieve list"""
        res = self.client.get(TODO_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)