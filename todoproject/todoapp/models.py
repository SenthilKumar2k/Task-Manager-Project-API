from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    username=models.CharField(max_length=20, unique=True)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=20)

class Todolist(models.Model):
    Task=models.CharField(max_length=30)
    Task_assign_time=models.DateTimeField(default=timezone.now)
    completed=models.BooleanField(default=False)
    username=models.ForeignKey(User, on_delete=models.CASCADE, related_name='details')

