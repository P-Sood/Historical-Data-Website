from django.db import models
from django.contrib.auth.models import User
from datetime import timezone
from django_celery_results.models import TaskResult
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import JSONField

# Create your models here.

class UserExtensionModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key = True)
    numCeleryTasks_Recorded = models.PositiveIntegerField()
    arrayTasksCompleted = ArrayField(base_field = models.IntegerField())
