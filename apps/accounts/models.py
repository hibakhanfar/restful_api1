from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__( self):
        return self.username

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  bio = models.TextField(blank=True, null=True)
  avatar_url=models.URLField(blank=True, null=True)
  created_at=models.DateTimeField(auto_now_add=True)

  def __str__(self):
      return self.user.username
