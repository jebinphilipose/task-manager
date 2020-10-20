import uuid
from django.db import models

# Create your models here.
class Task(models.Model):
    class TaskStatus(models.TextChoices):
        CREATED = 'CREATED'
        PROCESSING = 'PROCESSING'
        PAUSED = 'PAUSED'
        CANCELLED = 'CANCELLED'
        COMPLETED = 'COMPLETED'
        FAILED = 'FAILED'

    type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=TaskStatus.choices, default=TaskStatus.CREATED)

    def __str__(self):
        return self.type
