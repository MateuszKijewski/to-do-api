from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, name, password):
        """Create new user profile"""
        if not email or not password:
            raise ValueError('Users must specify both email and password')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Create a new superuser"""
        user = self.create_user(email, name, password)
        user.is_superuser = True
        user.save(using=self._db)

        return user      


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    objects = UserProfileManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        """Return string representation of user"""
        return self.email


class TodoTask(models.Model):
    """Database model for tasks"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE
    )
    task_name = models.CharField(max_length=255)
    TO_DO = 'To do'
    IN_PROGRESS = 'In progress'
    REJECTED = 'Rejected'
    DONE = 'Done'
    POSTPONED = 'Postponed'
    TASK_STATUS_CHOICES = [
        (TO_DO, 'To do'),
        (IN_PROGRESS, 'In progress'),
        (REJECTED, 'Rejected'),
        (DONE, 'Done'),
        (POSTPONED, 'Postponed')
    ]
    task_status = models.CharField(
        max_length=255,
        choices=TASK_STATUS_CHOICES,
        default=TO_DO
    )    
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """String representation of the model"""
        return self.task_name
    