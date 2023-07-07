"""
Database models
"""

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class UserManager(BaseUserManager):
    """Manager for users"""

    def build_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create save and return a new user"""
        user = self.build_user(email, password, **extra_fields)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        """Create save and return a new superuser"""
        user = self.build_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)  # can login
    is_staff = models.BooleanField(default=False)  # is admin

    objects = UserManager()

    USERNAME_FIELD = 'email'  # default is username
