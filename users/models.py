from django.db import models
from django.contrib.auth.models import AbstractUser
from users.managers import CustomUserManager


# Create your models here.
class User(AbstractUser):
    ADMIN = 'admin'
    AUTHOR = 'author'
    REVIEWSER = 'reviewer'
    USER = 'guest'

    ROLE_CHOICES = (
            ('admin', 'Admin'),
            ('author', 'Author'),
            ('reviewer', 'Reviewer'),
            ('guest', 'Guest'),
        )
    
    username = 'None'
    email = models.EmailField(unique=True)
    first_name=models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100,null=True, blank=True)
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='guest', db_index=True)
    institution = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # username remove must be override objects manager
    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    class Meta:
        indexes = [
            models.Index(fields=['role', 'is_active']),
        ]
    