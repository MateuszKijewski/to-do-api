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