"""
here i create my accounts models
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import check_password


class User(AbstractUser):
    """
    User's class
    """
    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('seller', 'Seller'),
        ('manager', 'Manager'),
    ]
    role = models.CharField(max_length=20,
                            choices=ROLE_CHOICES,
                            default='owner')

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    def __str__(self):
        return f"{self.email}"
     