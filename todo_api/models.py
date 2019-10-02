from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings

from todo_api import scrapers


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
        """Create and save a new superuser with given details"""
        user = self.create_user(email, name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user 


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

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


class QuoteGroup(models.Model):
    """Database model for quote groups"""
    name = models.CharField(max_length=255)
    quotes = models.CharField(max_length=16384)
    authors = models.CharField(max_length=2048)

    def update(self):
        self.quotes, self.authors = scrapers.inspirational_quotes_scraper()
        self.save()

    def __str__(self):
        return self.name
