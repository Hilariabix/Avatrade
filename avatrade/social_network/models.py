from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None  # remove this field, use email as username
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    name = models.CharField(max_length=50, blank=True, null=True)
    bio = models.CharField(max_length=250, blank=True, null=True)
    role = models.CharField(max_length=50, blank=True, null=True)
    location = models.CharField(max_length=250, blank=True, null=True)
    company = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Post(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Like(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (("user_id", "post_id"),)
