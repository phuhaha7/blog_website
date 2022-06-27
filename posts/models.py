from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100, blank=False)
    body = models.CharField(max_length=1000000, blank=False)
    created_at = models.DateTimeField(default=datetime.now, blank=True)