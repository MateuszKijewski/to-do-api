from rest_framework import serializers

from todo_api import models

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes user profiles"""

    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'password',)
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }
    
    def create(self, validated_data):
        """Creates and returns a new user"""
        user = models.UserProfile.objects.create_user(
            email = validated_data['email'],
            name = validated_data['name'],
            password = validated_data['password']
        )

        return user


class TodoTaskSerializer(serializers.ModelSerializer):
    """Serializes users TodoTasks"""

    class Meta:
        model = models.TodoTask
        fields = ('id', 'user', 'task_name', 'task_status', 'created_on',)
        extra_kwargs = {
            'user': {'read_only': True}
        }

class TaskDeleteSerializer(serializers.Serializer):
    """Serializes tasks that are about to be deleted"""
    ids = serializers.ListField(
        child=serializers.IntegerField()
    )