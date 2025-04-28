"""
here i create my accounts models
"""
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    """
    User's class
    """
    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('seller', 'Seller'),
        ('manager', 'Manager'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='owner')
    groups = models.ManyToManyField(
        Group,
        related_name='accounts_user_groups',  # Nom unique
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='accounts_user_permissions',  # Nom unique
        blank=True
    )
    def __str__(self):
        return f"{self.username}"